# Strands AgentCore Demo - 30 Minute Presentation Script

**Total Time:** 30 minutes
**Audience:** Technical audience interested in AI agents and AWS Bedrock
**Goal:** Show practical examples of building AI agents with Strands

> **✨ Demos are now numbered in presentation order for easy following!**

---

## 🎯 Demo Overview

### Main Presentation Path (Demos 01-08)
**Follow these in order for the 30-minute presentation:**

1. **01_hello_agent** - Simplest agent (4 lines)
2. **02_tools_and_functions** - Adding capabilities
3. **03_tool_consent** - Autonomous execution
4. **04_document_processing** - Real-world RAG
5. **05_fastapi_chatbot** - Web deployment
6. **06_file_upload** - Production app
7. **07_agentcore_deployment** - AWS deployment
8. **08_multi_agent** - Complex workflows

### Supporting Demos (Demos 09-24)
**Additional examples for deep dives:**
- **09-11:** Intermediate (streaming, chat, memory)
- **12-15:** Data & knowledge (RAG, databases)
- **16-18:** Integrations (APIs, MCP, Slack)
- **19-22:** Advanced (images, voice, code)
- **23-24:** Model options (custom, Ollama)

---

## 📖 Detailed Script

### Opening (2 minutes)

**Say:**
> "Hi everyone! Today I'm showing you how to build production AI agents with Strands and AWS Bedrock. We have 24 demos **numbered in presentation order** - we'll walk through demos 1-8 together."

**Show terminal:**
```bash
ls *.py | head -10
```

> "Demos 1-8 are the main path. Each builds on the last - from 'Hello World' to production deployment. But first, let's quickly set up our environment."

---

### Setup with UV (2 minutes)

**Say:**
> "We're using UV - the fast Python package manager. It's like pip but handles everything: dependencies, virtual environments, Python versions."

**Show setup:**
```bash
# Install UV if needed (one-time)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone or navigate to demo repo
cd strands-agentcore-demo

# UV automatically creates venv and installs dependencies
uv sync
```

**Key Points:**
- ✅ UV handles Python version management
- ✅ No need for manual venv creation
- ✅ Fast dependency resolution
- ✅ `uv run` executes scripts in the project environment

**Say:**
> "That's it! UV reads our `pyproject.toml` and sets up everything. Now we can run any demo with `uv run`. Let's start with Demo 1."

---

### Demo 01: Hello Agent (2 min)

**File:** `01_hello_agent.py`

**Say:**
> "Demo 1 - the simplest agent. Watch - this is 4 lines of code."

**Run:**
```bash
uv run 01_hello_agent.py
```

**Show code:**
```python
from strands import Agent

agent = Agent()
response = agent("What is 2+2?")
print(response)
```

**Key Point:** 4 lines = working AI agent on AWS Bedrock

---

### Demo 02: Tools and Functions (3 min)

**File:** `02_tools_and_functions.py`

**Say:**
> "Demo 2 - agents get powerful with tools."

**Show code:**
```python
@tool
def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    ...

agent = Agent(tools=[calculate_fibonacci])
```

**Run:**
```bash
uv run 02_tools_and_functions.py
```

**Key Point:** `@tool` decorator + docstring = agent knows when and how to use it

---

### Demo 03: Tool Consent (3 min)

**File:** `03_tool_consent.py`

**Say:**
> "Demo 3 - critical for production: autonomous execution."

**Show code:**
```python
os.environ['BYPASS_TOOL_CONSENT'] = 'true'
```

**Run:**
```bash
uv run 03_tool_consent.py
```

**Key Point:** One env variable = fully autonomous agents (no manual approval)

---

### Demo 04: Document Processing (4 min)

**File:** `04_document_processing.py`

**Say:**
> "Demo 4 - real business use case: document Q&A."

**Run:**
```bash
uv run 04_document_processing.py
```

**Watch it:**
- Create sample documents
- Answer questions about employment contract
- Extract product features
- Summarize research

**Key Point:** Simple RAG pipeline for document analysis

---

### Demo 05: FastAPI Chatbot (4 min)

**File:** `05_fastapi_chatbot.py`

