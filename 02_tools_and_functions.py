"""
Demo 2: Adding Tools & Custom Functions (8 min)
Goal: Show how to extend agents with capabilities

Key Teaching Points:
- How to create custom tools with @tool decorator
- How to use pre-built tools from strands_tools
- How to combine multiple tools in a single agent
"""

import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands_tools import calculator, current_time
from strands_tools.tavily import tavily_search


# for tavily_search,  signup for an apikey at https://app.tavily.com
# and set the environment variable TAVILY_API_KEY to your api key in the .env file
tavily_search.api_key = os.getenv("TAVILY_API_KEY")

# Load environment variables
load_dotenv()

@tool
def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of input text."""
    # Simple sentiment logic for demo
    positive_words = ['good', 'great', 'excellent', 'amazing']
    negative_words = ['bad', 'poor', 'terrible', 'awful']

    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    if pos_count > neg_count:
        return "Positive sentiment"
    elif neg_count > pos_count:
        return "Negative sentiment"
    else:
        return "Neutral sentiment"

# Create agent with multiple tools
agent = Agent(
    tools=[calculator, current_time, tavily_search, analyze_sentiment],
    system_prompt="You are a helpful assistant that can analyze data and search the web."
)

# Demo the tools in action
response = agent("""
1. What's the current time?
2. Calculate the compound interest on $10,000 at 5% for 3 years
3. Analyze the sentiment of: "This hackathon is going to be amazing!"
4. Search for the latest news about AI agents (use tavily_search)
""")

print(response)


"""
Sample output:
emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run demo_2_tools_and_functions.py     
I'll help you with all four requests. Let me execute them one by one:
Tool #1: current_time

Tool #2: calculator

Tool #3: analyze_sentiment

Tool #4: tavily_search
╭───────────────────────────────────────────────────────────────────────── Tavily Search Results ──────────────────────────────────────────────────────────────────────────╮
│ Query: latest news about AI agents                                                                                                                                       │
│                                                                                                                                                                          │
│ Results: 5 found                                                                                                                                                         │
│ --------------------------------------------------                                                                                                                       │
│                                                                                                                                                                          │
│ [1] 68% of Multinationals Eye AI Agent Integration by 2026 Amid Risks - WebProNews                                                                                       │
│ URL: https://www.webpronews.com/68-of-multinationals-eye-ai-agent-integration-by-2026-amid-risks/                                                                        │
│ Score: 0.86713725                                                                                                                                                        │
│ Content: Multinational organizations are rapidly adopting AI agents, with 68% expecting integration by 2026, driven by automation and autonomy needs. In a rapidly       │
│ evolving tech environment, multinational organizations are accelerating their embrace of agentic AI, with a recent study highlighting ambitious timelines for            │
│ integration. According to a global survey by consulting firm Protiviti, more than 68% of organizations anticipate having integrated AI agents by 2026, signaling a shift │
│ toward autonomous systems that can perform tasks with minimal human oversight. Recent news on platforms like X echoes this enthusiasm, with posts from industry analysts │
│ noting that 51% of companies are already using AI agents in production, based on surveys by LangChainAI.                                                                 │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [2] Anthropic releases Claude Sonnet 4.5 in latest bid for AI agents and coding supremacy - The Verge                                                                    │
│ URL: https://www.theverge.com/ai-artificial-intelligence/787524/anthropic-releases-claude-sonnet-4-5-in-latest-bid-for-ai-agents-and-coding-supremacy                    │
│ Score: 0.81418616                                                                                                                                                        │
│ Content: # Anthropic releases Claude Sonnet 4.5 in latest bid for AI agents and coding supremacy Anthropic’s latest AI model spent 30 hours running by itself to code a  │
│ chat app akin to Slack or Teams. The company called Claude Sonnet 4.5 “the best model in the world for real-world agents, coding, and computer use” and said it “leads   │
│ the market at using computers,” referencing the Computer Use feature Anthropic debuted nearly a year ago. Anthropic, OpenAI, Google, and other companies have been       │
│ continuously releasing incremental updates and features that allow their technology to act as an assistant both for consumers (researching topics, scheduling meet-ups,  │
│ and looking up flights) and for enterprise and developer use (creating slide decks, helping with coding tasks, and analyzing spreadsheets). Anthropic also said the new  │
│ model would be paired with other updates to help developers code their own AI agents.                                                                                    │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [3] Anthropic unveils latest AI model, aiming to extend its lead in coding intelligence - Business Insider                                                               │
│ URL: https://www.businessinsider.com/anthropic-ai-model-claude-sonnet-extend-coding-lead-2025-9                                                                          │
│ Score: 0.7644879                                                                                                                                                         │
│ Content: # Anthropic unveils latest AI model, aiming to extend its lead in coding intelligence This story is available exclusively to Business Insider subscribers. *    │
│ Anthropic released Claude Sonnet 4.5, calling it the top AI coding system. * Claude Agent SDK aims to give developers new tools for building customized, context-aware   │
│ AI agents. The startup also pitched the new model's ability to generate practical business outcomes through autonomous computer use, cybersecurity capabilities, and the │
│ creation of production-ready applications and context-aware AI agents. On the Claude Developer Platform, Anthropic launched a Claude Agent software development kit      │
│ providing developers with fine-grained tools for building customized, context-aware AI agents. This story is available exclusively to Business Insider subscribers.      │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [4] AI Megatrends 2025: The Next Wave Is Here—Why Data‑Center Power, AI Agents & Edge Devices Could Reshape Markets (and Portfolios) Now - ts2.tech                      │
│ URL: https://ts2.tech/en/ai-megatrends-2025-the-next-wave-is-here-why-data%E2%80%91center-power-ai-agents-edge-devices-could-reshape-markets-and-portfolios-now/         │
│ Score: 0.70287734                                                                                                                                                        │
│ Content: # AI Megatrends 2025: The Next Wave Is Here—Why Data‑Center Power, AI Agents & Edge Devices Could Reshape Markets (and Portfolios) Now * **Agentic AI goes      │
│ enterprise**: Citi began a **5,000‑user** pilot of **AI agents** that autonomously execute multi‑step tasks; McKinsey calls this shift the answer to the “**gen‑AI       │
│ paradox**.”  * **Edge AI arrives**: Microsoft’s **Copilot+ PCs** spread beyond Qualcomm to Intel/AMD; **Apple Intelligence** continued rolling out across iPhone, iPad   │
│ and Mac. **What’s happening.** Frontier models, agents and video‑native AI are pushing demand from chips to **power, cooling, memory and networking**. **Why it          │
│ matters.** If inference shifts to the edge for latency/cost/privacy, PCs and phones become **AI endpoints** in distributed workflows—taking pressure off data‑center     │
│ power while unlocking **new consumer and field** use cases.                                                                                                              │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [5] Agentic AI Adoption Underway but Singapore Workforce Lacks Familiarity and Skills - Yahoo                                                                            │
│ URL: https://sg.finance.yahoo.com/news/agentic-ai-adoption-underway-singapore-060000192.html                                                                             │
│ Score: 0.62879556                                                                                                                                                        │
│ Content: SINGAPORE, Oct. 2, 2025 /PRNewswire/ -- As Agentic Artificial Intelligence (AI) moves from concept to deployment, there is a consensus among business leaders   │
│ (77%) and employees (74%) that this new technology is vital to remain competitive. Seven in ten business leaders (70%) and more than four in five employees (83%) say    │
│ their workforce is "not very skilled" or "not skilled at all" in working with Agentic AI systems. These are some of the key findings from **NTUC LearningHub's White     │
│ Paper Report on Agentic AI for Workplace Resilience**, which surveyed 150 business leaders and 300 full-time working professionals to examine the growing prominence of  │
│ Agentic AI and its implications for cybersecurity and data governance.                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Here are the results for all four of your requests:

