# Strands AI Agent Demos 🤖

A comprehensive collection of **23 progressive demos** to learn building AI agents with Strands, from basics to production-ready applications.

Perfect for hackathons, learning, and building real-world AI applications!

## 🚀 Quick Start

```bash
# Clone and install
git clone <your-repo>
cd strands-agentcore-demo
uv sync

# Run your first agent
python 01_hello_agent.py

# Try the web chatbot
python 04_fastapi_chatbot.py
# Open http://localhost:8000
```

## 📚 Learning Path

### Part 1: Fundamentals (Beginner)
Start here if you're new to Strands agents

| Demo | Name | What You'll Learn |
|------|------|-------------------|
| 01 | [Hello Agent](01_hello_agent.py) | Create your first agent, basic queries |
| 02 | [Tools & Functions](02_tools_and_functions.py) | Custom tools with @tool decorator |
| 03 | [Document Processing](03_document_processing.py) | Extract info from documents |
| 04 | [FastAPI Chatbot](04_fastapi_chatbot.py) | Web UI with FastAPI |

### Part 2: Knowledge & Data (Intermediate)
Work with data sources and knowledge bases

| Demo | Name | What You'll Learn |
|------|------|-------------------|
| 05 | [File Upload](05_file_upload.py) | Upload and process files |
| 06 | [AgentCore Deployment](06_agentcore_deployment.py) | Deploy to AWS AgentCore |
| 07 | [Multi-Agent](07_multi_agent.py) | Agent collaboration |
| 08 | [Streaming](08_streaming.py) | Real-time streaming responses |

### Part 3: Integration & APIs (Intermediate)
Connect to external services

| Demo | Name | What You'll Learn |
|------|------|-------------------|
| 09 | [Console Chat](09_console_chat.py) | Interactive chat sessions |
| 10 | [Memory & Context](10_memory_context.py) | Persistent memory across sessions |
| 11 | [Local Knowledge Base](11_local_knowledgebase.py) | Simple RAG implementation |
| 12 | [Bedrock Knowledge Base](12_bedrock_knowledgebase.py) | AWS managed knowledge bases |

### Part 4: Web & Production (Advanced)
Build production-ready applications

| Demo | Name | What You'll Learn |
|------|------|-------------------|
| 13 | [RAG Pipeline](13_rag_pipeline.py) | Complete RAG with embeddings |
| 14 | [Database Agent](14_database_agent.py) | Natural language to SQL |
| 15 | [External APIs](15_external_apis.py) | Weather, news, currency APIs |
| 16 | [MCP Integration](16_mcp_integration.py) | MCP server ecosystem |

### Part 5: Advanced Features (Expert)
Specialized capabilities for complex apps

| Demo | Name | What You'll Learn |
|------|------|-------------------|
| 17 | [Slack Bot](17_slack_bot.py) | Team collaboration assistant |
| 18 | [Image Analysis](18_image_analysis.py) | Vision models for images |
| 19 | [Voice Agent](19_voice_agent.py) | Speech-to-text & TTS |
| 20 | [Code Execution](20_code_execution.py) | Safe code generation & execution |

### Part 6: Best Practices (Essential)
Production patterns and optimization

| Demo | Name | What You'll Learn |
|------|------|-------------------|
| 21 | [Conversation Manager](21_conversation_manager.py) | Token limits & history management |
| 22 | [Custom Models](22_custom_models.py) | Switch between Bedrock models |
| 23 | [Ollama Models](23_ollama_models.py) | Local LLMs with Ollama |

## 🏆 Hackathon Quick Start (2-3 hours)

For rapid prototyping during a hackathon, follow this path:

```bash
# 1. Learn basics (15 min)
python 01_hello_agent.py
python 02_tools_and_functions.py

# 2. Build web interface (30 min)
python 04_fastapi_chatbot.py

# 3. Add external data (30 min)
python 15_external_apis.py

# 4. Add document Q&A (30 min)
python 03_document_processing.py

# 5. Combine and customize! (1 hour)
```

## 💡 Hackathon Project Ideas

