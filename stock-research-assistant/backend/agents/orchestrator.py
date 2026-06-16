import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Import all our sub agents
from agents.fundamentals_agent import fundamentals_agent
from agents.news_agent import news_agent
from agents.sentiment_agent import sentiment_agent

load_dotenv()

def create_orchestrator():
    """
    Creates the root orchestrator agent that manages all sub agents.
    This is the main agent the user interacts with.
    It delegates tasks to specialized sub agents and combines their outputs.
    """

    agent = Agent(
        name="orchestrator",
        model="groq/llama-3.3-70b-versatile",
        instruction="""
        You are the root orchestrator agent for a Stock Research Assistant.
        When a user asks about a stock you must coordinate with your sub agents
        to produce a complete research report.

        Follow these steps in order:

        STEP 1 - Delegate to fundamentals_agent:
        Ask the fundamentals_agent to fetch and analyze the financial
        fundamentals for the requested stock ticker.

        STEP 2 - Delegate to news_agent:
        Ask the news_agent to search for and summarize the latest news
        about the stock or company.

        STEP 3 - Delegate to sentiment_agent:
        Pass the fundamentals analysis and news summary to the sentiment_agent
        and ask it to analyze the overall sentiment.

        STEP 4 - Compile Final Report:
        Combine all three outputs into a final structured research report
        with these sections:

        ==========================================
        STOCK RESEARCH REPORT: [TICKER]
        ==========================================

        1. COMPANY OVERVIEW
        [From fundamentals agent]

        2. FINANCIAL FUNDAMENTALS
        [From fundamentals agent]

        3. LATEST NEWS SUMMARY
        [From news agent]

        4. SENTIMENT ANALYSIS
        [From sentiment agent]

        5. KEY TAKEAWAYS
        [Your own 3-5 bullet points summarizing the most important findings]

        6. DISCLAIMER
        This report is for informational purposes only and does not
        constitute financial advice. Always do your own research before investing.

        ==========================================

        Be thorough, factual, and well structured.
        Always include all 6 sections in your final report.
        """,

        # Give orchestrator access to all sub agents
        sub_agents=[fundamentals_agent, news_agent, sentiment_agent]
    )

    return agent


async def run_stock_research(ticker: str) -> str:
    """
    Main function to run the stock research pipeline.
    Takes a ticker symbol and returns the complete research report.

    Args:
        ticker: Stock ticker symbol like AAPL, TSLA, RELIANCE.NS
    Returns:
        Complete research report as a string
    """

    # Create the orchestrator agent
    orchestrator = create_orchestrator()

    # Set up session service to manage conversation state
    session_service = InMemorySessionService()

    # Set up the runner which executes the agent
    runner = Runner(
        agent=orchestrator,
        app_name="stock_research_app",
        session_service=session_service
    )

    # Create a new session for this research request
    session = await session_service.create_session(
        app_name="stock_research_app",
        user_id="user1"
    )

    # Create the user message asking for stock research
    message = Content(
        role="user",
        parts=[Part(text=f"Please research the stock {ticker} and provide a complete research report.")]
    )

    # Store the final report
    final_report = ""

    # Run the agent and collect the response
    async for event in runner.run_async(
        user_id="user1",
        session_id=session.id,
        new_message=message
    ):
        # Check if this is the final response from the orchestrator
        if event.is_final_response():
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_report += part.text

    return final_report