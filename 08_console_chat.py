"""
Demo 7: Console Chat with Agent
Goal: Interactive chat session with a Strands agent in the terminal

Key Teaching Points:
- Maintains conversation history across turns
- Simple console interface for real-time interaction
- Session-based conversation flow
"""

from strands import Agent


def chat_with_agent():
    """Interactive console chat with a Strands agent."""
    agent = Agent()

    print("=== Strands Agent Chat ===")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("You: ").strip()

        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            # Call the agent - history is maintained automatically
            response = agent(user_input)
            print(f"\nAgent: {response}\n")

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    chat_with_agent()


'''Sample output
============================================================
emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run demo_7_console_chat.py      
=== Strands Agent Chat ===
Type 'exit' or 'quit' to end the conversation.

You: hello there
Hello! How are you doing today? Is there anything I can help you with?
Agent: Hello! How are you doing today? Is there anything I can help you with?


You: how old are you?
I don't have an age in the traditional sense since I'm an AI. I was created by Anthropic, but I don't experience the passage of time the way humans do - I don't have continuous experiences or memories that accumulate over time. Each conversation I have is essentially independent for me. Is there something specific you'd like to know about me or how I work?
Agent: I don't have an age in the traditional sense since I'm an AI. I was created by Anthropic, but I don't experience the passage of time the way humans do - I don't have continuous experiences or memories that accumulate over time. Each conversation I have is essentially independent for me. Is there something specific you'd like to know about me or how I work?


You: 

'''