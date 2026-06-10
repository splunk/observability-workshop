# Environment Setup

This page explains the runtime environment.

## 1. Create `.env`

```bash
cp .env.example .env
```

Then populate values you actually have.

## 2. Student identity

Each student should use a unique `INSTANCE`.

```dotenv
INSTANCE=student-001
OTEL_RESOURCE_ATTRIBUTES=lab.name=ciscolive26,lab.student.id=student-001,service.instance.id=student-001,host.name=student-001,deployment.environment=demo
```

In a shared Splunk Observability Cloud account, this is what lets students filter to their own lab data.

## 3. Minimum useful values

```dotenv
SPLUNK_ACCESS_TOKEN=...
SPLUNK_REALM=...
OPENAI_API_KEY=...
GALILEO_API_KEY_FILE=/path/to/galileo_api_key
```

The stack can run without these values, but live Splunk export, MCP evidence intake, model-backed remediation, and Galileo agent monitoring will be limited. You can set `GALILEO_API_KEY` directly for local-only runs, but `GALILEO_API_KEY_FILE` keeps the secret out of shell history and process arguments. MCP uses the direct Observability endpoint by default:

```dotenv
SPLUNK_MCP_ENABLED=true
SPLUNK_MCP_URL=
```

## 4. Collector export

For local collector export, use the high host port:

```dotenv
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:14318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

Inside Docker Compose, services use `http://splunk-otel-collector:4318`.

## 5. App ports

Defaults:

```dotenv
ORCHESTRATOR_PORT=18110
API_GATEWAY_PORT=18100
ASSISTANT_SERVICE_PORT=18101
CASE_SERVICE_PORT=18102
KNOWLEDGE_SERVICE_PORT=18103
SCENARIO_CONTROLLER_PORT=18104
REMEDIATION_AGENT_PORT=18800
```

Frontend URLs:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:18100
VITE_ORCHESTRATOR_BASE_URL=http://127.0.0.1:18110
VITE_SCENARIO_CONTROLLER_BASE_URL=http://127.0.0.1:18104
```

## 6. Cache pressure controls

```dotenv
CLAIMS_KNOWLEDGE_CACHE_DIR=/tmp/ciscolive26-${INSTANCE}/claims-knowledge-cache
SPLUNK_CACHE_MOUNTPOINT=/var/cache/claims-knowledge
CLAIMS_KNOWLEDGE_CACHE_UTILIZATION_METRIC=claims_knowledge.cache.utilization
SPLUNK_CACHE_UTILIZATION_METRIC=claims_knowledge.cache.utilization
CLAIMS_KNOWLEDGE_CLAIM_STATUS_LATENCY_METRIC=claims_knowledge.claim_status.latency_ms
SPLUNK_CLAIM_STATUS_LATENCY_METRIC=claims_knowledge.claim_status.latency_ms
CLAIMS_KNOWLEDGE_CACHE_FILL_PERCENT=92
CLAIMS_KNOWLEDGE_CACHE_QUOTA_BYTES=134217728
```

The knowledge service emits `CLAIMS_KNOWLEDGE_CACHE_UTILIZATION_METRIC` from the same cache quota that controls the slow path and `CLAIMS_KNOWLEDGE_CLAIM_STATUS_LATENCY_METRIC` from the observed AI Claim Status request latency. Splunk detectors, dashboards, and MCP evidence use the `SPLUNK_*` metric names, so the remediation flow is not tied to unrelated host-level disk widgets.

## 7. Optional values

- `VITE_SPLUNK_RUM_TOKEN`
- `VITE_SPLUNK_SESSION_REPLAY_ENABLED=true`
- `ORCHESTRATOR_PUBLIC_WEBHOOK_URL`
- `SPLUNK_WEBHOOK_SHARED_SECRET`

## 8. Load `.env`

```bash
set -a
source .env
set +a
```

Do this before starting collector, backend, or frontend processes.

## 9. Optional public webhook

The primary lab flow uses copied Splunk evidence and does not require a public webhook. Start a tunnel only if you explicitly want Splunk detector delivery into the local orchestrator:

```bash
npm run dev:tunnel
```
