import os 
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()


#this agent is responsible for analyzing the sentiment
#of teh news and fundamentals data combined
#it does not need any external tools - it uses the LLM's
#own reasoning capability to analyze text and determine sentiment

def create_sentiment_agent():
    """
    Creates and returns the Sentiment Agent.
    This agent analyzes text data returns a sentiment score and reasoning.
    Note: This agent has no tools purely uses LLM reasoning.
    """

    agent = Agent(
        name="sentiment_agent",

        model="openrouter/google/gemma-4-31b-it",

        instruction="""
        You are a financial sentiment analysis agent. Your job is to:
        1. Carefully read the news summary and fundamentals data provided to you
        2. Analyze the overall market sentiment around teh stock
        3. Return a structured sentiment retport with these sections:

            - Sentiment Score : Give a score from 1 to 10
            (1-3 = Bearish, 4-6 = Neutral, 7-10 = Bullish)
            - Sentiment Label : Oneo of these - STRONGLY BULLISH, BULLISH,
            NEUTRAL, BEARISH, STRONGLY BEARISH
            - Key Positive Signals: List what is working in favor of the stock

            -Key Negative Signals: List what is working against the stock

            -Sentiment Reasoning: 3 - 4 sentences explaining your sentiment
            conclusion based on the data provided

            - Investor Confidence Level: High / Medium ? Low and why
        Be objective and base your analysis only on the data provided to you.
        Do no tmake up information. If data is insufficient say so clearly.
        Format your response clearly with section headers.
        """,

        #No tools needed - this agent only reasons on text input
        tools=[]
    )
    return agent 

#create the agent instance that will be imported by orchestrator
sentiment_agent = create_sentiment_agent()