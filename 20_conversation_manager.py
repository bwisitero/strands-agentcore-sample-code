"""
Demo: Managing Conversation History for Token Limits

This demo shows how to manage conversation history to prevent token limit errors
in complex applications. Without proper management, long conversations can exceed
model token limits and cause failures.

Key Teaching Points:
- Why token management matters for production apps
- How Agent maintains conversation history automatically
- Managing multiple conversation sessions with separate agents
- Clearing history to stay within token limits
- Using session_id for multi-user applications
"""

import os
from strands import Agent

# Enable bypass for smooth demo
os.environ['BYPASS_TOOL_CONSENT'] = 'true'


def demo_automatic_history():
    """Demo showing how Agent automatically maintains history."""
    print("\n" + "=" * 60)
    print("Demo 1: Automatic Conversation History")
    print("=" * 60)

    agent = Agent(name="Assistant")

    print("\n💬 Agent maintains conversation history automatically:")

    response1 = agent("My favorite color is blue")
    print(f"Turn 1: Set context")

    response2 = agent("What is my favorite color?")
    print(f"Turn 2: {response2}")

    print("\n✅ Agent remembers context across turns!")


def demo_separate_sessions():
    """Demo showing how to manage separate conversation sessions."""
    print("\n" + "=" * 60)
    print("Demo 2: Multiple Conversation Sessions")
    print("=" * 60)

    print("\n🔑 Use separate Agent instances for separate conversations")

    # Session 1: Travel planning
    agent1 = Agent(name="Travel Agent")
    print("\n📝 Session 1: Travel Planning")
    agent1("I want to visit Japan in spring")
    response1 = agent1("What cities should I visit?")
    print(f"Response: {str(response1)[:80]}...")

    # Session 2: Cooking (separate agent = separate history)
    agent2 = Agent(name="Chef Agent")
    print("\n📝 Session 2: Cooking Tips")
    response2 = agent2("How do I make scrambled eggs?")
    print(f"Response: {str(response2)[:80]}...")

    # Continue session 1 - context is maintained
    print("\n📝 Back to Session 1: Travel Planning")
    response3 = agent1("What about accommodations?")
    print(f"Response: {str(response3)[:80]}...")

    print("\n✅ Separate agents = separate conversation histories!")


def demo_token_limit_risk():
    """Demo showing the risk of exceeding token limits."""
    print("\n" + "=" * 60)
    print("Demo 3: Token Limit Risk in Long Conversations")
    print("=" * 60)

    agent = Agent(name="Long Runner")

    print("\n⚠️  Without management, long conversations risk token limits:")
    print("\nSimulating a long conversation...")

    # Simulate many turns
    for i in range(5):
        prompt = f"Tell me about topic {i+1}"
        response = agent(prompt)
        print(f"  Turn {i+1}: {len(str(response))} chars in response")

    print("\n⚠️  As conversation grows:")
    print("  - Token usage increases with each turn")
    print("  - Eventually may exceed model's context window")
    print("  - Can cause errors or unexpected behavior")
    print("  - Need strategies to manage history")


def demo_history_reset():
    """Demo showing how to reset conversation by creating new agent."""
    print("\n" + "=" * 60)
    print("Demo 4: Resetting Conversation History")
    print("=" * 60)

    print("\n🔄 Create new agent instance to reset history:")

    # First agent with history
    agent = Agent(name="Bot")
    agent("My name is Alice")
    agent("I work as a data scientist")
    response1 = agent("What's my name?")
    print(f"\nBefore reset: {response1}")

    # Reset by creating new agent
    print("\n🔄 Creating new agent (resets history)...")
    agent = Agent(name="Bot")
    response2 = agent("What's my name?")
    print(f"After reset: {response2}")

    print("\n✅ New agent instance = fresh start!")


def main():
    print("=" * 60)
    print("DEMO: Managing Conversation History")
    print("=" * 60)

    # Uncomment demos you want to run:
    demo_automatic_history()
    demo_separate_sessions()
    demo_token_limit_risk()
    demo_history_reset()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("=" * 60)
    print("✓ Agent automatically maintains conversation history")
    print("✓ Use separate Agent instances for separate conversations")
    print("✓ Long conversations can exceed token limits")
    print("✓ Reset history by creating a new Agent instance")
    print("✓ Essential for multi-user apps and chatbots")
    print("=" * 60)


if __name__ == "__main__":
    main()


