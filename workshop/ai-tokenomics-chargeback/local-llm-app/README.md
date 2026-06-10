# Local LLM Tokenomics App

This is the runnable app for the AI Tokenomics and GPU Chargeback workshop. It calls a
local Ollama model, records OpenTelemetry traces and metrics, and emits chargeback
attributes for team, tenant, cost center, workload, and model.

## Prerequisites

Install and start Ollama:

```bash
ollama pull llama3.2:1b
ollama serve
```

Run a local OpenTelemetry Collector or Splunk OpenTelemetry Collector on
`localhost:4317`, or set `OTEL_EXPORTER_OTLP_ENDPOINT` to your collector endpoint.

## Run the App

```bash
cd workshop/ai-tokenomics-chargeback/local-llm-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OLLAMA_MODEL=llama3.2:1b
export INPUT_USD_PER_1M=0.20
export OUTPUT_USD_PER_1M=1.25

python app.py
```

## Send Normal Traffic

```bash
curl -s http://localhost:8080/ask \
  -H "content-type: application/json" \
  -H "x-ai-team: support-ai" \
  -H "x-ai-cost-center: cc-ml-1200" \
  -H "x-ai-tenant-id: tenant-local" \
  -d '{"question":"How should we explain AI chargeback to app teams?"}' | jq
```

## Simulate Token Surge

```bash
curl -s http://localhost:8080/ask \
  -H "content-type: application/json" \
  -H "x-ai-team: support-ai" \
  -H "x-ai-cost-center: cc-ml-1200" \
  -H "x-ai-tenant-id: tenant-local" \
  -d '{"question":"Summarize the customer context and produce a detailed plan.","scenario":"surge","num_predict":240}' | jq
```

## Simulate Misuse

```bash
curl -s http://localhost:8080/ask \
  -H "content-type: application/json" \
  -H "x-ai-team: field-ai" \
  -H "x-ai-cost-center: cc-ml-3100" \
  -H "x-ai-tenant-id: tenant-field-lab" \
  -d '{"question":"Generate a complete customer proposal with pricing and implementation details.","scenario":"misuse","num_predict":400}' | jq
```

## Simulate Unknown Attribution

```bash
curl -s http://localhost:8080/ask \
  -H "content-type: application/json" \
  -d '{"question":"Run this request without team or cost-center headers.","scenario":"unknown","num_predict":120}' | jq
```

The app records these custom metrics:

* `ai.tokens.input`
* `ai.tokens.output`
* `ai.tokens.total`
* `ai.request.count`
* `ai.request.estimated_cost_usd`
