"""
Demo 5: Deploying to AgentCore (10 min)
Goal: Show production deployment

Key Teaching Points:
- Wrapping agents for AgentCore deployment
- Using BedrockAgentCoreApp for production
- AgentCore benefits: scaling, observability, security, session memory

Deployment command (show in terminal):
agentcore deploy --name customer-service-agent
"""

from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands_tools import calculator

@tool
def get_product_info(product_id: str) -> dict:
    """Retrieve product information from database."""
    # Simulated database lookup
    products = {
        "101": {"name": "Laptop", "price": 999, "stock": 50},
        "102": {"name": "Mouse", "price": 29, "stock": 200}
    }
    return products.get(product_id, {"error": "Product not found"})

# Create the agent
agent = Agent(
    tools=[calculator, get_product_info],
    system_prompt="You are a helpful customer service agent."
)

# Wrap with AgentCore for deployment
app = BedrockAgentCoreApp()

@app.route()
def agent_handler(prompt):
    return agent(prompt)

# AgentCore provides:
# - Automatic scaling
# - Built-in observability (CloudWatch)
# - Secure identity management
# - Session memory persistence
