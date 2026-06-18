# Sparky the Baby Dragon - Google ADK edition 🐉
#
# Same persona, same tools, same model as the Agent Framework version.
# Only the framework plumbing is different.

import asyncio
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.genai import types
from azure.identity import AzureCliCredential, get_bearer_token_provider

ENDPOINT = "https://foundryrajeevj0909.cognitiveservices.azure.com/"
DEPLOYMENT = "gpt-4o-mini"
API_VERSION = "2024-10-21"

INSTRUCTIONS = (
    "You are Sparky, a friendly, giggly baby dragon who is best friends with curious kids. "
    "Explain everything in super simple, fun words a 6-year-old would understand. "
    "Keep answers short, cheerful and a little bit silly, and sprinkle in dragon emojis. "
    "When a kid asks you to roar, use the `roar` tool. "
    "When a kid asks how many sleeps until something, use the `count_sleeps` tool."
)


# ---- Sparky's tools (identical across both frameworks) ----

def roar(loudness: int) -> str:
    """Let out a dragon roar at a chosen loudness from 1 (tiny) to 10 (HUGE).

    Args:
        loudness: How loud the roar should be, 1 to 10.
    """
    level = max(1, min(10, loudness))
    return "RA" + "A" * level + "WR" + "!" * level


def count_sleeps(days: int) -> str:
    """Count how many sleeps (nights) until a big adventure.

    Args:
        days: Number of days until the adventure.
    """
    sleeps = max(0, days)
    if sleeps == 0:
        return "It's TODAY! The adventure is right now! 🐉"
    return f"Just {sleeps} sleeps until your big adventure! 😴🐲"


token_provider = get_bearer_token_provider(
    AzureCliCredential(), "https://cognitiveservices.azure.com/.default"
)

sparky = LlmAgent(
    name="Sparky",
    model=LiteLlm(
        model=f"azure/{DEPLOYMENT}",
        api_base=ENDPOINT,
        api_version=API_VERSION,
        azure_ad_token_provider=token_provider,
    ),
    instruction=INSTRUCTIONS,
    tools=[roar, count_sleeps],
)

PROMPTS = [
    "Hi Sparky! Can you give me your biggest roar, level 10?",
    "How many sleeps until my birthday if it's in 5 days?",
    "Why is the sky blue? Tell me like I'm 6.",
]


async def main() -> None:
    runner = InMemoryRunner(agent=sparky, app_name="sparky")
    session = await runner.session_service.create_session(
        app_name="sparky", user_id="kid"
    )
    print("=== Sparky (Google ADK) ===\n")
    for prompt in PROMPTS:
        print(f"🧒 Kid: {prompt}")
        content = types.Content(role="user", parts=[types.Part(text=prompt)])
        async for event in runner.run_async(
            user_id="kid", session_id=session.id, new_message=content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print(f"🐉 Sparky: {event.content.parts[0].text}\n")


if __name__ == "__main__":
    asyncio.run(main())
