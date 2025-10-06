"""
Demo: Deploying Strands Agents to AWS with AgentCore

This demo shows how to deploy a Strands agent to production using AWS Bedrock AgentCore.
AgentCore provides: auto-scaling, observability, session memory, and managed infrastructure.

SETUP & DEPLOYMENT:

1. Prerequisites:
   - AWS account with Bedrock AgentCore access
   - AWS credentials configured (aws configure)
   - Docker installed (for local builds)
   - Permissions: AgentCore, ECR, IAM, CodeBuild

2. Configure Your Agent:
   $ uv run agentcore configure --entrypoint agentcore_deployment.py

   This creates .bedrock_agentcore.yaml with your agent configuration.

3. Deploy to AWS:

   Option A - CodeBuild (cloud build, no local Docker needed):
   $ uv run agentcore launch

   Option B - Local build (faster iteration, requires Docker):
   $ uv run agentcore launch --local-build

   The deployment will:
   - Build ARM64 container (locally or in CodeBuild)
   - Push to ECR repository
   - Create/update AgentCore runtime
   - Configure CloudWatch logging and X-Ray tracing
   - Set up session memory persistence

4. Invoke Your Deployed Agent:

   Basic invocation:
   $ uv run agentcore invoke '{"prompt": "Hello"}'

   With session memory (maintains conversation context):
   $ uv run agentcore invoke '{"prompt": "What did I just ask?"}'

   Check deployment status:
   $ uv run agentcore status

   View logs:
   $ aws logs tail /aws/bedrock-agentcore/runtimes/<agent-name> --follow

KEY IMPLEMENTATION DETAILS:

- Use @app.entrypoint decorator (not @app.route)
- Handler receives dict event with "prompt" key
- Call app.run() when DOCKER_CONTAINER env var is set
- Agent tools work seamlessly in AgentCore

TROUBLESHOOTING:

- "No entrypoint defined": Use @app.entrypoint, not @app.route
- "Cross-account pass role": Check AWS_PROFILE matches AgentCore account
- Build failures: Check pyproject.toml excludes data directories
- Permission errors in Docker: Ensure chown before USER switch
"""

from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands_tools import calculator
# uv add bedrock-agentcore

@tool
def get_product_info(product_id: str) -> dict:
    """Retrieve product information from database."""
    # Simulated database lookup
    products = {
        "101": {"name": "Laptop", "price": 999, "stock": 50},
        "102": {"name": "Mouse", "price": 29, "stock": 200}
    }
    return products.get(product_id, {"error": "Product not found"})

# Create the agent (same as any Strands agent)
agent = Agent(
    tools=[calculator, get_product_info],
    system_prompt="You are a helpful customer service agent."
)

# ============================================================================
# AGENTCORE DEPLOYMENT WRAPPER
# ============================================================================
# Wrap the agent with BedrockAgentCoreApp to enable cloud deployment.
# The agent code above stays the same - AgentCore just provides the runtime.
app = BedrockAgentCoreApp()

@app.entrypoint  # IMPORTANT: Use @app.entrypoint, not @app.route
def agent_handler(event):
    """
    AgentCore entrypoint handler.

    Args:
        event: Dict with structure {"prompt": "user message", ...}

    Returns:
        Agent response string
    """
    # Extract prompt from the event dictionary
    prompt = event.get("prompt") if isinstance(event, dict) else str(event)
    return agent(prompt)

# AgentCore provides:
# - Automatic scaling based on load
# - Built-in observability (CloudWatch Logs + X-Ray)
# - Secure identity management (IAM roles)
# - Session memory persistence across invocations

# Test the agent locally or start the server
if __name__ == "__main__":
    import sys
    import os

    # If running in Docker, start the AgentCore server
    if os.getenv("DOCKER_CONTAINER"):
        app.run()
    else:
        # Local testing mode
        print("Testing agent locally before deployment...\n")

        # Test 1: Product lookup
        response = agent("What is the price of product 101?")
        print(f"Test 1 - Product Query:\n{response}\n")

        # Test 2: Calculation with tool
        response = agent("If I buy 3 units of product 102, what's the total cost?")
        print(f"Test 2 - Calculation:\n{response}\n")

        print("✅ Local testing complete!")
        print("\nNext steps for AWS deployment:")
        print("1. Configure: uv run agentcore configure --entrypoint agentcore_deployment.py")
        print("2. Deploy: uv run agentcore launch --local-build")
        print("3. Test: uv run agentcore invoke '{\"prompt\": \"What is product 101?\"}'")

