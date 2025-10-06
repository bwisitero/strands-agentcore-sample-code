"""
Demo 10: Using Different Bedrock Models
Goal: Show how to configure and switch between different Bedrock models

Key Teaching Points:
- Default uses Claude 4 Sonnet, but you can customize
- How to specify different Bedrock models
- Comparing model responses for different use cases
- Model configuration options
"""

from strands import Agent

# Example 1: Using Claude 4 Sonnet (default)
print("=== Example 1: Claude 4 Sonnet (Default) ===")
agent_sonnet = Agent()
response = agent_sonnet("Explain quantum computing in one sentence.")
print(f"Response: {response}\n")


# Example 2: Using Claude 3.5 Sonnet
print("=== Example 2: Claude 3.5 Sonnet ===")
agent_claude_35 = Agent(
    model="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
)
response = agent_claude_35("Explain quantum computing in one sentence.")
print(f"Response: {response}\n")


# Example 3: Using Claude 3 Haiku (faster, cheaper)
print("=== Example 3: Claude 3 Haiku (Fast & Cost-Efficient) ===")
agent_haiku = Agent(
    model="us.anthropic.claude-3-haiku-20240307-v1:0"
)
response = agent_haiku("Explain quantum computing in one sentence.")
print(f"Response: {response}\n")


# Example 4: Using Claude 3 Opus (most capable)
print("=== Example 4: Claude 3 Opus (Most Capable) ===")
agent_opus = Agent(
    model="us.anthropic.claude-3-opus-20240229-v1:0"
)
response = agent_opus("Explain quantum computing in one sentence.")
print(f"Response: {response}\n")


# Example 5: Model with custom configuration
print("=== Example 5: Custom Model Configuration ===")
from strands.models import BedrockModel

custom_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature=0.7,  # Control randomness (0-1)
    max_tokens=500,   # Limit response length
    top_p=0.9        # Control diversity
)

agent_custom = Agent(
    model=custom_model,
    system_prompt="You are a concise technical expert."
)
response = agent_custom("Explain quantum computing.")
print(f"Response: {response}\n")


"""
Available Bedrock Models (as of Oct 2025):

Claude Models:
- anthropic.claude-4-sonnet-20250514-v1:0 (Default - Latest, most capable)
- anthropic.claude-3-5-sonnet-20241022-v2:0 (Previous generation)
- anthropic.claude-3-opus-20240229-v1:0 (Most capable Claude 3)
- anthropic.claude-3-sonnet-20240229-v1:0 (Balanced Claude 3)
- anthropic.claude-3-haiku-20240307-v1:0 (Fastest, most cost-efficient)

Other Models (if available in your region):
- amazon.titan-text-express-v1
- amazon.titan-text-lite-v1
- ai21.j2-ultra-v1
- meta.llama3-70b-instruct-v1:0
- cohere.command-text-v14

Model Selection Guide:
- Claude 4 Sonnet: Best for complex reasoning, coding, and analysis (Default)
- Claude 3.5 Sonnet: Great balance of capability and cost
- Claude 3 Opus: Maximum capability for hardest tasks
- Claude 3 Haiku: Fast responses, lower cost, simpler tasks

Model Configuration Parameters:
- temperature: Controls randomness (0=deterministic, 1=creative)
- max_tokens: Maximum response length
- top_p: Nucleus sampling threshold
- top_k: Limits token selection pool

Note: Ensure you have access to these models in your AWS account.
Check AWS Bedrock console > Model access to enable models.
"""

'''
Sample output:

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run demo_10_custom_models.py
=== Example 1: Claude 4 Sonnet (Default) ===
Quantum computing harnesses the bizarre properties of quantum mechanics—like superposition (being in multiple states simultaneously) and entanglement (instant connection between particles)—to process information in fundamentally different ways than classical computers, potentially solving certain complex problems exponentially faster.Response: Quantum computing harnesses the bizarre properties of quantum mechanics—like superposition (being in multiple states simultaneously) and entanglement (instant connection between particles)—to process information in fundamentally different ways than classical computers, potentially solving certain complex problems exponentially faster.


=== Example 2: Claude 3.5 Sonnet ===
Quantum computing harnesses the principles of quantum mechanics (like superposition and entanglement) to perform certain calculations exponentially faster than classical computers by using quantum bits that can exist in multiple states simultaneously.Response: Quantum computing harnesses the principles of quantum mechanics (like superposition and entanglement) to perform certain calculations exponentially faster than classical computers by using quantum bits that can exist in multiple states simultaneously.


=== Example 3: Claude 3 Haiku (Fast & Cost-Efficient) ===
Quantum computing leverages the principles of quantum mechanics, such as superposition and entanglement, to perform computations in a fundamentally different way from traditional, classical computers, potentially enabling the solving of certain complex problems much faster than classical computers.Response: Quantum computing leverages the principles of quantum mechanics, such as superposition and entanglement, to perform computations in a fundamentally different way from traditional, classical computers, potentially enabling the solving of certain complex problems much faster than classical computers.


=== Example 4: Claude 3 Opus (Most Capable) ===
Quantum computing is a type of computing that uses quantum-mechanical phenomena, such as superposition and entanglement, to perform operations on data in ways that are fundamentally different from classical computers.Response: Quantum computing is a type of computing that uses quantum-mechanical phenomena, such as superposition and entanglement, to perform operations on data in ways that are fundamentally different from classical computers.


=== Example 5: Custom Model Configuration ===
Quantum computing uses quantum bits (qubits) that exist in multiple states simultaneously through superposition, unlike classical binary bits. This allows parallel processing of vast calculations. Qubits are linked through quantum entanglement, enabling complex operations. However, qubits are highly sensitive to interference and require extreme cooling. Current applications include cryptography, optimization, and molecular simulation. The field remains experimental with limited practical use.Response: Quantum computing uses quantum bits (qubits) that exist in multiple states simultaneously through superposition, unlike classical binary bits. This allows parallel processing of vast calculations. Qubits are linked through quantum entanglement, enabling complex operations. However, qubits are highly sensitive to interference and require extreme cooling. Current applications include cryptography, optimization, and molecular simulation. The field remains experimental with limited practical use.
'''