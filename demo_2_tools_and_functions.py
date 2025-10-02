"""
Demo 2: Adding Tools & Custom Functions (8 min)
Goal: Show how to extend agents with capabilities

Key Teaching Points:
- How to create custom tools with @tool decorator
- How to use pre-built tools from strands_tools
- How to combine multiple tools in a single agent
"""

from strands import Agent, tool
from strands_tools import calculator, current_time, web_search

@tool
def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of input text."""
    # Simple sentiment logic for demo
    positive_words = ['good', 'great', 'excellent', 'amazing']
    negative_words = ['bad', 'poor', 'terrible', 'awful']

    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    if pos_count > neg_count:
        return "Positive sentiment"
    elif neg_count > pos_count:
        return "Negative sentiment"
    else:
        return "Neutral sentiment"

# Create agent with multiple tools
agent = Agent(
    tools=[calculator, current_time, web_search, analyze_sentiment],
    system_prompt="You are a helpful assistant that can analyze data and search the web."
)

# Demo the tools in action
response = agent("""
1. What's the current time?
2. Calculate the compound interest on $10,000 at 5% for 3 years
3. Analyze the sentiment of: "This hackathon is going to be amazing!"
4. Search for the latest news about AI agents
""")

print(response)
