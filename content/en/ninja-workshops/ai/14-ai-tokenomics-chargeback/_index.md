---
title: AI Tokenomics and GPU Chargeback
linkTitle: AI Tokenomics and Chargeback
weight: 14
layout: chapter
time: 90 minutes
authors: ["Splunk Observability Workshop Contributors"]
description: Build token, cost, and GPU allocation views for AI workloads using local model benchmarks, public GPU price proxies, and targeted OpenTelemetry instrumentation.
draft: false
hidden: false
aliases:
  - /ninja-workshops/14-ai-tokenomics-chargeback/
product: "Observability Cloud"
---

AI platforms need cost visibility at two levels: the application layer that consumes
tokens, and the infrastructure layer that runs shared GPU capacity. **Splunk
Observability Cloud** gives teams out-of-the-box visibility into AI infrastructure,
LLM application traces, Kubernetes, and GPU telemetry. Chargeback requires one
additional layer of intent: stable business attribution and cost metrics that connect
that telemetry to teams, tenants, workloads, and models.

This workshop shows how to combine both approaches. The primary lab path runs on a
local model, so students do not need a Kubernetes cluster. If you have a Cisco AI Pods
or GPU cluster environment, the same model extends to out-of-the-box GPU telemetry.

* Benchmark a local model with Ollama or an OpenAI-compatible local endpoint.
* Derive internal token rates from observed throughput and hourly accelerator cost.
* Use public GPU hourly data as a market proxy when no internal rate card exists.
* Optionally use out-of-the-box AI infrastructure and AI application monitoring data.
* Add custom OpenTelemetry attributes and metrics for chargeback attribution.
* Estimate token cost per request, tenant, team, workload, and model.
* Allocate shared GPU or local accelerator cost from utilization, allocation, or
  measured throughput.
* Build dashboard views and detectors that FinOps, platform, and application teams can
  use without exporting data to a separate spreadsheet.

## Workshop Flow

```mermaid
flowchart LR
    Local["Local model benchmark"] --> Throughput["Observed token throughput"]
    Public["Public GPU hourly proxy"] --> RateCard["Derived internal rate card"]
    Throughput --> RateCard
    RateCard --> Instr["Custom OTel attributes and metrics"]
    OOTB["Optional GPU cluster monitoring"] --> GPUCost["GPU allocation signals"]
    Instr --> Dashboard["Tokenomics dashboard"]
    GPUCost --> Dashboard
    Dashboard --> Detectors["Budget and efficiency detectors"]
```

## What You Need

* Access to a Splunk Observability Cloud organization.
* A laptop or workstation that can run a local model with Ollama. CPU-only works for
  the lab; a local GPU makes the economics more realistic.
* Optional: a monitored Kubernetes or OpenShift environment with GPU workloads.
* Optional: the Cisco AI Pods collector and NIM examples from the **Monitoring Cisco AI
  Pods** workshop, or equivalent NVIDIA DCGM and NIM Prometheus metrics.
* Permission to view dashboards, Infrastructure Monitoring, APM, traces, detectors, and
  Metric Finder.
* A sample public GPU hourly proxy or internal hardware amortization value.

{{% notice title="Workshop Positioning" style="info" %}}
This workshop can run as a standalone local-model lab. The **Monitoring Cisco AI Pods**
and **Monitoring Agentic AI Applications** workshops provide optional production-style
telemetry, but they are not required to learn the economics model.
{{% /notice %}}

## What You Will Build

By the end of the workshop, you will have a working pattern for:

* AI request attribution with `ai.team`, `ai.cost_center`, `ai.tenant.id`,
  `ai.workload.name`, and `gen_ai.request.model`.
* A derived token rate card from local benchmark data.
* Token counters for prompt, completion, and total tokens.
* Request-level estimated cost metrics.
* GPU pool allocation formulas based on shared workload usage.
* A dashboard layout for executive summary, team breakdown, model economics, and GPU
  efficiency.
* Detectors for cost spikes, budget burn, inefficient GPU use, and runaway token growth.
