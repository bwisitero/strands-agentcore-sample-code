"""
Demo 1: Hello Agent (5 min)
Goal: Get everyone's first agent running

Key Teaching Points:
- Default uses Bedrock Claude 4 Sonnet
- Model-driven approach - no complex workflow needed
"""

from strands import Agent

# Simplest possible agent
agent = Agent()
response = agent("What are the key considerations for building a chatbot?")
print(response)
