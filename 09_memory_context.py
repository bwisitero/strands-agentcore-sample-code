"""
Demo 17: Memory & Context Management
Goal: Agent with persistent memory across sessions

Key Teaching Points:
- Persistent memory storage (file-based for demo)
- User preferences and conversation history
- Context-aware responses
- Session management
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from strands import Agent, tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Memory storage path
MEMORY_DIR = Path("agent_memory")
MEMORY_DIR.mkdir(exist_ok=True)


class MemoryManager:
    """Manages persistent memory for the agent."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory_file = MEMORY_DIR / f"{user_id}_memory.json"
        self.memory = self.load_memory()

    def load_memory(self) -> Dict[str, Any]:
        """Load memory from file."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"⚠️  Corrupted memory file detected, creating fresh memory: {e}")
                # Backup corrupted file
                backup_file = self.memory_file.with_suffix('.json.backup')
                self.memory_file.rename(backup_file)
                print(f"   Old file backed up to: {backup_file}")

        return {
            "user_id": self.user_id,
            "preferences": {},
            "conversation_history": [],
            "facts": {},
            "created_at": datetime.now().isoformat(),
            "last_interaction": None
        }

    def save_memory(self):
        """Save memory to file."""
        self.memory["last_interaction"] = datetime.now().isoformat()
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, indent=2, fp=f)

    def add_preference(self, key: str, value: Any):
        """Store user preference."""
        self.memory["preferences"][key] = value
        self.save_memory()

    def get_preference(self, key: str) -> Any:
        """Retrieve user preference."""
        return self.memory["preferences"].get(key)

    def add_fact(self, key: str, value: Any):
        """Store a fact about the user."""
        self.memory["facts"][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self.save_memory()

    def get_fact(self, key: str) -> Any:
        """Retrieve a fact about the user."""
        fact = self.memory["facts"].get(key)
        return fact["value"] if fact else None

    def add_conversation(self, role: str, message: str):
        """Add to conversation history."""
        self.memory["conversation_history"].append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 50 messages
        self.memory["conversation_history"] = self.memory["conversation_history"][-50:]
        self.save_memory()

    def get_conversation_summary(self) -> str:
        """Get a summary of recent conversations."""
        history = self.memory["conversation_history"][-10:]
        if not history:
            return "No previous conversations."

        summary = ["Recent conversation history:"]
        for entry in history:
            role = "User" if entry["role"] == "user" else "Assistant"
            summary.append(f"{role}: {entry['message'][:100]}...")

        return "\n".join(summary)

    def get_context(self) -> str:
        """Get full context for the agent."""
        context = ["=== User Context ==="]

        if self.memory["preferences"]:
            context.append("\nPreferences:")
            for key, value in self.memory["preferences"].items():
                context.append(f"  - {key}: {value}")

        if self.memory["facts"]:
            context.append("\nKnown facts:")
            for key, data in self.memory["facts"].items():
                context.append(f"  - {key}: {data['value']}")

        last_interaction = self.memory.get("last_interaction")
        if last_interaction:
            context.append(f"\nLast interaction: {last_interaction}")

        return "\n".join(context)


# Global memory manager (in production, use proper session management)
memory_managers: Dict[str, MemoryManager] = {}


def get_memory_manager(user_id: str = "demo_user") -> MemoryManager:
    """Get or create memory manager for user."""
    if user_id not in memory_managers:
        memory_managers[user_id] = MemoryManager(user_id)
    return memory_managers[user_id]


@tool
def remember_preference(user_id: str, preference_name: str, preference_value: str) -> str:
    """Remember a user preference for future conversations."""
    manager = get_memory_manager(user_id)
    manager.add_preference(preference_name, preference_value)
    return f"I'll remember that your {preference_name} is {preference_value}."


@tool
def recall_preference(user_id: str, preference_name: str) -> str:
    """Recall a previously stored user preference."""
    manager = get_memory_manager(user_id)
    value = manager.get_preference(preference_name)
    if value:
        return f"Your {preference_name} is {value}."
    return f"I don't have a stored preference for {preference_name}."


@tool
def remember_fact(user_id: str, fact_name: str, fact_value: str) -> str:
    """Remember a fact about the user."""
    manager = get_memory_manager(user_id)
    manager.add_fact(fact_name, fact_value)
    return f"I'll remember that {fact_name}: {fact_value}."


@tool
def recall_fact(user_id: str, fact_name: str) -> str:
    """Recall a previously stored fact about the user."""
    manager = get_memory_manager(user_id)
    value = manager.get_fact(fact_name)
    if value:
        return f"{fact_name}: {value}"
    return f"I don't have information about {fact_name}."


@tool
def get_user_context(user_id: str) -> str:
    """Get all stored context about the user."""
    manager = get_memory_manager(user_id)
    return manager.get_context()


@tool
def clear_user_memory(user_id: str) -> str:
    """Clear all stored memory for the user."""
    manager = get_memory_manager(user_id)
    manager.memory = {
        "user_id": user_id,
        "preferences": {},
        "conversation_history": [],
        "facts": {},
        "created_at": datetime.now().isoformat(),
        "last_interaction": None
    }
    manager.save_memory()
    return "All memory has been cleared."


def create_memory_agent(user_id: str = "demo_user") -> Agent:
    """Create an agent with memory capabilities."""
    manager = get_memory_manager(user_id)

    # Inject user context into system prompt
    context = manager.get_context()

    agent = Agent(
        tools=[
            remember_preference,
            recall_preference,
            remember_fact,
            recall_fact,
            get_user_context,
            clear_user_memory
        ],
        system_prompt=f"""You are a helpful assistant with persistent memory capabilities.

