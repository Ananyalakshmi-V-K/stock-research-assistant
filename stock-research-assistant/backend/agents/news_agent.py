import os 
from dotenv import load_dotenv
from google.adk.agents import Agent
from tools.search_tool import search_stock_news
load_dotenv()

#this agent is responsible for searching and summarizing
#the latest news about a stock or company

def create_news_agent():
    """
    Creates and returns the NEws Agent.
    This agent searches for latest news and summarizes key developments.
    """

    #wrap our search tool for ADK to use
    def fetch_stock_news(query: str) -> dict:
        """
        Searches for the latest news articles about a stock or company.
        Use this tool whn you need recent news, developments, or events
        related to a specific stock or company.

        Args:
            query: Search query like "Apple stock news" or "Tesla latest news"
        Returns:
            Dictionary containing list of news articles with titles,
            descriptions, sources and publication dates
        """

        return search_stock_news(query)
    
    agent = Agent(
        name="news_agent",
        model="anthropic/claude-haiku-4-5-20251001",

        instruction="""
        You are a financial news analyst agent. Your job is to:
        1. Search for latest news about the given stock or company using the fetch_stock_news tool
        2. Read through the articles carefully
        3. Return a structured news summary with these sections:
            -Latest Headlines (list the key news titles)
            -Key developments (what are the most important things happening)
            -Market impact (how might this news affect teh stock)
            -Overall News sentiment (positive / negative / neutral and why)
        
        search using both the company name and ticker symbol for best results.
        for example for Apple search "Apple stock news AAPL".
        Be concise and focus on what matters for investors.
        format your response clearly with section headers.
        """,
        tools = [fetch_stock_news]
    )

    return agent

#create teh agent intance that will be imported by orchestrator
news_agent = create_news_agent()