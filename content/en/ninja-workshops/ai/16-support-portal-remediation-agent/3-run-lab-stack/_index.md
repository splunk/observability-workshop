---
title: Run the Lab Stack
linkTitle: 3. Run the Lab Stack
weight: 3
archetype: chapter
time: 20 minutes
description: Start the collector and application stack, verify local endpoints, and create a healthy baseline.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are a **service team engineer** creating the healthy baseline. Your job is to prove the portal, backend, telemetry, and operator console work before the failure is introduced.
{{% /notice %}}

## Start the Collector

Use this when you want Splunk APM, RUM, and host metric export:

```bash
cd workshop/support-portal-remediation-agent
set -a
source .env
set +a
npm run dev:collector
```

The host OTLP HTTP endpoint is:

```text
http://127.0.0.1:14318
```

Leave the collector running in its terminal.

## Start the Application

Open a second terminal:

```bash
cd workshop/support-portal-remediation-agent
set -a
source .env
set +a
npm run dev
```

This starts the backend services, remediation agent, claims portal, and operator console.

## Verify Local Endpoints

Open:

- Claims portal: `http://127.0.0.1:18080`
- Operator console: `http://127.0.0.1:18081`

Run API checks:

```bash
curl -s http://127.0.0.1:18100/api/health
curl -s http://127.0.0.1:18104/scenario/state
curl -s http://127.0.0.1:18110/remediation/health
curl -s http://127.0.0.1:18800/agent/health
```

Expected result:

- Portal loads.
- Operator console loads.
- Scenario state is healthy.
- Remediation orchestrator and remediation agent return healthy responses.

## Establish a Healthy Baseline

In the claims portal, run each journey once:

1. `AI Claim Status`
2. `Policy Coverage Lookup`
3. `Claims FAQ Search`

Confirm:

- All three journeys return successful responses.
- `AI Claim Status` is not noticeably slower than the comparison journeys.
- The operator console has no stale incident blocking the flow.

## Optional Background Traffic

Backend traffic:

```bash
SIMULATOR_DURATION_SECONDS=300 SIMULATOR_INTERVAL_MS=750 SIMULATOR_MIX=balanced npm run simulate:traffic
```

Browser traffic when RUM is configured:

```bash
RUM_SIMULATOR_USERS=3 RUM_SIMULATOR_ROUNDS=4 RUM_SIMULATOR_BROWSERS=chromium npm run simulate:rum
```

Presenter-friendly background traffic:

```bash
SIMULATOR_DURATION_SECONDS=3600 SIMULATOR_INTERVAL_MS=750 SIMULATOR_MIX=balanced npm run simulate:traffic
```

## Baseline Splunk Checks

In Splunk APM, confirm these services appear:

- `claims-portal-api`
- `claims-assistant`
- `claims-knowledge`
- `claims-policy-service`
- `scenario-controller`
- `remediation-orchestrator`
- `remediation-agent`

If RUM is configured, confirm Digital Experience activity for:

```text
ibobs-claims-portal
```
