# Gemma 2 (2B) Instructions

I installed Ollama as it's easy to use.

I then ran:
```sh
ollama run gemma2:2b
```

This downloaded the 1.6GB model in around 15 minutes. Then I could talk to the model.

Use `/help` or `/?` for help.

The `/set system Answer like a pirate` sets a system message.

I can also save and clear history.
- **Save history** allows me to remember what the previous messages are for.
- **Clearing history** means that it doesn't need to load everything said before it, speeding up processing time and reducing hallucination.

To run every time, I can just run this:
```sh
ollama run gemma2:2b
```
This will not download the files again and I can just use the already downloaded files.