**Smart Research Assistant**
```bash
# Combine: Document Processing + Knowledge Base + RAG
python 03_document_processing.py  # Learn document extraction
python 12_bedrock_knowledgebase.py  # Learn managed KB
python 13_rag_pipeline.py  # Learn complete RAG
# → Build a research tool that answers questions from papers
```

**Team Productivity Bot**
```bash
# Combine: Memory + Multi-Agent + Slack
python 10_memory_context.py  # Learn persistent memory
python 07_multi_agent.py  # Learn agent delegation
python 17_slack_bot.py  # Learn Slack integration
# → Build a Slack bot that remembers context and delegates tasks
```

**Data Analysis Platform**
```bash
# Combine: Database + Code Execution + Web UI
python 14_database_agent.py  # Learn SQL generation
python 20_code_execution.py  # Learn code execution
python 04_fastapi_chatbot.py  # Learn web interface
# → Build a natural language data analytics tool
```

**Multimodal AI Assistant**
```bash
# Combine: Voice + Vision + Web
python 19_voice_agent.py  # Learn voice processing
python 18_image_analysis.py  # Learn image analysis
python 04_fastapi_chatbot.py  # Learn web UI
# → Build an assistant that works with voice, images, and text
```

## 🛠️ Setup & Requirements

### Prerequisites
- Python 3.11+
- **uv** (recommended) or pip

### Installation

#### Option 1: Using uv (Recommended ⚡)

**Why uv?**
- 🚀 **10-100x faster** than pip
- 🔒 **Deterministic** dependency resolution
- 📦 **Built-in virtual environment** management
- 💾 **Better caching** - reuses packages across projects

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or on macOS: brew install uv

# Install all dependencies
uv sync

# Run any demo with uv
uv run python 01_hello_agent.py
uv run python 04_fastapi_chatbot.py

# Add a new package
uv add requests
uv add fastapi uvicorn

# Add dev dependencies
uv add --dev pytest black
```

#### Option 2: Using traditional Python/pip

You can still use Python directly without uv:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run demos directly
python 01_hello_agent.py
python 04_fastapi_chatbot.py

# Add new packages
pip install requests
```

### Running Demos

```bash
# With uv (handles virtual env automatically)
uv run python 01_hello_agent.py

# With traditional Python (activate venv first)
source .venv/bin/activate
python 01_hello_agent.py
```

### Environment Variables

Create a `.env` file for optional API keys:

```bash
# Optional - for news API (demo 09)
NEWS_API_KEY=your_newsapi_key  # Get from https://newsapi.org

# Optional - for Slack bot (demo 21)
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-secret

# Optional - for custom APIs
TAVILY_API_KEY=your_tavily_key  # For web search (demo 02)
```

Most demos work without API keys using free services!

## 📖 Documentation

- **[LEARNING_PATH.md](LEARNING_PATH.md)** - Detailed learning guide with tips and use cases
- **Each demo file** - Contains extensive documentation and production examples in comments

## 🎯 Key Features Covered

✅ Basic agent creation and configuration
✅ Custom tools and function calling
✅ Knowledge bases and RAG
✅ External API integration
✅ Multi-agent collaboration
✅ Web interfaces with FastAPI
✅ Database querying with natural language
✅ Document processing and Q&A
✅ Code generation and execution
✅ Voice and image processing
✅ Persistent memory
✅ Production deployment
✅ Slack/Discord integration
✅ Token management & conversation history
✅ Custom and local model support

## 🤝 Contributing

Have a cool demo idea? Contributions welcome!

1. Follow the existing demo structure
2. Include comprehensive documentation
3. Add production-ready examples
4. Update LEARNING_PATH.md

## 📝 License

[Your License Here]

## 🙋 Support

- **Issues**: [GitHub Issues](your-repo/issues)
- **Discussions**: [GitHub Discussions](your-repo/discussions)
- **Strands Docs**: [docs.strands.ai](https://docs.strands.ai)

---

**Happy Building! 🚀**

Made with ❤️ for the Strands AI Hackathon
