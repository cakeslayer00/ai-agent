# ai-agent

A tiny command-line coding agent. You give it a prompt, and it talks to an LLM (through OpenRouter) that can actually poke around a small sandboxed project on its own — listing files, reading them, writing changes, and running Python. It keeps looping, calling those tools and feeding the results back to the model, until it has an answer for you. All file access is locked to the `./calculator` working directory so the agent can't wander off and touch the rest of your machine.

## Usage

```bash
uv run main.py "your prompt here" [--verbose]
```

Set `OPENROUTER_API_KEY` in a `.env` file first.