## 1. Current Time
The current time is: **October 4, 2025 at 9:57:28 PM UTC**

## 2. Compound Interest Calculation
For $10,000 invested at 5% annual interest compounded annually for 3 years:
- **Final amount: $11,584.00**
- **Interest earned: $1,584.00**

## 3. Sentiment Analysis
The sentiment of "This hackathon is going to be amazing!" is: **Positive sentiment**

## 4. Latest News About AI Agents
Here are the latest news updates about AI agents:

1. **Enterprise AI Agent Adoption Accelerating** (Sept 30, 2025)
   - 68% of multinational organizations expect to integrate AI agents by 2026
   - 51% of companies are already using AI agents in production

2. **Anthropic Releases Claude Sonnet 4.5** (Sept 29, 2025)
   - New model claims to be "the best model in the world for real-world agents, coding, and computer use"
   - Spent 30 hours autonomously coding a chat app similar to Slack or Teams
   - Includes new Claude Agent SDK for developers

3. **AI Megatrends 2025** (Sept 28, 2025)
   - Citi began a 5,000-user pilot of AI agents that execute multi-step tasks autonomously
   - McKinsey calls agentic AI the answer to the "gen-AI paradox"

4. **Singapore Workforce Skills Gap** (Oct 2, 2025)
   - 77% of business leaders and 74% of employees believe agentic AI is vital for competitiveness
   - However, 70% of business leaders and 83% of employees say their workforce lacks adequate AI skills

The trend shows rapid enterprise adoption of AI agents, with major companies launching large-scale pilots and new AI models specifically designed for autonomous task execution.Here are the results for all four of your requests:

## 1. Current Time
The current time is: **October 4, 2025 at 9:57:28 PM UTC**

## 2. Compound Interest Calculation
For $10,000 invested at 5% annual interest compounded annually for 3 years:
- **Final amount: $11,584.00**
- **Interest earned: $1,584.00**

## 3. Sentiment Analysis
The sentiment of "This hackathon is going to be amazing!" is: **Positive sentiment**

## 4. Latest News About AI Agents
Here are the latest news updates about AI agents:

1. **Enterprise AI Agent Adoption Accelerating** (Sept 30, 2025)
   - 68% of multinational organizations expect to integrate AI agents by 2026
   - 51% of companies are already using AI agents in production

2. **Anthropic Releases Claude Sonnet 4.5** (Sept 29, 2025)
   - New model claims to be "the best model in the world for real-world agents, coding, and computer use"
   - Spent 30 hours autonomously coding a chat app similar to Slack or Teams
   - Includes new Claude Agent SDK for developers

3. **AI Megatrends 2025** (Sept 28, 2025)
   - Citi began a 5,000-user pilot of AI agents that execute multi-step tasks autonomously
   - McKinsey calls agentic AI the answer to the "gen-AI paradox"

4. **Singapore Workforce Skills Gap** (Oct 2, 2025)
   - 77% of business leaders and 74% of employees believe agentic AI is vital for competitiveness
   - However, 70% of business leaders and 83% of employees say their workforce lacks adequate AI skills

The trend shows rapid enterprise adoption of AI agents, with major companies launching large-scale pilots and new AI models specifically designed for autonomous task execution.

"""