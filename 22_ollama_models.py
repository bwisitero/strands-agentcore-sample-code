"""
Demo 11: Using Ollama Models (Local LLMs)
Goal: Show how to use local Ollama models instead of Bedrock

Key Teaching Points:
- Running agents with local Ollama models
- Benefits: Privacy, no API costs, offline capability
- Easy switching between cloud and local models
"""

from strands import Agent

# Example 1: Using Ollama with Llama 3
print("=== Example 1: Ollama Llama 3 ===")
agent_llama = Agent(
    model="ollama/llama3",
    model_kwargs={
        "base_url": "http://localhost:11434"  # Default Ollama URL
    }
)
response = agent_llama("What are the benefits of using local LLMs?")
print(f"Response: {response}\n")


# Example 2: Using Ollama with Mistral
print("=== Example 2: Ollama Mistral ===")
agent_mistral = Agent(
    model="ollama/mistral",
    model_kwargs={
        "base_url": "http://localhost:11434",
        "temperature": 0.7
    }
)
response = agent_mistral("Explain the difference between local and cloud LLMs.")
print(f"Response: {response}\n")


# Example 3: Using Ollama with CodeLlama for coding tasks
print("=== Example 3: Ollama CodeLlama ===")
agent_codellama = Agent(
    model="ollama/codellama",
    model_kwargs={
        "base_url": "http://localhost:11434"
    },
    system_prompt="You are an expert coding assistant."
)
response = agent_codellama("Write a Python function to calculate fibonacci numbers.")
print(f"Response: {response}\n")


# Example 4: Using Ollama with Phi-3 (smaller, faster model)
print("=== Example 4: Ollama Phi-3 (Small & Fast) ===")
agent_phi = Agent(
    model="ollama/phi3",
    model_kwargs={
        "base_url": "http://localhost:11434",
        "temperature": 0.5
    }
)
response = agent_phi("What is machine learning?")
print(f"Response: {response}\n")


"""
Setup Instructions:

1. Install Ollama:
   - macOS: brew install ollama
   - Linux: curl -fsSL https://ollama.com/install.sh | sh
   - Windows: Download from https://ollama.com/download

2. Start Ollama service:
   ollama serve

3. Pull models you want to use:
   ollama pull llama3
   ollama pull mistral
   ollama pull codellama
   ollama pull phi3

4. List available models:
   ollama list

5. Run this demo:
   python demo_11_ollama_models.py

Popular Ollama Models:

General Purpose:
- llama3 (8B, 70B): Meta's latest open model
- mistral: Fast and capable 7B model
- mixtral: Mixture of experts, very capable
- phi3: Microsoft's small but powerful model

Code-Specialized:
- codellama: Optimized for code generation
- deepseek-coder: Excellent coding model
- starcoder: Large code generation model

Benefits of Local Models:
- Privacy: Data never leaves your machine
- Cost: No API costs, unlimited usage
- Offline: Works without internet
- Speed: No network latency
- Control: Full control over model and data

Trade-offs:
- Requires local GPU/CPU resources
- Smaller models may be less capable than Claude
- Need to manage model downloads and updates
- Setup complexity vs cloud APIs

Model Sizes:
- 7B parameters: Fast, runs on most machines
- 13B parameters: Better quality, needs more RAM
- 70B+ parameters: Best quality, requires significant resources

Note: Ensure Ollama is running before executing this demo.
"""
