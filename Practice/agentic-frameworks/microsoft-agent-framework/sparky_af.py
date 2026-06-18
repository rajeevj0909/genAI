# Sparky the Baby Dragon - Microsoft Agent Framework edition 🐉
#
# Same persona, same tools, same model as the Google ADK version.
# Only the framework plumbing is different.

import asyncio
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agent_framework.openai import OpenAIChatCompletionClient
from azure.identity import AzureCliCredential

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
    """Let out a dragon roar at a chosen loudness from 1 (tiny) to 10 (HUGE)."""
    level = max(1, min(10, loudness))
    return "RA" + "A" * level + "WR" + "!" * level


def count_sleeps(days: int) -> str:
    """Count how many sleeps (nights) until a big adventure."""
    sleeps = max(0, days)
    if sleeps == 0:
        return "It's TODAY! The adventure is right now! 🐉"
    return f"Just {sleeps} sleeps until your big adventure! 😴🐲"


PROMPTS = [
    "Hi Sparky! Can you give me your biggest roar, level 10?",
    "How many sleeps until my birthday if it's in 5 days?",
    "Why is the sky blue? Tell me like I'm 6.",
]


async def main() -> None:
    client = OpenAIChatCompletionClient(
        model=DEPLOYMENT,
        azure_endpoint=ENDPOINT,
        api_version=API_VERSION,
        credential=AzureCliCredential(),
    )
    sparky = client.as_agent(
        name="Sparky",
        instructions=INSTRUCTIONS,
        tools=[roar, count_sleeps],
    )

    print("=== Sparky (Microsoft Agent Framework) ===\n")
    for prompt in PROMPTS:
        print(f"🧒 Kid: {prompt}")
        result = await sparky.run(prompt)
        print(f"🐉 Sparky: {result.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