"""Sample output

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run 22_conversation_manager.py 
============================================================
DEMO: Managing Conversation History
============================================================

============================================================
Demo 1: Automatic Conversation History
============================================================

💬 Agent maintains conversation history automatically:
Blue is a wonderful color! It's actually one of the most popular favorite colors. There's something really calming and versatile about blue - from the soft sky blues to deep ocean blues to vibrant electric blues. Do you have a particular shade of blue you're drawn to, or is it blue in general that appeals to you?Turn 1: Set context
Your favorite color is blue - you just told me that in your previous message!Turn 2: Your favorite color is blue - you just told me that in your previous message!


✅ Agent remembers context across turns!

============================================================
Demo 2: Multiple Conversation Sessions
============================================================

🔑 Use separate Agent instances for separate conversations

📝 Session 1: Travel Planning
Spring is a wonderful time to visit Japan! Here are some key things to know:

**Best Timing:**
- Late March to early May is peak spring season
- Cherry blossom (sakura) season typically runs March-May, varying by region
- Southern Japan blooms earlier, northern areas later

**Top Spring Destinations:**
- **Tokyo** - Ueno Park, Shinjuku Gyoen, Chidorigafuchi
- **Kyoto** - Philosopher's Path, Maruyama Park, Arashiyama
- **Osaka** - Osaka Castle Park, Kema Sakuranomiya Park
- **Mount Fuji area** - Kawaguchi Lake, Chureito Pagoda
- **Nara** - Nara Park with deer and cherry blossoms

**What to Expect:**
- Mild temperatures (10-20°C/50-68°F)
- Occasional rain showers
- Crowds during peak sakura season
- Higher accommodation prices
- Beautiful pink and white blossoms everywhere

**Tips:**
- Book accommodations early - spring is very popular
- Pack layers and a light rain jacket
- Consider hanami (cherry blossom viewing) picnics
- Check sakura forecasts for timing your trip

Do you have specific cities in mind or particular interests (culture, nature, food, etc.)? I can provide more targeted recommendations!Here are the best city combinations for a spring Japan trip:

**Classic First-Timer Route (7-14 days):**
- **Tokyo** (3-4 days) - Modern culture, diverse neighborhoods, great sakura spots
- **Kyoto** (2-3 days) - Traditional temples, geishas, incredible cherry blossoms
- **Osaka** (1-2 days) - Food capital, castle, easy day trips

**Extended Golden Route (10-14 days):**
Add to the above:
- **Nara** (day trip from Kyoto/Osaka) - Deer park, Todaiji Temple
- **Hakone/Mount Fuji area** (1-2 days) - Hot springs, mountain views
- **Hiroshima** (1-2 days) - Peace Memorial, Miyajima Island

**Off-the-Beaten-Path Options:**
- **Kanazawa** - Kenrokuen Garden (one of Japan's top 3), traditional crafts
- **Takayama** - Historic mountain town, great sake
- **Nikko** - UNESCO temples, nature (day trip from Tokyo)

**Northern Extension (if you have 2+ weeks):**
- **Sendai** - Famous for cherry blossoms
- **Kakunodate** - Samurai district with weeping cherry trees

**My Recommendation for First Visit:**
Tokyo (4 days) → Hakone (1 day) → Kyoto (3 days) → Nara (day trip) → Osaka (2 days)

How many days do you have total? Are you interested in big cities, traditional culture, nature, or a mix of everything?Response: Here are the best city combinations for a spring Japan trip:

**Classic First-Ti...

📝 Session 2: Cooking Tips
Here's how to make basic scrambled eggs:

**Ingredients:**
- 2-3 eggs
- 2-3 tablespoons milk or cream (optional)
- Salt and pepper to taste
- 1-2 teaspoons butter or oil

**Steps:**
1. **Crack and whisk** the eggs in a bowl with milk (if using), salt, and pepper until well combined

2. **Heat the pan** on medium-low heat and add butter, letting it melt and coat the pan

3. **Pour in the eggs** and let them sit for about 20 seconds

4. **Gently stir** with a spatula, pushing the eggs from the edges toward the center, tilting the pan to let uncooked egg flow underneath

5. **Continue stirring gently** every 20-30 seconds. The eggs will gradually form soft curds

6. **Remove from heat** when the eggs still look slightly wet (they'll continue cooking from residual heat)

**Tips:**
- Keep heat on medium-low to avoid tough, rubbery eggs
- Don't over-stir - gentle movements work best
- The whole process should take 2-4 minutes
- Serve immediately while hot

Would you like any variations or additional tips?Response: Here's how to make basic scrambled eggs:

**Ingredients:**
- 2-3 eggs
- 2-3 tabl...

📝 Back to Session 1: Travel Planning
Here's a breakdown of accommodation options for spring in Japan:

**Types of Accommodations:**

**Hotels:**
- **Business hotels** - Clean, compact, $60-120/night (Toyoko Inn, APA Hotels)
- **Mid-range hotels** - More space/amenities, $100-200/night
- **Luxury hotels** - Premium service, $300+/night (Park Hyatt, Ritz-Carlton)

**Traditional Options:**
- **Ryokan** - Traditional inns with tatami rooms, kaiseki meals, $150-500+/night
- **Minshuku** - Family-run guesthouses, simpler than ryokan, $50-100/night

**Budget Options:**
- **Hostels** - Dorms $25-40/night, private rooms $60-80/night
- **Capsule hotels** - Unique experience, $30-60/night
- **Manga cafes** - Ultra-budget emergency option, $15-25/night

**Spring-Specific Tips:**
- **Book 2-3 months ahead** - Spring is peak season, especially during Golden Week (late April/early May)
- **Prices increase 50-100%** during sakura peak
- **Consider locations near train stations** for easy temple/park access
- **Hakone/Mount Fuji ryokans** book up fastest in spring

**Recommended Areas:**
- **Tokyo:** Shibuya, Shinjuku, Asakusa
- **Kyoto:** Near Kyoto Station, Gion district
- **Osaka:** Namba, Osaka Station area

Do you have a budget range in mind? Are you interested in trying traditional ryokan or prefer modern hotels?Response: Here's a breakdown of accommodation options for spring in Japan:

**Types of Acc...

✅ Separate agents = separate conversation histories!

============================================================
Demo 3: Token Limit Risk in Long Conversations
============================================================

⚠️  Without management, long conversations risk token limits:

Simulating a long conversation...
I don't have any context about what "topic 1" refers to. Could you please provide more details about which specific topic you'd like me to discuss? For example:

- Is this from a course syllabus or curriculum?
- A list of topics we discussed earlier?
- A specific subject area you're studying?
- Something from a document or presentation?

Once you give me more context, I'll be happy to provide detailed information about the topic you're interested in!  Turn 1: 455 chars in response
I still don't have any context about what "topic 2" refers to. It seems like you might be referencing a specific list, curriculum, or set of topics, but I don't have access to that information.

To help you effectively, I would need you to:

- Specify what subject area or field these topics are from
- Provide the actual topic titles or descriptions
- Give me context about where these numbered topics come from
- Tell me what specific information you're looking for

Could you please share more details about what topic 2 actually covers? Then I can give you a comprehensive explanation!  Turn 2: 590 chars in response
I notice you've now asked about topics 1, 2, and 3, but I still don't have any context about what these numbered topics refer to. It seems like you might be testing something or expecting me to know about a specific set of topics, but I don't have access to any list or curriculum you might be referencing.

To provide you with helpful information, I would need you to actually tell me what these topics are about. For example:
- "Tell me about topic 3: photosynthesis"
- "Tell me about topic 3 from my biology class"
- "Tell me about topic 3: machine learning algorithms"

Without knowing the actual subject matter, I can't provide meaningful information. Could you please specify what topic 3 actually covers?  Turn 3: 712 chars in response
I see a pattern here - you've now asked about topics 1, 2, 3, and 4 without providing any context about what these topics actually are. 

I don't have access to any predefined list of numbered topics, and I can't guess what specific subjects you're referring to. Each time you ask, I need you to actually specify what the topic is about.

If you're looking for information on specific subjects, please tell me what they are directly. For example:
- "Tell me about photosynthesis"
- "Explain quantum mechanics"
- "What is machine learning?"

Or if these are from a specific course or document, please share that context.

Is there something specific you're trying to accomplish with these numbered topic requests? I'm happy to help once I understand what information you're actually seeking!  Turn 4: 791 chars in response
I understand you're continuing the pattern with topic 5, but as I've mentioned in my previous responses, I don't have access to any numbered list of topics you might be referencing.

It seems like you might be:
- Testing how I respond to repeated similar requests
- Expecting me to have access to a specific curriculum or document
- Or perhaps there's some other purpose I'm not understanding

I'm genuinely ready to help you learn about any subject you're interested in, but I need you to tell me what the actual topics are rather than just referring to them by number.

Would you like to share what you're actually hoping to learn about? I'm here to provide detailed, helpful explanations once I know what subject matter you're interested in exploring.  Turn 5: 755 chars in response

⚠️  As conversation grows:
  - Token usage increases with each turn
  - Eventually may exceed model's context window
  - Can cause errors or unexpected behavior
  - Need strategies to manage history

============================================================
Demo 4: Resetting Conversation History
============================================================

🔄 Create new agent instance to reset history:
Hello Alice! It's nice to meet you. How are you doing today?That's great, Alice! Data science is such a fascinating and rapidly evolving field. What kind of work do you focus on as a data scientist? Are you working with particular types of data or in a specific industry? I'd love to hear more about what you're working on or what aspects of the field you find most interesting.Your name is Alice.
Before reset: Your name is Alice.


🔄 Creating new agent (resets history)...
I don't have any information about your name. You haven't told me what it is, and I don't have access to any personal information about you. What would you like me to call you?After reset: I don't have any information about your name. You haven't told me what it is, and I don't have access to any personal information about you. What would you like me to call you?


✅ New agent instance = fresh start!

============================================================
KEY TAKEAWAYS:
============================================================
✓ Agent automatically maintains conversation history
✓ Use separate Agent instances for separate conversations
✓ Long conversations can exceed token limits
✓ Reset history by creating a new Agent instance
✓ Essential for multi-user apps and chatbots
============================================================
"""