Current user context:
{context}

When interacting with users:
1. Use remember_preference to store user preferences when they mention them
2. Use remember_fact to store important facts about the user
3. Use recall_preference and recall_fact to retrieve information
4. Proactively use stored information to personalize responses
5. Always pass the user_id parameter: "{user_id}"

Be natural and conversational. Don't explicitly mention you're storing things unless asked.
"""
    )

    return agent


def main():
    """Run the memory and context demo."""
    print("=" * 70)
    print("🧠 Memory & Context Management Demo")
    print("=" * 70)
    print()

    user_id = "demo_user"
    agent = create_memory_agent(user_id)
    manager = get_memory_manager(user_id)

    # Simulate a conversation with memory
    conversations = [
        ("Hello! My name is Alice and I prefer to be called Ali.", "user"),
        ("What's my name?", "user"),
        ("I love reading science fiction books, especially by Isaac Asimov.", "user"),
        ("My favorite color is blue.", "user"),
        ("What do you know about me?", "user"),
        ("What books do I like?", "user"),
    ]

    for i, (message, role) in enumerate(conversations, 1):
        print(f"\n{'='*70}")
        print(f"💬 Conversation Turn {i}")
        print(f"{'='*70}")
        print(f"User: {message}")

        # Store user message in memory
        manager.add_conversation("user", message)

        # Get agent response
        response = agent(f"user_id: {user_id}, message: {message}")

        # Convert response to string for storage
        response_text = str(response)

        # Store agent response in memory
        manager.add_conversation("assistant", response_text)

        print(f"\nAssistant: {response_text}")

    # Show stored memory
    print("\n" + "=" * 70)
    print("📊 Stored Memory")
    print("=" * 70)
    print(manager.get_context())

    print("\n" + "=" * 70)
    print("✨ Demo complete!")
    print(f"\nMemory saved to: {manager.memory_file}")
    print("Run the demo again to see memory persistence across sessions!")
    print("=" * 70)


if __name__ == "__main__":
    main()


"""
Setup Instructions:

1. Install required packages:
   uv add python-dotenv

2. Run the demo:
   python demo_17_memory_context.py

3. Run it again to see memory persistence!

Features Demonstrated:
- Persistent memory storage (file-based)
- User preference management
- Fact storage and retrieval
- Conversation history tracking
- Context-aware responses
- Session management

Memory Storage:
- Preferences: User settings (e.g., name, favorite color)
- Facts: Information about the user
- Conversation history: Recent chat messages
- Metadata: Timestamps, user ID

Use Cases:
- Personalized chatbots
- Customer service agents (remember customer preferences)
- Personal assistants (remember user habits)
- Educational tutors (track learning progress)
- Healthcare assistants (remember medical history)

