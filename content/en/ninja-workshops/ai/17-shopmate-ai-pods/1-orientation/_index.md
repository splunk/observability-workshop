---
title: Orientation
linkTitle: 1. Orientation
weight: 1
archetype: chapter
time: 20 minutes
description: Understand the AI POD-inspired lab environment, ShopMate Sports app, and operator investigation path.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are an **AI platform operator**. Your job is to explain whether a slow or expensive AI request came from the app workflow, model-serving layer, GPU pressure, or Kubernetes health.
{{% /notice %}}

## What Is ShopMate Sports?

ShopMate Sports is a fictional athletic retail website with an AI shopping assistant. A shopper can browse products, compare shoes and gear, check inventory, ask return-policy questions, and request cart recommendations.

In Kubernetes and Splunk, the workload may appear as:

```text
shopmate-ai
```

Use that service name for trace, metric, and dashboard filters unless your instructor provides a different name.

## What Is Already Running?

The shared lab environment includes:

- Kubernetes with GPU worker nodes.
- NVIDIA GPU Operator.
- DCGM exporter for GPU metrics.
- NVIDIA NIM for model inference.
- ShopMate Sports retail AI workload.
- Splunk Observability Cloud.
- Shared Kubernetes and platform telemetry.

You will not rack hardware, deploy GPU operators, build images, or manage the shared model-serving platform during the student lab.

## What You Control

Inside your namespace, you control:

- Your student OpenTelemetry Collector gateway.
- ShopMate Sports telemetry configuration.
- Your `deployment.environment` filter.
- Splunk searches, dashboards, traces, and metric views.
- Scenario traffic for tokenomics and agent-loop analysis.

## Investigation Questions

As you work through the lab, keep asking:

- Did the request reach ShopMate Sports?
- Did the app emit workflow, agent, tool, and LLM spans?
- Did telemetry include `deployment.environment`?
- Did NIM latency or GPU utilization change during token-heavy work?
- Did repeated agent or NIM spans burn tokens before guardrails stopped the path?
- Can you explain final token usage with evidence?

## Source Copy

The local copy of the source lab is:

```bash
cd workshop/clus-shopmate-exercises
```

Useful source paths:

| Path | Purpose |
| --- | --- |
| `workshop/` | Original attendee-facing MkDocs lab guide. |
| `workshop/lab-files/` | Student manifests and collector snippets. |
| `shopmate-sports/` | Standalone retail AI app source. |
| `infra/` | Instructor infrastructure, Kubernetes, Helm, and Terraform assets. |
| `docs/` | Planning, setup, and validation notes. |
