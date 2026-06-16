import requests #for making http requests to the search API
import os #to access environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

def search_stock_news(query: str) -> dict:
    """
    Searches for latest news about a stock or company usng GNews API.

    Args:
        query: Search query string like "Apple stock news" or "AAPL latest news"
    Returns:
        Dictionary containing list of news articles
    """

    try:
        #Get the API key from environment variables 
        #we will add this key to .env file in a moment
        api_key = os.getenv("GNEWS_API_KEY")

        #Gnews API endpoint - this is the URL we send our request ot 
        #max=5 means we want maximum 5 news rticles
        #lang-en means English articles only
        url = f"https://gnews.io/api/v4/search"

        params = {
            "q" : query,
            "max" : 5,
            "lang" : "en",
            "token" : api_key
        }
        #make the actual HTTP GET request to GNews API 
        response = requests.get(url, params=params, timeout=10)

        #convert the response from JSON format to Python dictinary 
        data = response.json()

        #check if we got articles in the response
        if "articles" not in data:
            return {"error": "No articles found", "raw": data}

        #extract only the fields we need from each article
        #we don't need everything GNews returns, jus tthe important parts
        articles = []
        for article in data["articles"]:
            articles.append({
                #Headline of the news article
                "title": article.get("title", "N/A"),

                #short summary of what the article is about
                "description": article.get("description", "N/A"),

                #which news source published this (CNN, Reuters etc)
                "source": article.get("source", {}).get("name", "N/A"),

                #when was this article published 
                "published_at": article.get("publishedAt", "N/A"),

                #direct link to read th full article
                "url": article.get("url", "N/A")
            })
        return {
            "query": query,
            "total_articles": len(articles),
            "articles": articles
        }
    except Exception as e:
        #If anything goes wrong return error message instead of crashing
        return {"error": f"Failed to fetch news for query '{query}': {str(e)}"}
