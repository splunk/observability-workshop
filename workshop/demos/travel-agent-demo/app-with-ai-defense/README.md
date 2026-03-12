# Multi-Agent Travel Planner with AI Defense Gateway Mode

A multi-agent travel planning system that demonstrates **Cisco AI Defense Gateway Mode** 
- where LLM calls are proxied through AI Defense Gateway for security inspection.

## Gateway Mode vs SDK Mode

| Aspect | SDK Mode | Gateway Mode |
|--------|----------|--------------|
| **How it works** | Explicit `inspect_prompt()` calls | LLM calls proxied through gateway |
| **Event ID source** | Response body from AI Defense API | `X-Cisco-AI-Defense-Event-Id` header |
| **Span structure** | Separate AI Defense spans | Event ID added to existing LLM spans |
| **Code changes** | Add security check calls | Change LLM base URL only |

## How Event ID is Captured

1. LLM call goes to AI Defense Gateway URL
2. Gateway inspects request, forwards to LLM provider
3. Gateway inspects response, adds `X-Cisco-AI-Defense-Event-Id` header
4. `AIDefenseInstrumentor` (via httpx wrapper) extracts header
5. Event ID added to current span (LangChain's ChatOpenAI span)

## Setup

```bash
# Add your AI Defense Gateway URL and Azure OpenAI API Key
export AZURE_OPENAI_ENDPOINT="https://gateway.aidefense.security.cisco.com/{tenant}/connections/{conn}"
export AZURE_OPENAI_API_KEY=your_api_key 

export AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini 
export AZURE_OPENAI_API_VERSION=2025-01-01-preview 
export OPENAI_MODEL=gpt-4.1-mini 
```

### Running the Example

```bash
# Run
cd app-with-ai-defense
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Telemetry

In Gateway Mode, the `gen_ai.security.event_id` is added to the **existing LangChain spans**, not separate AI Defense spans:

```json
{
    "name": "ChatOpenAI",
    "attributes": {
        "gen_ai.request.model": "gpt-4o-mini",
        "gen_ai.response.id": "chatcmpl-...",
        "gen_ai.security.event_id": "e91a8f7a-77ec-11f0-988b-220941ce26ae"
    }
}
```

This provides seamless integration with your existing LLM telemetry.

## Custom Gateway URLs

If you have a custom AI Defense Gateway deployment, you can add URL patterns:

```bash
export OTEL_INSTRUMENTATION_AIDEFENSE_GATEWAY_URLS="custom-gateway.internal,my-proxy.corp"
```

The instrumentation will check both built-in patterns and custom patterns.

## Supported LLM SDKs

Gateway Mode supports any LLM SDK that uses httpx for HTTP requests:
- **OpenAI SDK** (sync and async)
- **Azure OpenAI** (via OpenAI SDK with Azure base URL)
- **Cohere SDK**
- **Mistral SDK**
- **AWS Bedrock** (via botocore)

## References

- [AI Defense Gateway Documentation](https://securitydocs.cisco.com/docs/ai-def/user/105487.dita)
- [AI Defense SDK Mode Example](../../multi_agent_travel_planner/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)