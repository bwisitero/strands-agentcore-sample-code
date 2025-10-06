"""
Demo 16: Tool-Calling Agent with External APIs
Goal: Integrate with real external APIs (weather, news, etc.)

Key Teaching Points:
- Calling external REST APIs from agent tools
- Handling API responses and errors
- Real-time data aggregation
- Multi-source information synthesis
"""

import os
import requests
from strands import Agent, tool
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Get current weather information for a city using wttr.in API (no key required)."""
    try:
        # Using wttr.in - a free weather API that doesn't require API key
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        current = data['current_condition'][0]

        weather_info = f"""
Weather in {city}:
- Temperature: {current['temp_C']}°C ({current['temp_F']}°F)
- Condition: {current['weatherDesc'][0]['value']}
- Humidity: {current['humidity']}%
- Wind: {current['windspeedKmph']} km/h
- Feels Like: {current['FeelsLikeC']}°C
"""
        return weather_info.strip()
    except Exception as e:
        return f"Error getting weather: {str(e)}"


@tool
def get_news_headlines(topic: str = "technology") -> str:
    """Get latest news headlines about a topic using NewsAPI."""
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        return """NewsAPI key not found. To use this tool:
1. Sign up at https://newsapi.org (free tier available)
2. Add NEWS_API_KEY to your .env file
For demo purposes, using mock data instead."""

    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": topic,
            "apiKey": api_key,
            "pageSize": 5,
            "sortBy": "publishedAt",
            "language": "en"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            return f"Error: {data.get('message', 'Unknown error')}"

        articles = data.get("articles", [])
        if not articles:
            return f"No news found for topic: {topic}"

        headlines = [f"📰 Latest {topic} news:\n"]
        for i, article in enumerate(articles[:5], 1):
            headlines.append(f"{i}. {article['title']}")
            headlines.append(f"   Source: {article['source']['name']}")
            headlines.append(f"   {article['url']}\n")

        return "\n".join(headlines)

    except Exception as e:
        return f"Error getting news: {str(e)}"


@tool
def get_exchange_rate(from_currency: str = "USD", to_currency: str = "EUR") -> str:
    """Get current exchange rate between two currencies using exchangerate-api.com (free, no key required)."""
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        to_curr = to_currency.upper()

        if to_curr not in data['rates']:
            return f"Currency {to_curr} not found"

        rate = data['rates'][to_curr]
        return f"1 {from_currency.upper()} = {rate:.4f} {to_curr}\nLast updated: {data['date']}"

    except Exception as e:
        return f"Error getting exchange rate: {str(e)}"


@tool
def get_public_holidays(country_code: str = "US", year: int = 2025) -> str:
    """Get public holidays for a country using Nager.Date API (free, no key required)."""
    try:
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code.upper()}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        holidays = response.json()

        if not holidays:
            return f"No holidays found for {country_code.upper()} in {year}"

        # Get next 5 upcoming holidays
        today = datetime.now().date()
        upcoming = []

        for holiday in holidays:
            holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
            if holiday_date >= today:
                upcoming.append(f"• {holiday['localName']} - {holiday['date']} ({holiday['name']})")
            if len(upcoming) >= 5:
                break

        if not upcoming:
            return f"No upcoming holidays found for {country_code.upper()} in {year}"

        return f"Upcoming holidays in {country_code.upper()}:\n" + "\n".join(upcoming)

    except Exception as e:
        return f"Error getting holidays: {str(e)}"


@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia and get a summary of the topic."""
    try:
        # Wikipedia API
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        summary = f"""
📚 Wikipedia: {data.get('title', query)}

{data.get('extract', 'No summary available')}

🔗 Read more: {data.get('content_urls', {}).get('desktop', {}).get('page', '')}
"""
        return summary.strip()

    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"


# Create API agent
api_agent = Agent(
    tools=[
        get_weather,
        get_news_headlines,
        get_exchange_rate,
        get_public_holidays,
        search_wikipedia
    ],
    system_prompt="""You are a helpful information assistant with access to various APIs.

When users ask questions:
1. Determine which API(s) would be most helpful
2. Call the appropriate tools to gather information
3. Synthesize information from multiple sources when relevant
4. Present the information in a clear, organized format
5. If API keys are missing, inform the user how to set them up

You have access to:
- Weather information (wttr.in)
- News headlines (NewsAPI - requires key)
- Currency exchange rates
- Public holidays
- Wikipedia summaries
"""
)


