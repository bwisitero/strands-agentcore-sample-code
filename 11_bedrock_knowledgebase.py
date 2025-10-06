"""
Demo 9: Bedrock Knowledge Base Integration
Goal: Connect agents to AWS Bedrock Knowledge Bases for production RAG

Key Teaching Points:
- Using AWS Bedrock Knowledge Bases for enterprise RAG
- Integration with S3-backed knowledge bases
- Combining multiple knowledge bases with agents
"""

import os
from dotenv import load_dotenv
from strands import Agent
from strands.knowledge_bases import BedrockKnowledgeBase

# Load environment variables
load_dotenv()

# Connect to an existing Bedrock Knowledge Base
# Prerequisites:
# 1. Create a Knowledge Base in AWS Bedrock console
# 2. Upload documents to S3 bucket associated with the KB
# 3. Note the Knowledge Base ID from the console

# Example: Create agent with Bedrock Knowledge Base
kb = BedrockKnowledgeBase(
    knowledge_base_id="YOUR_KB_ID_HERE",  # Replace with your KB ID from AWS console
    region_name="us-east-1"  # Adjust to your region
)

# Create agent with the knowledge base
agent = Agent(
    knowledge_bases=[kb],
    system_prompt="""You are a knowledgeable assistant with access to company documentation.
    Always cite sources from the knowledge base when answering questions.
    If information is not available in the knowledge base, clearly state that."""
)

# Example queries
if __name__ == "__main__":
    # Test query
    response = agent("What is our company's refund policy?")
    print(f"Response: {response}\n")

    # Follow-up query (maintains context)
    response = agent("How long does the refund process take?")
    print(f"Follow-up: {response}\n")


"""
Setup Instructions:

1. Create a Bedrock Knowledge Base:
   - Go to AWS Console > Bedrock > Knowledge bases
   - Click "Create knowledge base"
   - Configure S3 data source with your documents
   - Choose embeddings model (e.g., Titan Embeddings)
   - Create vector store (OpenSearch Serverless or other)
   - Note the Knowledge Base ID

2. Set up AWS credentials:
   - Ensure AWS credentials are configured (~/.aws/credentials)
   - Or set environment variables:
     export AWS_ACCESS_KEY_ID="your-key"
     export AWS_SECRET_ACCESS_KEY="your-secret"
     export AWS_DEFAULT_REGION="us-east-1"

3. Update the knowledge_base_id in this script

4. Run the demo:
   python demo_9_bedrock_knowledgebase.py

Benefits of Bedrock Knowledge Bases:
- Managed vector database (no infrastructure to maintain)
- Automatic document chunking and embedding
- Supports multiple data sources (S3, web crawlers, etc.)
- Built-in security and access control
- Scales automatically with usage
- Integrated with other AWS services
"""
