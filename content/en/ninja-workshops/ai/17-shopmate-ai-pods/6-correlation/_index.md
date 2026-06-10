---
title: Correlation
linkTitle: 6. Correlation
weight: 6
archetype: chapter
time: 25 minutes
description: Follow one ShopMate request through app, model, GPU, and Kubernetes evidence.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are an **incident investigator**. Your goal is to explain one user-visible AI request with trace, model-serving, GPU, and Kubernetes evidence.
{{% /notice %}}

## Generate A Correlation Request

Open the ShopMate Sports website and send:

```text
Find me wide running shoes with good stability, and explain the pickup or delivery options.
```

Expected response:

- Products from the demo catalog, such as `RoadFlow 880` or `TrailRidge GTX`.
- Inventory examples from demo locations.
- Pickup or delivery notes from demo store data.
- No invented products, locations, delivery dates, or order actions.

## Start From The Trace

In Splunk Observability Cloud:

1. Open **APM** and then **Traces** or **Trace Analyzer**.
2. Use a recent time range, such as the last 15 minutes.
3. Filter:

```text
service.name = shopmate-ai
deployment.environment = <your student id>
operation = POST /api/chat
```

Open the newest matching trace.

Record:

| Field | Value |
| --- | --- |
| Trace start time | |
| Trace duration | |
| Slowest span | |
| NIM or LLM span duration | |
| Token fields visible | |

## Read The Waterfall

Look for spans or attributes similar to:

- `POST /api/chat`
- `shopmate.workflow`
- `ShoppingAssistantAgent`
- `CatalogAgent`
- `InventoryAgent`
- `PolicyAgent`
- `lookup_inventory`
- `lookup_store_policy`
- NIM or OpenAI-compatible LLM spans

Use the trace timestamp to inspect related metric views.

## Compare Lower-Layer Signals

Use the same time window as the trace:

| Layer | Filter | What it tells you |
| --- | --- | --- |
| App | `service.name=shopmate-ai`, `deployment.environment=<STUDENT_ID>` | Which route, agent, tool, or LLM span consumed request time. |
| NIM | `job=nim`, `deployment.environment=<STUDENT_ID>` | Model-serving request rate, latency, or error pattern. |
| GPU | `job=dcgm`, `deployment.environment=<STUDENT_ID>` | Whether GPU utilization or memory pressure rose during the request. |
| Kubernetes | Namespace and workload filters | Whether pod health, restarts, or scheduling explain the app symptom. |

## Evidence Statement

Write one sentence:

```text
At <time>, ShopMate request <trace id> took <duration>. The slowest span was <span>. NIM metrics showed <observation>. GPU metrics showed <observation>. Kubernetes health showed <observation>. Therefore, the strongest explanation is <hypothesis>.
```

{{% notice title="Correlation Rule" style="info" %}}
Start with one trace and then move outward. Do not start by browsing every dashboard without a timestamp and environment filter.
{{% /notice %}}