Production Enhancements:
- Use Redis for distributed memory
- Use DynamoDB/PostgreSQL for scalable storage
- Implement memory decay (forget old information)
- Add memory search and filtering
- Implement memory sharing across agents
- Add privacy controls and data encryption
- Implement GDPR compliance (right to be forgotten)
- Add memory compression for long histories

Redis Example (for production):
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set(f"user:{user_id}:preferences", json.dumps(preferences))
```

DynamoDB Example (for production):
```python
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user_memory')
table.put_item(Item={'user_id': user_id, 'memory': memory_data})
```
"""


"""
Sample output

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run 14_memory_context.py
======================================================================
🧠 Memory & Context Management Demo
======================================================================

⚠️  Corrupted memory file detected, creating fresh memory: Expecting value: line 14 column 18 (char 316)
   Old file backed up to: agent_memory/demo_user_memory.json.backup

======================================================================
💬 Conversation Turn 1
======================================================================
User: Hello! My name is Alice and I prefer to be called Ali.
Hello Ali! It's nice to meet you. I'll make sure to remember that you prefer to be called Ali.
Tool #1: remember_fact

Tool #2: remember_preference
How can I help you today, Ali?
Assistant: How can I help you today, Ali?


======================================================================
💬 Conversation Turn 2
======================================================================
User: What's my name?

Tool #3: recall_fact

Tool #4: recall_preference
Your name is Alice, but you prefer to be called Ali!
Assistant: Your name is Alice, but you prefer to be called Ali!


======================================================================
💬 Conversation Turn 3
======================================================================
User: I love reading science fiction books, especially by Isaac Asimov.
That's fantastic, Ali! Isaac Asimov is such a brilliant science fiction author - his Foundation series and robot stories are absolutely captivating. Do you have a favorite Asimov work?
Tool #5: remember_preference

Tool #6: remember_preference
His Three Laws of Robotics were so ahead of their time and still influence how we think about AI today!
Assistant: His Three Laws of Robotics were so ahead of their time and still influence how we think about AI today!


======================================================================
💬 Conversation Turn 4
======================================================================
User: My favorite color is blue.
That's a lovely color choice, Ali! Blue is such a calming and versatile color.
Tool #7: remember_preference
Is there a particular shade of blue you're drawn to, or just blue in general?
Assistant: Is there a particular shade of blue you're drawn to, or just blue in general?


======================================================================
💬 Conversation Turn 5
======================================================================
User: What do you know about me?

Tool #8: get_user_context
Here's what I know about you, Ali:

- Your name is Alice, but you prefer to be called Ali
- You love reading science fiction books, especially by Isaac Asimov
- Your favorite color is blue

You have great taste in literature! Asimov's work really stands the test of time. Is there anything else you'd like me to know about you?
Assistant: Here's what I know about you, Ali:

- Your name is Alice, but you prefer to be called Ali
- You love reading science fiction books, especially by Isaac Asimov
- Your favorite color is blue

You have great taste in literature! Asimov's work really stands the test of time. Is there anything else you'd like me to know about you?


======================================================================
💬 Conversation Turn 6
======================================================================
User: What books do I like?

Tool #9: recall_preference

Tool #10: recall_preference
Based on what you've told me, Ali, you love reading science fiction books, especially works by Isaac Asimov! His stories about robots, space exploration, and the future of humanity are truly fascinating. Have you read any other sci-fi authors that you'd recommend, or are you looking for suggestions similar to Asimov's style?
Assistant: Based on what you've told me, Ali, you love reading science fiction books, especially works by Isaac Asimov! His stories about robots, space exploration, and the future of humanity are truly fascinating. Have you read any other sci-fi authors that you'd recommend, or are you looking for suggestions similar to Asimov's style?


======================================================================
📊 Stored Memory
======================================================================
=== User Context ===

Preferences:
  - preferred_name: Ali
  - favorite_genre: science fiction
  - favorite_author: Isaac Asimov
  - favorite_color: blue

Known facts:
  - name: Alice

Last interaction: 2025-10-05T13:17:45.518697

======================================================================
✨ Demo complete!

Memory saved to: agent_memory/demo_user_memory.json
Run the demo again to see memory persistence across sessions!
======================================================================
"""

