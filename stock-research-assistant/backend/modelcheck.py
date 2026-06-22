import litellm
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENROUTER_API_KEY'] = os.getenv('OPENROUTER_API_KEY')
import asyncio

# These are the best candidates for function calling and agent use
models_to_test = [
    "openrouter/google/gemma-4-31b-it:free",
    "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free",
    "openrouter/qwen/qwen3-next-80b-a3b-instruct:free",
    "openrouter/nex-agi/nex-n2-pro:free",
]

async def test_model(model):
    try:
        response = await litellm.acompletion(
            model=model,
            messages=[{'role': 'user', 'content': 'Say hello in one word'}],
            timeout=30
        )
        print(f"✓ {model} works!")
        print(f"  Response: {response.choices[0].message.content[:100]}")
    except Exception as e:
        print(f"✗ {model} failed: {str(e)[:100]}")

async def main():
    for model in models_to_test:
        await test_model(model)

asyncio.run(main())