"""
Demo 4: Multi-Agent System (10 min)
Goal: Build a research + writer agent team

Key Teaching Points:
- Creating specialist agents for different tasks
- Converting agents to tools for orchestration
- Coordinating multiple agents with an orchestrator
"""

from strands import Agent, tool
from strands_tools import web_search, retrieve

# Specialist Agent 1: Research Agent
research_agent = Agent(
    tools=[web_search, retrieve],
    system_prompt="""You are a research specialist.
    Your job is to find accurate, up-to-date information."""
)

# Specialist Agent 2: Content Writer
writer_agent = Agent(
    system_prompt="""You are a technical writer.
    Create clear, engaging content based on research provided."""
)

# Convert specialist agents to tools
@tool
def research_assistant(query: str) -> str:
    """Research agent that finds information."""
    return research_agent(query)

@tool
def writing_assistant(content: str, style: str = "technical") -> str:
    """Writing agent that creates content."""
    prompt = f"Write in {style} style about: {content}"
    return writer_agent(prompt)

# Orchestrator agent
orchestrator = Agent(
    tools=[research_assistant, writing_assistant],
    system_prompt="""You coordinate research and writing tasks.
    First research, then create content based on findings."""
)

# Demo the multi-agent system
result = orchestrator(
    "Create a technical blog post about the latest advances in RAG systems"
)

print(result)
