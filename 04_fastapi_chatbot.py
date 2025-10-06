"""
Demo 12: FastAPI Web Chatbot
Goal: Build a web-based chatbot UI with FastAPI backend

Key Teaching Points:
- Connecting Strands agents to a web frontend
- FastAPI for REST API endpoints
- HTML/JavaScript chat interface
- Session management for conversation history
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from strands import Agent
from pydantic import BaseModel
import uvicorn
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(title="Strands Chatbot API")

# Initialize agent
agent = Agent(
    system_prompt="You are a helpful and friendly AI assistant. Be concise but informative."
)

# Store conversation sessions (in production, use a database)
sessions = {}


class ChatMessage(BaseModel):
    message: str
    session_id: str = "default"


@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    """Serve the chat interface HTML page."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Strands AI Chatbot</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }

            .chat-container {
                background: white;
                border-radius: 16px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 800px;
                height: 600px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }

            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }

            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            .message {
                display: flex;
                gap: 10px;
                animation: fadeIn 0.3s;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .message.user {
                justify-content: flex-end;
            }

            .message-content {
                max-width: 70%;
                padding: 12px 16px;
                border-radius: 18px;
                word-wrap: break-word;
            }

            .message.user .message-content {
                background: #667eea;
                color: white;
            }

            .message.assistant .message-content {
                background: #f1f3f4;
                color: #333;
            }

            .chat-input-container {
                padding: 20px;
                border-top: 1px solid #e0e0e0;
                display: flex;
                gap: 10px;
            }

            #messageInput {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 24px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }

            #messageInput:focus {
                border-color: #667eea;
            }

            #sendButton {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 24px;
                font-size: 16px;
                cursor: pointer;
                transition: transform 0.2s;
            }

            #sendButton:hover {
                transform: scale(1.05);
            }

            #sendButton:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }

            .typing-indicator {
                display: none;
                padding: 12px 16px;
                background: #f1f3f4;
                border-radius: 18px;
                width: 60px;
                margin-left: 20px;
            }

            .typing-indicator.show {
                display: flex;
                align-items: center;
            }

            .typing-indicator span {
                height: 8px;
                width: 8px;
                background: #999;
                border-radius: 50%;
                display: inline-block;
                margin: 0 2px;
                animation: typing 1.4s infinite;
            }

            .typing-indicator span:nth-child(2) {
                animation-delay: 0.2s;
            }

            .typing-indicator span:nth-child(3) {
                animation-delay: 0.4s;
            }

            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                🤖 Strands AI Assistant
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message assistant">
                    <div class="message-content">
                        Hello! I'm your AI assistant. How can I help you today?
                    </div>
                </div>
                <div class="typing-indicator" id="typingIndicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            <div class="chat-input-container">
                <input
                    type="text"
                    id="messageInput"
                    placeholder="Type your message..."
                    autocomplete="off"
                >
                <button id="sendButton">Send</button>
            </div>
        </div>

        <script>
            const chatMessages = document.getElementById('chatMessages');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const typingIndicator = document.getElementById('typingIndicator');
            const sessionId = 'session_' + Date.now();

            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }

            function addMessage(content, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
                const escapedContent = escapeHtml(content);
                messageDiv.innerHTML = `
                    <div class="message-content">${escapedContent}</div>
                `;
                // Insert before typing indicator
                chatMessages.insertBefore(messageDiv, typingIndicator);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;

                // Add user message to chat immediately
                addMessage(message, true);

                // Clear input and disable button
                messageInput.value = '';
                sendButton.disabled = true;
                typingIndicator.classList.add('show');

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            session_id: sessionId
                        })
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();

                    console.log('Received data:', data);

                    // Check if response exists and is not undefined
                    if (data && data.response !== undefined && data.response !== null) {
                        addMessage(data.response, false);
                    } else if (data && data.error) {
                        addMessage(`Error: ${data.error}`, false);
                    } else {
                        addMessage('Sorry, I received an empty response. Please try again.', false);
                    }
                } catch (error) {
                    addMessage('Sorry, I encountered an error. Please try again.', false);
                    console.error('Error:', error);
                } finally {
                    typingIndicator.classList.remove('show');
                    sendButton.disabled = false;
                    messageInput.focus();
                }
            }

            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Focus input on load
            messageInput.focus();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    """Handle chat messages and return agent responses."""
    try:
        # Get or create session
        session_id = chat_message.session_id
        if session_id not in sessions:
            sessions[session_id] = {
                "agent": Agent(
                    system_prompt="You are a helpful and friendly AI assistant. Be concise but informative."
                ),
                "created_at": datetime.now()
            }

        # Get response from agent (maintains conversation history automatically)
        session_agent = sessions[session_id]["agent"]
        response = session_agent(chat_message.message)

        # Ensure response is a string
        response_text = str(response) if response is not None else "I apologize, but I couldn't generate a response."

        return JSONResponse({
            "response": response_text,
            "session_id": session_id
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")  # Server-side logging
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "active_sessions": len(sessions)}


if __name__ == "__main__":
    print("🚀 Starting Strands Chatbot Server...")
    print("📱 Open http://localhost:8000 in your browser")
    print("⏹️  Press Ctrl+C to stop")

    uvicorn.run(app, host="0.0.0.0", port=8000)


"""
Setup Instructions:

1. Install required packages:
   uv add fastapi uvicorn python-multipart

2. Run the server:
   python demo_12_fastapi_chatbot.py

3. Open your browser:
   http://localhost:8000

4. Start chatting with the AI!

Features:
- Clean, modern chat interface
- Real-time messaging
- Session-based conversation history
- Typing indicators
- Responsive design
- Automatic scrolling

API Endpoints:
- GET /: Chat interface (HTML page)
- POST /chat: Send message and get response
- GET /health: Health check

Production Considerations:
- Use proper session storage (Redis, database)
- Add authentication and rate limiting
- Implement WebSocket for real-time updates
- Add error handling and logging
- Deploy with production ASGI server (Gunicorn + Uvicorn)
"""
