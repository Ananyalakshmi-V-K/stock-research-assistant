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

#import os
import litellm
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
# Map the model name without :free to use the free endpoint
litellm.model_alias_map = {
    "openrouter/google/gemma-4-31b-it": "openrouter/google/gemma-4-31b-it:free"
}
def create_orchestrator():
    """
    Creates the root orchestrator agent that manages all sub agents.
    This is the main agent the user interacts with.
    It delegates tasks to specialized sub agents and combines their outputs.
    """

    agent = Agent(
        name="orchestrator",
        model="openrouter/google/gemma-4-31b-it",
        instruction="""
        You are the root orchestrator agent for PRISM - a Stock Research Assistant.
        You MUST call ALL THREE sub agents before giving a final response.
        Do NOT stop after calling just one agent.

        You have access to these sub agents:
        - fundamentals_agent: fetches financial data
        - news_agent: fetches latest news
        - sentiment_agent: analyzes sentiment

        MANDATORY STEPS - complete ALL of them:
        STEP 1: Call fundamentals_agent with the stock ticker. Wait for response.
        STEP 2: Call news_agent with the company name and ticker. Wait for response.
        STEP 3: Call sentiment_agent with teh combined data from steps 1 and 2. Wait for response.
        STEP 4: Only after ALL THREE agents have responded, compile the final report.

        Final report must have these sections:
        ===========================================
        STOCK RESEARCH REPORT: [TICKER]
        ===========================================
        1. COMPANY OVERVIEW
        2. FINANCIAL FUNDAMENTALS
        3. LATEST NEWS SUMMARY 
        4. SENTIMENT ANALYSIS
        5. KEY TAKEAWAYS
        6. DISCLAIMER
        ===========================================

        IMPORTANT: You are NOT done until you have responses from ALL THREE afents.
        Do not skip any agent. Do not combine steps.
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