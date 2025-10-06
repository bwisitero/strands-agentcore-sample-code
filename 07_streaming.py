"""
Demo 6: Advanced - Streaming & Real-time (5 min)
Goal: Show streaming responses for better UX

Key Teaching Points:
- Using async streaming for real-time responses
- Event types: text and tool_use
- Better user experience with progressive output
"""

from strands import Agent
import asyncio

agent = Agent()

async def stream_demo():
    """Stream responses in real-time"""
    async for event in agent.stream_async(
        "Write a 3-step plan for building an AI startup"
    ):
        if event.get("type") == "text":
            print(event.get("content", ""), end="", flush=True)
        elif event.get("type") == "tool_use":
            print(f"\n[Using tool: {event.get('tool_name')}]")

# Run the streaming demo
if __name__ == "__main__":
    asyncio.run(stream_demo())