"""
SAMPLE OUTPUT - Successful Deployment:

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run agentcore launch --local-build
🔧 Launching Bedrock AgentCore (local-build mode - NEW!)...
   • Build container locally with Docker
   • Deploy to Bedrock AgentCore cloud runtime
   • Requires Docker/Finch/Podman to be installed
   • Use when you need custom build control

Using existing memory: agentcore_deployment_mem-x1iBrUA1NY
Launching Bedrock AgentCore agent 'agentcore_deployment' to cloud
⠸ Launching Bedrock AgentCore...Docker image built: bedrock_agentcore-agentcore_deployment:latest
Using execution role from config: arn:aws:iam::313806797257:role/AmazonBedrockAgentCoreSDKRuntime-us-east-1-992f8f5be7
Uploading to ECR...
Using ECR repository from config: 313806797257.dkr.ecr.us-east-1.amazonaws.com/bedrock-agentcore-agentcore_deployment
⠦ Launching Bedrock AgentCore...Authenticating with registry...
⠦ Launching Bedrock AgentCore...Registry authentication successful
Tagging image: bedrock_agentcore-agentcore_deployment:latest -> 313806797257.dkr.ecr.us-east-1.amazonaws.com/bedrock-agentcore-agentcore_deployment:latest
⠧ Launching Bedrock AgentCore...Pushing image to registry...
The push refers to repository [313806797257.dkr.ecr.us-east-1.amazonaws.com/bedrock-agentcore-agentcore_deployment]
c3ba96bb1073: Pushed 
ec73bc00df10: Pushed 
8b198bbb2fc1: Layer already exists 
f4e51325a7cb: Layer already exists 
800a845e09ad: Layer already exists 
a185a56c0223: Layer already exists 
20c9124ae81d: Pushed 
c69a60b7da69: Pushed 
53865f2fb3d4: Layer already exists 
f8ccd48d7228: Layer already exists 
b878f4b3193f: Pushed 
⠸ Launching Bedrock AgentCore...latest: digest: sha256:0ba941f00d6299625a889ca31c13b266e0e29434aa2c3d7a2ff96f8adfc028e2 size: 856
Image pushed successfully
Image uploaded to ECR: 313806797257.dkr.ecr.us-east-1.amazonaws.com/bedrock-agentcore-agentcore_deployment
Deploying to Bedrock AgentCore...
Passing memory configuration to agent: agentcore_deployment_mem-x1iBrUA1NY
⠇ Launching Bedrock AgentCore...⚠️ Session ID will be reset to connect to the updated agent. The previous agent remains accessible via the original session ID: 7f2ccd69-6be6-465d-ac22-da3e41f66c7a
✅ Agent created/updated: arn:aws:bedrock-agentcore:us-east-1:313806797257:runtime/agentcore_deployment-hQDE9gD1Pp
Observability is enabled, configuring Transaction Search...
⠼ Launching Bedrock AgentCore...CloudWatch Logs resource policy already configured
⠇ Launching Bedrock AgentCore...X-Ray trace destination already configured
⠋ Launching Bedrock AgentCore...X-Ray indexing rule already configured
✅ Transaction Search already fully configured
🔍 GenAI Observability Dashboard:
   https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#gen-ai-observability/agent-core
Polling for endpoint to be ready...
⠸ Launching Bedrock AgentCore...Agent endpoint: arn:aws:bedrock-agentcore:us-east-1:313806797257:runtime/agentcore_deployment-hQDE9gD1Pp/runtime-endpoint/DEFAULT
╭────────────────────────────────────────────────────────────────── Local Build Success ───────────────────────────────────────────────────────────────────╮
│ ✅ Local Build Deployment Successful!                                                                                                                    │
│                                                                                                                                                          │
│ Agent Details:                                                                                                                                           │
│ Agent Name: agentcore_deployment                                                                                                                         │
│ Agent ARN: arn:aws:bedrock-agentcore:us-east-1:313806797257:runtime/agentcore_deployment-hQDE9gD1Pp                                                      │
│ ECR URI: 313806797257.dkr.ecr.us-east-1.amazonaws.com/bedrock-agentcore-agentcore_deployment                                                             │
│                                                                                                                                                          │
│ 🔧 Container deployed to Bedrock AgentCore                                                                                                               │
│                                                                                                                                                          │
│ Next Steps:                                                                                                                                              │
│    agentcore status                                                                                                                                      │
│    agentcore invoke '{"prompt": "Hello"}'                                                                                                                │
│                                                                                                                                                          │
│ 📋 CloudWatch Logs:                                                                                                                                      │
│    /aws/bedrock-agentcore/runtimes/agentcore_deployment-hQDE9gD1Pp-DEFAULT --log-stream-name-prefix "2025/10/06/[runtime-logs]"                          │
│    /aws/bedrock-agentcore/runtimes/agentcore_deployment-hQDE9gD1Pp-DEFAULT --log-stream-names "otel-rt-logs"                                             │
│                                                                                                                                                          │
│ 💡 Tail logs with:                                                                                                                                       │
│    aws logs tail /aws/bedrock-agentcore/runtimes/agentcore_deployment-hQDE9gD1Pp-DEFAULT --log-stream-name-prefix "2025/10/06/[runtime-logs]" --follow   │
│    aws logs tail /aws/bedrock-agentcore/runtimes/agentcore_deployment-hQDE9gD1Pp-DEFAULT --log-stream-name-prefix "2025/10/06/[runtime-logs]" --since 1h │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run agentcore invoke '{"prompt": "Hello"}'
╭────────────────────────────────────────────────────────────────── agentcore_deployment ──────────────────────────────────────────────────────────────────╮
│ Session: 737486e6-e959-49c3-8840-6a60a16609b8                                                                                                            │
│ Request ID: fcfe06e5-81aa-4d68-8998-a20f70b8001d                                                                                                         │
│ ARN: arn:aws:bedrock-agentcore:us-east-1:313806797257:runtime/agentcore_deployment-hQDE9gD1Pp                                                            │
│ Logs: aws logs tail /aws/bedrock-agentcore/runtimes/agentcore_deployment-hQDE9gD1Pp-DEFAULT --log-stream-name-prefix "2025/10/06/[runtime-logs]"         │
│ --follow                                                                                                                                                 │
│       aws logs tail /aws/bedrock-agentcore/runtimes/agentcore_deployment-hQDE9gD1Pp-DEFAULT --log-stream-name-prefix "2025/10/06/[runtime-logs]" --since │
│ 1h                                                                                                                                                       │
│ GenAI Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#gen-ai-observability/agent-core                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Response:
Hello! I'm here to help you as a customer service agent. How can I assist you today? 

I can help you with:
- Looking up product information using product IDs
- Performing mathematical calculations if you need any computations
- Answering questions or resolving any issues you might have

What would you like help with?

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run agentcore invoke '{"prompt": "What is the price of product 101?"}'
╭────────────────────────────────────────────────────────────────── agentcore_deployment ──────────────────────────────────────────────────────────────────╮
│ Session: 737486e6-e959-49c3-8840-6a60a16609b8                                                                                                            │
│ Request ID: ba6b4f81-6533-4342-9bff-78ee0741ef75                                                                                                         │
│ ARN: arn:aws:bedrock-agentcore:us-east-1:313806797257:runtime/agentcore_deployment-hQDE9gD1Pp                                                            │
│ Logs: aws logs tail /aws/bedrock-agentcore/runtimes/agentcore_deployment-hQDE9gD1Pp-DEFAULT --log-stream-name-prefix "2025/10/06/[runtime-logs]"         │
│ --follow                                                                                                                                                 │
│       aws logs tail /aws/bedrock-agentcore/runtimes/agentcore_deployment-hQDE9gD1Pp-DEFAULT --log-stream-name-prefix "2025/10/06/[runtime-logs]" --since │
│ 1h                                                                                                                                                       │
│ GenAI Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#gen-ai-observability/agent-core                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Response:
The price of product 101 (Laptop) is $999. We currently have 50 units in stock. Is there anything else you'd like to know about this product?

emil@Franklins-MacBook-Pro strands-agentcore-demo % 
"""