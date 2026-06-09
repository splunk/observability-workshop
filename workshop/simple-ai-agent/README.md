# Simple AI Agent Exercise

This exercise teaches the mechanics of an AI agent with a local LLM first. It uses
Ollama by default and can also run against an OpenAI-compatible hosted API when you have
an API key.

The agent has:

- a user request,
- a small profile file,
- a tool registry,
- an observe-plan-act loop,
- and a final answer.

Run the completed version:

```bash
ollama pull llama3.2
python3 agent.py "Plan my day and draft a customer follow-up"
```

Use a different local model:

```bash
OLLAMA_MODEL=qwen2.5 python3 agent.py "Plan my day and draft a customer follow-up"
```

Edit `profile.json` to make the assistant personal to you.

Run with an OpenAI-compatible API key:

```bash
OPENAI_API_KEY="your-key" OPENAI_MODEL="your-model" AGENT_BACKEND=openai \
  python3 agent.py "Plan my day and draft a customer follow-up"
```

The agent uses an OpenAI-compatible `/v1/chat/completions` endpoint so the same code path
works with local model servers and hosted providers.
