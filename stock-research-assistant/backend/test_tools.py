'''
from tools.search_tool import search_stock_news
import os
from dotenv import load_dotenv

load_dotenv()  # Make sure .env is loaded

# Check if key is being read
print("API Key:", os.getenv("GNEWS_API_KEY"))

result = search_stock_news("Apple stock news")
print("Raw result:", result)  # Print raw result to see the actual error

#we import the function we just wrote from the tools folder
#python finds tools/stock_tool.py because we're running from the backed folder
from tools.stock_tool import get_stock_fundamentals

#test with Apple's ticker symbol
#for Indian stocks you would use "RELIANCE.NS" or "TCS.NS" etc
result = get_stock_fundamentals("AAPL")

#Loop through all key-value pairs in the result dictionary and print them 
#this gives us a clean readae output to verify everything is working
for key, value in result.items():
    print(f"{key}: {value}")

from tools.search_tool import search_stock_news
#Test with Apple news search
result = search_stock_news("Apple stock news")

#print the query and total articles found
print(f"\nQuery: {result['query']}")
print(f"Total Articles Found: {result['total_articles']}")
print("\n---ARTICLES---")

#Loop through each articles and print its details

for i, article in enumerate(result['articles'], 1):
    print(f"\nArticle {i}:")
    print(f"  Title: {article['title']}")
    print(f"  Source: {article['source']}")
    print(f"  Published: {article['published_at']}")
    print(f"  Description: {article['description']}")
    print(f"  URL: {article['url']}")

import asyncio 
from agents.orchestrator import run_stock_research


async def test_orchestrator():
    print("\n\nRunning full stock research pipeline...")
    print("This may take 30-6- seconds\n")
    report = await run_stock_research("AAPL")
    print(report)

asyncio.run(test_orchestrator())'''

import asyncio
from agents.orchestrator import create_orchestrator, run_stock_research
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

async def test_orchestrator_debug():
    orchestrator = create_orchestrator()
    session_service = InMemorySessionService()
    runner = Runner(
        agent=orchestrator,
        app_name="stock_research_app",
        session_service=session_service
    )
    session = await session_service.create_session(
        app_name="stock_research_app",
        user_id="user1"
    )
    message = Content(
        role="user",
        parts=[Part(text="Please research the stock AAPL and provide a complete research report.")]
    )

    print("\n--- ALL EVENTS ---")
    async for event in runner.run_async(
        user_id="user1",
        session_id=session.id,
        new_message=message
    ):
        # Print every event to see what agents are being called
        print(f"Event author: {event.author}")
        if hasattr(event, 'content') and event.content:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"Text: {part.text[:200]}")
        print("---")

asyncio.run(test_orchestrator_debug())