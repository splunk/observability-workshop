---
title: Troubleshooting
linkTitle: 7. Troubleshooting
weight: 7
archetype: chapter
time: 10 minutes
description: Recover from common local setup, telemetry, and remediation issues during the workshop.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are a **workshop facilitator** recovering the lab without changing the learning objective. Your goal is to keep the audience focused on customer impact, evidence, policy, approval, and validation.
{{% /notice %}}

## `npm install` Fails

Check:

- Internet access or package registry access.
- Node version compatibility.
- Whether a previous partial install left a corrupted `node_modules`.

Action:

```bash
npm install
```

Capture the first real error and fix that root issue before changing application code.

## Python Agent Setup Fails

Recreate the virtual environment only when you intend to replace it:

```bash
cd apps/remediation-agent
rm -rf .venv
python3 -m venv .venv
.venv/bin/pip install --index-url https://pypi.org/simple -e .
```

## Collector Will Not Start

Check:

- Docker daemon is running.
- `.env` is loaded.
- Host port `14318` is free.

Action:

```bash
docker info
grep -E '^OTEL_EXPORTER_OTLP_ENDPOINT=' .env
npm run dev:collector
```

Expected local endpoint:

```dotenv
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:14318
```

## Portal or Console Does Not Load

Check:

- `npm run dev` is still running.
- Vite did not fail because of a port conflict.
- Browser is pointed at the high-port URLs.

Action:

```bash
lsof -i :18080 -i :18081
```

## The Support Transaction Does Not Degrade

Check:

- `Trigger Cache Pressure` was clicked.
- `AI Claim Status` was rerun after the scenario became active.
- `CLAIMS_KNOWLEDGE_CACHE_DIR` points at a writable lab directory.

Useful checks:

```bash
curl -s http://127.0.0.1:18104/scenario/state
curl -s http://127.0.0.1:18103/knowledge/cache/status
```

## Telemetry Is Not Visible in Splunk

Check locally first:

1. Collector is running.
2. App processes started with `.env` loaded.
3. Fresh traffic was generated after collector startup.
4. `INSTANCE` and `OTEL_RESOURCE_ATTRIBUTES` match the student lab.

Look for:

- APM services such as `claims-knowledge`, `claims-assistant`, and `remediation-agent`.
- Filesystem utilization for `/var/cache/claims-knowledge`.
- RUM data for the portal if `VITE_SPLUNK_RUM_TOKEN` is set.

If RUM sessions are missing:

1. Confirm `VITE_SPLUNK_RUM_TOKEN` is configured.
2. Restart the portal.
3. Generate fresh browser traffic.
4. Wait a few minutes.
5. Use `Pages` or `Network Requests` before relying on Session Search.

## Remediation Recommendation Is Missing

Check:

- `Gather MCP Evidence` created an evidence package.
- The orchestrator built an evidence bundle.
- Policy mode is visible.
- The remediation agent is reachable on `18800`.

Action:

```bash
curl -s http://127.0.0.1:18800/agent/health
curl -s http://127.0.0.1:18110/remediation/health
```

## Safe Fallback

If the live path is unstable:

1. Show the portal baseline.
2. Explain and trigger cache pressure.
3. Use the fallback evidence text in the operator console.
4. Explain policy and approval.
5. Approve the bounded action if the local services are healthy.
6. Close on validation and auditability.