def main():
    """Run the external API demo."""
    print("=" * 70)
    print("🌐 External API Integration Demo")
    print("=" * 70)
    print()

    queries = [
        "What's the weather like in London?",
        "What's the exchange rate between USD and EUR?",
        "What are the upcoming holidays in the US?",
        "Tell me about artificial intelligence from Wikipedia",
        "Get me the latest technology news",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n❓ Query {i}: {query}")
        print("-" * 70)
        response = api_agent(query)
        print(response)
        print()

    print("=" * 70)
    print("✨ Demo complete!")
    print("\nNote: Some APIs require keys. Check the .env.example for setup:")
    print("  NEWS_API_KEY=your_key_here  # Get free key at https://newsapi.org")
    print("=" * 70)


if __name__ == "__main__":
    main()


"""
Setup Instructions:

1. Install required packages:
   uv add requests python-dotenv

2. (Optional) Set up API keys in .env file:
   NEWS_API_KEY=your_newsapi_key  # Get from https://newsapi.org

3. Run the demo:
   python demo_16_external_apis.py

Features Demonstrated:
- Multiple external API integrations
- Free APIs that don't require keys
- Error handling for API calls
- Data aggregation from multiple sources
- API key management with environment variables

Available APIs (No Key Required):
- wttr.in - Weather data
- exchangerate-api.com - Currency exchange rates
- Nager.Date - Public holidays
- Wikipedia API - Encyclopedia summaries

Optional APIs (Free Key Required):
- NewsAPI - Latest news headlines

Use Cases:
- Personal assistant applications
- Information aggregation dashboards
- Travel planning tools
- Financial data apps
- News monitoring systems

Production Considerations:
- Implement rate limiting
- Add caching for frequently requested data
- Handle API timeouts gracefully
- Use async requests for better performance
- Add retry logic with exponential backoff
- Monitor API usage and costs
- Implement fallback data sources
"""


"""
Sample outpout

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run 09_external_apis.py 
======================================================================
🌐 External API Integration Demo
======================================================================


❓ Query 1: What's the weather like in London?
----------------------------------------------------------------------
I'll get the current weather information for London for you.
Tool #1: get_weather
Here's the current weather in London:

🌤️ **Partly Cloudy**
- **Temperature:** 16°C (61°F)
- **Feels like:** 16°C 
- **Humidity:** 48%
- **Wind:** 24 km/h

It's a pleasant day in London with mild temperatures and partly cloudy skies. The wind is a bit brisk at 24 km/h, but overall quite comfortable weather conditions!Here's the current weather in London:

🌤️ **Partly Cloudy**
- **Temperature:** 16°C (61°F)
- **Feels like:** 16°C 
- **Humidity:** 48%
- **Wind:** 24 km/h

It's a pleasant day in London with mild temperatures and partly cloudy skies. The wind is a bit brisk at 24 km/h, but overall quite comfortable weather conditions!



❓ Query 2: What's the exchange rate between USD and EUR?
----------------------------------------------------------------------
I'll get the current exchange rate between USD and EUR for you.
Tool #2: get_exchange_rate
Here's the current exchange rate:

💱 **USD to EUR Exchange Rate**
- **1 USD = 0.8520 EUR**
- **Last updated:** October 5, 2025

This means that for every US Dollar, you would get approximately 85.20 Euro cents. Conversely, 1 Euro would be worth about $1.17 USD.Here's the current exchange rate:

💱 **USD to EUR Exchange Rate**
- **1 USD = 0.8520 EUR**
- **Last updated:** October 5, 2025

This means that for every US Dollar, you would get approximately 85.20 Euro cents. Conversely, 1 Euro would be worth about $1.17 USD.



❓ Query 3: What are the upcoming holidays in the US?
----------------------------------------------------------------------
I'll get the public holidays for the United States in 2025.
Tool #3: get_public_holidays
Here are the upcoming public holidays in the United States for the rest of 2025:

🇺🇸 **Upcoming US Public Holidays**

📅 **October 13, 2025**
- Columbus Day
- Indigenous Peoples' Day (observed on the same date)

📅 **November 11, 2025**
- Veterans Day

📅 **November 27, 2025**
- Thanksgiving Day

📅 **December 25, 2025**
- Christmas Day

Note that Columbus Day and Indigenous Peoples' Day are both observed on October 13th, with many states and localities choosing to recognize Indigenous Peoples' Day instead of or alongside Columbus Day.Here are the upcoming public holidays in the United States for the rest of 2025:

🇺🇸 **Upcoming US Public Holidays**

📅 **October 13, 2025**
- Columbus Day
- Indigenous Peoples' Day (observed on the same date)

📅 **November 11, 2025**
- Veterans Day

📅 **November 27, 2025**
- Thanksgiving Day

📅 **December 25, 2025**
- Christmas Day

Note that Columbus Day and Indigenous Peoples' Day are both observed on October 13th, with many states and localities choosing to recognize Indigenous Peoples' Day instead of or alongside Columbus Day.



❓ Query 4: Tell me about artificial intelligence from Wikipedia
----------------------------------------------------------------------
I'll search Wikipedia for information about artificial intelligence.
Tool #4: search_wikipedia
I apologize, but I'm currently unable to access Wikipedia due to a server error (403 Forbidden). This might be a temporary issue with the Wikipedia API.

However, I can provide you with some general information about artificial intelligence:

🤖 **Artificial Intelligence (AI)** is a broad field of computer science focused on creating systems that can perform tasks that typically require human intelligence. Key aspects include:

**Main Areas:**
- Machine Learning
- Natural Language Processing
- Computer Vision
- Robotics
- Expert Systems

**Types of AI:**
- **Narrow AI** (current systems that excel at specific tasks)
- **General AI** (hypothetical human-level intelligence)
- **Superintelligence** (theoretical AI exceeding human capabilities)

**Applications:**
- Virtual assistants
- Autonomous vehicles
- Medical diagnosis
- Financial trading
- Content recommendation systems

If you'd like more detailed or specific information about AI, please let me know what particular aspect interests you, and I can try the Wikipedia search again or provide more targeted information.I apologize, but I'm currently unable to access Wikipedia due to a server error (403 Forbidden). This might be a temporary issue with the Wikipedia API.

However, I can provide you with some general information about artificial intelligence:

🤖 **Artificial Intelligence (AI)** is a broad field of computer science focused on creating systems that can perform tasks that typically require human intelligence. Key aspects include:

**Main Areas:**
- Machine Learning
- Natural Language Processing
- Computer Vision
- Robotics
- Expert Systems

**Types of AI:**
- **Narrow AI** (current systems that excel at specific tasks)
- **General AI** (hypothetical human-level intelligence)
- **Superintelligence** (theoretical AI exceeding human capabilities)

**Applications:**
- Virtual assistants
- Autonomous vehicles
- Medical diagnosis
- Financial trading
- Content recommendation systems

If you'd like more detailed or specific information about AI, please let me know what particular aspect interests you, and I can try the Wikipedia search again or provide more targeted information.



❓ Query 5: Get me the latest technology news
----------------------------------------------------------------------
I'll get the latest technology news headlines for you.
Tool #5: get_news_headlines
I apologize, but I don't have access to the NewsAPI at the moment because an API key is required. To get real-time technology news headlines, you would need to:

📰 **To Set Up News Access:**

1. **Sign up at NewsAPI.org** (they offer a free tier)
2. **Get your API key** from your dashboard
3. **Add the key** to your environment configuration

**Free Tier Includes:**
- Up to 1,000 requests per day
- Access to top headlines
- Search through news articles
- Multiple news sources

**Alternative Options:**
- Visit major tech news websites directly (TechCrunch, Ars Technica, The Verge, etc.)
- Use RSS feeds from technology publications
- Check Google News technology section

Would you like me to help you with any other information using the available tools, such as weather, exchange rates, holidays, or Wikipedia searches?I apologize, but I don't have access to the NewsAPI at the moment because an API key is required. To get real-time technology news headlines, you would need to:

📰 **To Set Up News Access:**

1. **Sign up at NewsAPI.org** (they offer a free tier)
2. **Get your API key** from your dashboard
3. **Add the key** to your environment configuration

**Free Tier Includes:**
- Up to 1,000 requests per day
- Access to top headlines
- Search through news articles
- Multiple news sources

**Alternative Options:**
- Visit major tech news websites directly (TechCrunch, Ars Technica, The Verge, etc.)
- Use RSS feeds from technology publications
- Check Google News technology section

Would you like me to help you with any other information using the available tools, such as weather, exchange rates, holidays, or Wikipedia searches?


======================================================================
✨ Demo complete!

Note: Some APIs require keys. Check the .env.example for setup:
  NEWS_API_KEY=your_key_here  # Get free key at https://newsapi.org
======================================================================
"""