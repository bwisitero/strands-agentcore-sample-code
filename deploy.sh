#!/bin/bash
# Deployment script for agentcore_deployment
#
# This script helps deploy the agent with the correct AWS credentials
# The agent is configured for AWS account 313806797257

echo "🚀 Deploying agentcore_deployment to AWS account 313806797257"
echo ""
echo "⚠️  Make sure you have AWS credentials configured for account 313806797257"
echo ""
echo "Choose deployment mode:"
echo "1) CodeBuild (cloud build - recommended)"
echo "2) Local build + cloud deploy"
echo ""
read -p "Enter choice [1-2]: " choice

case $choice in
  1)
    echo "Launching with CodeBuild..."
    uv run agentcore launch
    ;;
  2)
    echo "Launching with local build..."
    uv run agentcore launch --local-build
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Test with:"
echo "  uv run agentcore invoke '{\"prompt\": \"Hello\"}'"
