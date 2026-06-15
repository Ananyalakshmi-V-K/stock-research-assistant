import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

load_dotenv()

root_agent = Agent(
    name="test_agent",
    model="groq/llama-3.3-70b-versatile",
    instruction="You are a helpful assistant. Answer the user's question simply.",
)

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="test_app",
    session_service=session_service
)

async def main():
    session = await session_service.create_session(
        app_name="test_app",
        user_id="user1"
    )

    from google.genai.types import Content, Part
    message = Content(role="user", parts=[Part(text="What is a stock market?")])

    async for event in runner.run_async(
        user_id="user1",
        session_id=session.id,
        new_message=message
    ):
        if event.is_final_response():
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        print("Agent response: ",part.text)
        
import asyncio
asyncio.run(main())