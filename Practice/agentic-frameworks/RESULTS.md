# Results: ADK vs Microsoft Agent Framework 🐉

Tested on **18 June 2026**. Same Sparky persona, same tools, same model
(`gpt-4o-mini` on Azure Foundry), keyless Entra ID auth. Only the framework changed.

## Both agents passed ✅

Identical three prompts, identical tool behaviour, identical model. Sample output:

### Google ADK
```
🧒 Kid: Hi Sparky! Can you give me your biggest roar, level 10?
🐉 Sparky: RAAAAAAAAAAAWR!!!!!!!!!! 🐉✨ That was a big, brave roar! Did it make you giggle?

🧒 Kid: How many sleeps until my birthday if it's in 5 days?
🐉 Sparky: Yay! Just 5 sleeps until your big birthday adventure! 🎉🎂🐉

🧒 Kid: Why is the sky blue? Tell me like I'm 6.
🐉 Sparky: Ooooh, the sky is blue because of the sunlight! ☀️ ... a big blue blanket! 💙
```

### Microsoft Agent Framework
```
🧒 Kid: Hi Sparky! Can you give me your biggest roar, level 10?
🐉 Sparky: 🎉 RAAAAAAAAAAAWR!!!!!!!!!! 🎉 That was my biggest roar! Did it tickle your ears?

🧒 Kid: How many sleeps until my birthday if it's in 5 days?
🐉 Sparky: Hooray! 🎉 Just 5 sleeps until your birthday! 💤🐉

🧒 Kid: Why is the sky blue? Tell me like I'm 6.
🐉 Sparky: Oh, yay! 🌈 The sky is blue because of something called "light magic"! ☀️ ...
```

Both correctly called `roar(10)` -> `RAAAAAAAAAAAWR!!!!!!!!!!` and `count_sleeps(5)` -> `5 sleeps`.

## Developer-experience notes 📝

| Aspect | Google ADK | Microsoft Agent Framework |
|--------|------------|---------------------------|
| Install | `google-adk` + `litellm` | `agent-framework` (pre-release, pulls many extras) |
| Lines of glue code | ~A few more (needs a `Runner` + `Session` to invoke) | Slightly fewer (`client.as_agent(...).run(...)`) |
| Azure (non-Gemini) model wiring | Via `LiteLlm("azure/<deployment>")` adapter | Native `azure_endpoint` on the OpenAI client |
| Keyless Entra auth | Pass `azure_ad_token_provider` into LiteLlm | Pass `credential=AzureCliCredential()` directly |
| Tools | Plain Python functions, docstrings become schema | Plain Python functions, docstrings become schema |
| Running the agent | Explicit `Runner.run_async` event loop, yields events | `agent.run(prompt)` returns a result object |

## Gotchas hit during the build 🐛

1. **MAF is churny (pre-release).** The class moved: the older `agent_framework.azure.AzureOpenAIChatClient`
   no longer exists in v1.9.0. The Azure path is now via `agent_framework.openai`:
   - `OpenAIChatClient` -> uses the **Responses API** (needs `api_version="preview"`).
   - `OpenAIChatCompletionClient` -> uses **chat completions** (accepts `2024-10-21`). We used this
     to stay apples-to-apples with ADK's transport.
2. **API version error.** The Responses-API client rejected `2024-10-21` / `2025-01-01-preview` with
   `API version not supported`. Switching to the chat-completions client fixed it.
3. **Local auth disabled.** The Foundry resource has `disableLocalAuth=true`, so API keys can't be
   listed - keyless Entra ID is mandatory (which is the nicer path anyway).
4. **Windows console + emoji.** `cp1252` stdout choked on 🧒. Both scripts now call
   `sys.stdout.reconfigure(encoding="utf-8")`.

## Verdict

For this trivial single-agent case the two are **functionally identical** - same model, same tools,
same quality of answer. The real differences are ergonomic: ADK needs an explicit `Runner`/`Session`
to drive the agent and routes non-Gemini models through LiteLLM, while MAF has native Azure wiring and
a one-line `run()` but is still pre-release and shifting under your feet. Pick by cloud gravity, not capability.
