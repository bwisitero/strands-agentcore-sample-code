"""
Demo 16: Simple Slack Bot
Goal: Create a simple Slack bot that replies when messaged directly

Key Teaching Points:
- Basic Slack integration
- Direct message responses
- Webhook handling
- Simple agent responses
"""

import os
from dotenv import load_dotenv
from strands import Agent
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import requests

# Load environment variables
load_dotenv()

app = FastAPI(title="Slack Bot API")

# Slack configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")


# Create simple Slack bot agent
slack_agent = Agent(
    system_prompt="""You are a friendly and helpful Slack bot assistant.

When responding:
- Be concise and conversational
- Use Slack-friendly formatting with markdown
- Be helpful and answer questions directly
- Keep responses short and to the point

You can help with:
- Answering general questions
- Providing information and assistance
- Having friendly conversations
"""
)


def send_slack_message(channel: str, text: str):
    """Send a message to Slack channel."""
    if not SLACK_BOT_TOKEN:
        print(f"Would send to Slack channel {channel}: {text}")
        return

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "channel": channel,
        "text": text
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"✓ Sent to Slack channel {channel}")
    except Exception as e:
        print(f"Error sending Slack message: {e}")


@app.post("/slack/events")
async def slack_events(request: Request):
    """Handle Slack events (messages, mentions, etc.)."""
    try:
        body = await request.json()

        # Handle URL verification challenge
        if body.get("type") == "url_verification":
            return JSONResponse({"challenge": body.get("challenge")})

        # Handle app mentions and messages
        if body.get("type") == "event_callback":
            event = body.get("event", {})

            # Ignore bot messages to prevent loops
            if event.get("bot_id"):
                return JSONResponse({"ok": True})

            # Process message
            if event.get("type") == "app_mention" or event.get("type") == "message":
                user_message = event.get("text", "")
                channel = event.get("channel")

                # Remove bot mention from message
                user_message = user_message.replace(f"<@{event.get('bot_id')}>", "").strip()

                # Get agent response
                response = slack_agent(user_message)

                # Send response back to Slack
                send_slack_message(channel, response)

        return JSONResponse({"ok": True})

    except Exception as e:
        print(f"Error processing Slack event: {e}")
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


@app.post("/slack/commands")
async def slack_commands(request: Request):
    """Handle Slack slash commands."""
    try:
        form_data = await request.form()
        command = form_data.get("command")
        text = form_data.get("text", "")
        user_id = form_data.get("user_id")

        # Process command
        if command == "/agent":
            response = slack_agent(text)
            return JSONResponse({
                "response_type": "in_channel",
                "text": response
            })

        return JSONResponse({
            "response_type": "ephemeral",
            "text": f"Unknown command: {command}"
        })

    except Exception as e:
        return JSONResponse({
            "response_type": "ephemeral",
            "text": f"Error: {str(e)}"
        }, status_code=500)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "bot": "slack-agent"}


def main():
    """Run the Slack bot server."""
    print("=" * 70)
    print("💬 Simple Slack Bot Demo")
    print("=" * 70)
    print()

    if not SLACK_BOT_TOKEN:
        print("⚠️  SLACK_BOT_TOKEN not found in environment variables")
        print("\nTo set up a real Slack bot:")
        print("1. Go to https://api.slack.com/apps")
        print("2. Create a new app")
        print("3. Add Bot Token Scopes: chat:write, app_mentions:read")
        print("4. Install app to workspace")
        print("5. Copy Bot User OAuth Token to .env as SLACK_BOT_TOKEN")
        print("6. Set up Event Subscriptions: {your_url}/slack/events")
        print("7. Subscribe to: app_mention")
        print("\nRunning in demo mode...\n")

    # Demo interactions
    print("Demo: Simulating Slack conversations\n")

    demo_messages = [
        "Hello!",
        "What can you help me with?",
        "Tell me a joke",
        "What's the weather like today?",
    ]

    for msg in demo_messages:
        print(f"\n{'='*70}")
        print(f"User: {msg}")
        print(f"{'='*70}")
        response = slack_agent(msg)
        print(f"\nBot: {response}\n")

    print("=" * 70)
    print("✨ Demo complete!")
    print("\nTo run the actual server:")
    print("  python 16_slack_bot.py --server")
    print("\nOr use:")
    print("  uvicorn 16_slack_bot:app --reload --port 8000")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    if "--server" in sys.argv:
        print("🚀 Starting Slack Bot Server...")
        print("📱 Webhook URL: http://localhost:8000/slack/events")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        main()


"""
Setup Instructions:

1. Install required packages:
   uv add fastapi uvicorn python-dotenv requests

2. Create a Slack App:
   - Go to https://api.slack.com/apps
   - Click "Create New App" → "From scratch"
   - Name it and select your workspace

3. Configure Bot:
   - OAuth & Permissions → Add scopes:
     - chat:write
     - app_mentions:read
   - Install app to workspace
   - Copy "Bot User OAuth Token"

4. Set up environment variables in .env:
   SLACK_BOT_TOKEN=xoxb-your-token-here

5. Set up ngrok for local development:
   ngrok http 8000

6. Configure Slack Event Subscriptions:
   - Enable Events: ON
   - Request URL: https://your-ngrok-url.ngrok.io/slack/events
   - Subscribe to events: app_mention

7. Run the server:
   python 16_slack_bot.py --server

Features Demonstrated:
- Simple Slack bot responses
- Direct message handling
- App mentions
- Basic conversation

Use Cases:
- Simple Q&A bot
- Customer support assistant
- Team helper
- Information bot

Production Considerations:
- Add rate limiting
- Store conversation context
- Add error handling
- Implement logging
- Add monitoring
"""
