"""
Demo 3: MCP Server Integration (7 min)
Goal: Show how to use thousands of pre-built tools

Key Teaching Points:
- How to connect to MCP servers
- Using AWS documentation MCP server as example
- Accessing external tool ecosystems
"""

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# Connect to AWS documentation MCP server
aws_docs_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

with aws_docs_client:
    agent = Agent(tools=aws_docs_client.list_tools_sync())
    response = agent("How do I set up DynamoDB with Python?")
    print(response)
