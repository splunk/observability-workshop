---
title: 7. Run With a Local or API LLM
linkTitle: 7. Run With an LLM
weight: 7
time: 10 minutes
---

The workshop agent uses a local LLM by default. The same file can also use a hosted
OpenAI-compatible endpoint when you have an API key.

The example uses the OpenAI-compatible `chat/completions` shape because it works with
[Ollama's OpenAI-compatible API](https://docs.ollama.com/api/openai-compatibility) and
hosted providers that expose the
[OpenAI Chat Completions API](https://developers.openai.com/api/reference/chat-completions/overview/).
OpenAI recommends the Responses API for new OpenAI-native projects, but this workshop
uses chat completions to keep one code path for local and hosted endpoints.

It supports two backend modes:

* `ollama`: a local LLM exposed through Ollama's OpenAI-compatible endpoint.
* `openai`: an OpenAI-compatible hosted endpoint that uses an API key.

## Run With a Local LLM

Start Ollama and make sure a chat model is available. The example below uses `llama3.2`,
but you can use another local model that works well at instruction following.

```bash
ollama pull llama3.2
python3 agent.py "Plan my day and draft a customer follow-up"
```

By default, the script calls:

```text
http://localhost:11434/v1/chat/completions
```

If your local model server uses a different base URL, set `OLLAMA_BASE_URL`:

```bash
AGENT_BACKEND=ollama \
OLLAMA_BASE_URL="http://localhost:11434/v1" \
OLLAMA_MODEL="llama3.2" \
python3 agent.py "Draft a concise status update"
```

## Run With an API Key

Set `AGENT_BACKEND=openai`, provide a key, and choose a model available to your account:

```bash
OPENAI_API_KEY="your-key" \
OPENAI_MODEL="your-model" \
AGENT_BACKEND=openai \
python3 agent.py "Plan my day and draft a customer follow-up"
```

The default hosted base URL is:

```text
https://api.openai.com/v1
```

If you use another OpenAI-compatible provider or gateway, set `OPENAI_BASE_URL`:

```bash
OPENAI_API_KEY="your-key" \
OPENAI_BASE_URL="https://your-provider.example/v1" \
OPENAI_MODEL="your-model" \
AGENT_BACKEND=openai \
python3 agent.py "Create a task and draft a follow-up"
```

## What Changes With an API Key

The tools do not change. The safety boundary does not change. The only difference is
which model endpoint is called. In both local and hosted modes, the script sends the
request, observations, and tool descriptions to the model:

```python
decide_next_action_with_model(state, model_config)
```

The model must return JSON in this shape:

```json
{
  "tool_name": "lookup_profile",
  "arguments": {
    "section": "current_goals"
  }
}
```

The script then validates the action before calling any tool. If the model returns an
unknown tool, repeats a tool, or sends invalid arguments, the script stops with a clear
error instead of calling unsafe or unknown code.

{{% notice title="Important" style="info" %}}
The API-key version still uses the workshop's tool allowlist. A model can request a tool,
but Python decides whether that tool is registered and whether the arguments are valid.
That separation is a core safety pattern for agent design.
{{% /notice %}}
