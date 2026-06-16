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