---
title: Investigate Cache Pressure
linkTitle: 4. Investigate Cache Pressure
weight: 4
archetype: chapter
time: 25 minutes
description: Trigger the cache-pressure incident, reproduce the degraded transaction, and validate the evidence in Splunk Observability Cloud.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are an **observability lead** proving the incident with telemetry. Your job is to separate customer impact, service behavior, and infrastructure cause before anyone approves a remediation action.
{{% /notice %}}

## Trigger the Incident

Use the portal or operator console button named `Trigger Cache Pressure`.

You can also trigger the scenario from a terminal:

```bash
curl -X POST http://127.0.0.1:18104/scenario/activate/cache-disk-pressure
curl -s http://127.0.0.1:18104/scenario/state
```

Expected result:

```text
cache-disk-pressure
```

## Reproduce Customer Impact

In the claims portal:

1. Run `AI Claim Status`.
2. Run `Policy Coverage Lookup`.
3. Run `Claims FAQ Search`.

Expected result:

- `AI Claim Status` is slower or partially degraded.
- `Policy Coverage Lookup` and `Claims FAQ Search` remain healthier comparison journeys.
- The whole application is not down.

Optional local checks:

```bash
curl -s http://127.0.0.1:18104/scenario/state
curl -s http://127.0.0.1:18103/knowledge/cache/status
```

## Drive Degraded Traffic

Use this if you need more telemetry points:

```bash
SIMULATOR_SCENARIO=current SIMULATOR_DURATION_SECONDS=300 SIMULATOR_INTERVAL_MS=750 SIMULATOR_MIX=claim-heavy npm run simulate:traffic
```

Keep comparison traffic visible:

```bash
SIMULATOR_SCENARIO=current SIMULATOR_DURATION_SECONDS=180 SIMULATOR_INTERVAL_MS=1000 SIMULATOR_MIX=balanced npm run simulate:traffic
```

## Validate in Splunk

Filter by the student identity:

```text
service.instance.id=<INSTANCE>
deployment.environment=demo
lab.name=ciscolive26
lab.student.id=<INSTANCE>
```

Use these checks:

| Area | What to open | Expected evidence |
| --- | --- | --- |
| Digital Experience | RUM app `ibobs-claims-portal` | Portal activity and slower `/api/support/respond` requests when RUM is configured. |
| APM | `claims-knowledge` service | `service.request.duration.ns` increases for the claim status path. |
| APM traces | Slow `AI Claim Status` trace | Waterfall includes `claims-portal-api`, `claims-assistant`, and `claims-knowledge`. |
| Infrastructure | Host or container filesystem metrics filtered by `INSTANCE` | Filesystem utilization rises for `/var/cache/claims-knowledge`. |
| Business comparison | Policy Coverage and FAQ paths | Comparison journeys remain healthier than `AI Claim Status`. |

## Evidence Statement

Write a short evidence statement before moving to remediation:

```text
AI Claim Status is degraded for <INSTANCE>. APM shows elevated claims-knowledge duration, and infrastructure metrics show cache filesystem pressure for /var/cache/claims-knowledge. Policy Coverage Lookup and Claims FAQ Search remain healthier comparison journeys. The narrow recommended action is clean_claims_knowledge_cache.
```

{{% notice title="Stop and Check" style="warning" %}}
Do not approve remediation until you can connect the degraded customer journey to `claims-knowledge` service latency and cache filesystem pressure. If one signal is missing, document the gap and lower confidence.
{{% /notice %}}
