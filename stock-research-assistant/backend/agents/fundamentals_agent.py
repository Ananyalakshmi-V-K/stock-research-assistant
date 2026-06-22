import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from tools.stock_tool import get_stock_fundamentals

load_dotenv()


#This agent is responsible for fetching and analyzing
#the financial fundamentals of a stock
#it uses the get_stock_fundamentals tool we built earlier

def create_fundamentals_agent():
    """
    Creates and returns the fundamentals agent;
    This agent takes a stock ticker and returns key financial metrics.
    """

    #we wrap our tool function so ADK can use it
    #ADK needs functions with clear docstrings to understand when to call them

    def fetch_stock_fundamentals(ticker: str) -> dict:
        """
        Fetches the financial fundamentals for a given stock ticker symbol.
        Use this tool when yu need financial data like PE ratio, market cap, revenue, profit margin,
        and other key metrics for a stock
        
        Args:
            ticker: The stock ticker symbol e.g. AAPL for Apple,
            TSLA for Tesla, RELIANCE.NS for Reliance Industries
        Returns :
            Dictionary containing key financial metrics
        
        """
        return get_stock_fundamentals(ticker)
    
    agent = Agent(
        name = "fundamentals_agent",
        
        #using groq with llama as we set up earlier
        model="openrouter/google/gemma-4-31b-it",

        #this instruction tells the agent what its role is
        #and how it should behavve
        instruction="""
        You are a financial data analyst agent. Your job is to :
        1. Fetch stock fundamental data using the fetch_stock_fundamentals tool
        2. Analyze the key metrics and identify strengths and weaknesses
        3. Return a structured analysis with teh following sections:
            - Company Overview (name, sector, industry, what they do)
            - Key Metrics (price, market cap, PE ratio, EPS)
            - Financial Health (revenue, profit margin, debt to equity)
            - 52 Week perfomane (high,low , current position)
            - Brief Assessment (2-3 sentences on overall financial health)
        
        Always be factual and based only on the data provided by the tool.
        Format your response clearly with section headers.
        """,

        #Give the agent access to the fundamentals tool
        tools = [fetch_stock_fundamentals]
    )
    return agent
#create the agent instance that will be imported by orchestrator
fundamentals_agent = create_fundamentals_agent()