**Say:**
> "Demo 5 - web deployment with conversation memory."

**Run:**
```bash
uv run 05_fastapi_chatbot.py
```

**Browser:** `http://localhost:8000`

**Demo:**
1. "My name is Emil"
2. "What's 15 * 23?"
3. "What's my name?" ← Shows memory works!

**Key Point:** Session-based agents with automatic conversation history

---

### Demo 06: File Upload (4 min)

**File:** `06_file_upload.py`

**Say:**
> "Demo 6 - users upload files and chat with them."

**Run:**
```bash
uv run 06_file_upload.py
```

**Browser:** `http://localhost:8000`

**Demo:**
1. Drag-drop a file
2. Ask "What files did I upload?"
3. Ask "Summarize this document"

**Key Point:** Production-ready document analysis platform

---

### Demo 07: AgentCore Deployment (3 min)

**File:** `07_agentcore_deployment.py`

**Say:**
> "Demo 7 - deploying to production with AWS AgentCore."

**Show code:**
```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.route("/agent")
def agent_handler(prompt):
    return agent(prompt)
```

**Benefits:**
- Auto-scaling
- CloudWatch monitoring
- IAM security
- Session persistence

**Deploy:**
```bash
agentcore deploy --name my-agent
```

**Key Point:** One command → production deployment

---

### Demo 08: Multi-Agent (3 min)

**File:** `08_multi_agent.py`

**Say:**
> "Demo 8 - multiple agents working together."

**Run:**
```bash
uv run 08_multi_agent.py
```

**Show pattern:**
```python
researcher = Agent(name="Researcher", tools=[search])
writer = Agent(name="Writer")

# Research → Write → Review
```

**Key Point:** Specialized agents = better results (like human teams)

---

### Closing (2 min)

**Recap:**

✅ **Foundation (1-3):** Hello Agent → Tools → Autonomous
✅ **Real-World (4-6):** Documents → Web Chat → File Upload
✅ **Production (7-8):** AWS Deploy → Multi-Agent

**Additional Demos:**
- **09-11:** Streaming, console, memory
- **12-15:** Knowledge bases, RAG, databases
- **16-18:** APIs, MCP, Slack
- **19-22:** Images, voice, code
- **23-24:** Custom models, Ollama

**Next Steps:**
```bash
uv run 01_hello_agent.py  # Start here
# Then run 02, 03, 04... in order
```

---

## ⏱️ Timing Reference

| Time | Demo | Key Point | Required |
|------|------|-----------|----------|
| 0-2 | Intro | Overview | ✅ |
| 2-4 | Setup | UV environment | ✅ |
| 4-6 | 01 | 4 lines | ✅ |
| 6-9 | 02 | Tools | ✅ |
| 9-12 | 03 | Autonomous | ✅ |
| 12-16 | 04 | RAG | ✅ |
| 16-20 | 05 | Web chat | ✅ |
| 20-24 | 06 | File upload | ✅ |
| 24-27 | 07 | AWS deploy | Optional |
| 27-30 | 08 | Multi-agent | Optional |
| 30 | Q&A | Questions | ✅ |

---

## 💡 Q&A Quick Answers

**Q: What models?**
A: Any Bedrock model (Claude, Nova, Llama). Also Ollama (Demo 24).

**Q: Cost?**
A: Bedrock API calls + AgentCore compute. Strands SDK is free.

**Q: Internal data?**
A: Yes - via tools. Demos 15 (database), 16 (APIs), 04 (documents).

**Q: Security?**
A: AWS-grade with AgentCore. IAM, VPC, audit logging.

**Q: vs LangChain?**
A: Strands is simpler, Bedrock-native. Can integrate via MCP (Demo 17).

---

## 🎯 Pro Tips

**Before:**
- Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Run `uv sync` to set up dependencies
- Test demos 01-08 with `uv run`
- Have terminals ready
- Check browser (demos 05, 06)

**During:**
- Run code while talking
- Follow numbers: Setup → 01 → 02 → 03...
- Skip to closing if running late

**If breaks:**
- Show code, explain, move on
- Have screenshots as backup

---

**Good luck! 🚀 Just follow the numbers: 01, 02, 03...**
