import asyncio
from agents.orchestrator import create_orchestrator
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

    print("\n---ALL EVENTS---")
    async for event in runner.run_async(
        user_id="user1",
        session_id=session.id,
        new_message=message
    ):
        print(f"Event author: {event.author}")
        if hasattr(event, 'content') and event.content:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"Text: {part.text[:200]}")
        print("---")

asyncio.run(test_orchestrator_debug())