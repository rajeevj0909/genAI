# Agentic Frameworks: ADK vs Microsoft Agent Framework 🐉

A tiny, hands-on bake-off. **Same agent, same model, two frameworks.** The only thing that
changes between the two folders is the framework plumbing, so you can feel the difference
in the developer experience side by side.

## The shared idea: Sparky the Baby Dragon

**Sparky** is a friendly, giggly baby dragon who is best friends with curious kids. 🐲
He explains things in super simple, silly words a 6-year-old would love, and he has two fun tools:

| Tool | What it does |
|------|--------------|
| `roar(loudness)` | Lets out a dragon roar at a chosen loudness (1-10) |
| `count_sleeps(days)` | Counts how many "sleeps" until a big adventure |

## What is kept identical (the controlled variables)

- **Model:** Azure OpenAI `gpt-4o-mini` (on the `FoundryRajeevJ0909` Foundry resource)
- **Auth:** Keyless Entra ID via `AzureCliCredential` (uses your `az login`, no API keys on disk)
- **Persona / instructions:** identical Sparky system prompt
- **Tools:** identical `roar` and `count_sleeps` Python functions
- **Test prompts:** identical three prompts

## What changes (the independent variable)

| | `google-adk/` | `microsoft-agent-framework/` |
|---|---|---|
| Framework | Google Agent Development Kit | Microsoft Agent Framework |
| Package | `google-adk`, `litellm` | `agent-framework` (pre-release) |
| Agent class | `LlmAgent` + `Runner` | `ChatAgent` via `AzureOpenAIChatClient` |
| Model wiring | `LiteLlm("azure/gpt-4o-mini")` | `AzureOpenAIChatClient(deployment_name=...)` |
| Tool format | plain Python functions | plain Python functions |

## Prerequisites

1. `az login` (already done on this machine) with access to `FoundryRajeevJ0909`.
2. Python 3.13.

## Run it

Each folder is self-contained with its own virtual env and `requirements.txt`.

```powershell
# Google ADK
cd google-adk
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python sparky_adk.py

# Microsoft Agent Framework
cd ..\microsoft-agent-framework
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python sparky_af.py
```

## Findings

See `RESULTS.md` (written after the first test run) for the side-by-side output and notes.
