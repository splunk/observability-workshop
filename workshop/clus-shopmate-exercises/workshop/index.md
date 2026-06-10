---
template: home.html
title: Home
---

# CLUS-LTROBS-2001 Lab Guide

## From Deployment To Deep Insights

Welcome to the student lab guide for `CLUS-LTROBS-2001`.

In this lab you will work as an AI platform operator. Your job is to observe the ShopMate Sports retail website, connect its telemetry to Splunk Observability Cloud, inspect its assistant trace flow, scrape GPU and NVIDIA NIM metrics, and finish with an environment-level tokenomics investigation.

!!! note "App Naming"
    Students use the **ShopMate Sports** website in the browser. In Kubernetes and Splunk, the workload may appear as `shopmate-ai` so the lab has a stable service name for traces, metrics, and dashboards.

This site is the path you follow during the workshop. It does not teach you how to build the shared cluster. The Kubernetes, GPU, NIM, and Splunk environment is already prepared for you.

## AI PODs In One Minute

A Cisco AI POD is a validated infrastructure pattern for running AI workloads. It brings together GPU compute, high-speed networking, storage, platform software, and operations tooling so teams can run model training, fine-tuning, RAG, and inference workloads with a repeatable design.

For this lab, keep the idea simple:

```text
AI app -> model service -> GPUs -> platform health -> Splunk evidence
```

The GPUs are the center of the story. The app creates demand, NVIDIA NIM serves the model, the GPUs do the acceleration work, and Splunk helps you prove what happened.

## How This Lab Works

You will not rack servers, cable switches, or build the AI POD hardware. The instructor has already prepared a shared GPU-backed environment.

Your job is to follow the operational path:

1. Start your namespace-scoped collector as a baseline OTLP gateway.
2. Configure the ShopMate Sports agent app to send traces and metrics to that collector.
3. Send a request through the ShopMate Sports AI assistant and find the trace in Splunk.
4. Change the collector file to add GPU and NIM Prometheus scraping.
5. Compare the before/after result in Splunk, then correlate those signals with Kubernetes health and the standard `deployment.environment` filter.

## What You Will Do

By the end of the lab, you will be able to:

- Filter lab telemetry by `deployment.environment`, namespace, and service name.
- Deploy or validate a namespace-scoped OpenTelemetry Collector.
- Send ShopMate Sports traces and metrics through your collector.
- Make a collector config change, redeploy it, and verify the new telemetry path.
- Inspect an AI assistant trace with ShopMate API, OpenAI-compatible assistant, NIM, and token signals.
- Capture safe synthetic prompt and response content.
- Scrape shared GPU and NIM Prometheus metrics.
- Correlate app behavior, model-serving latency, GPU utilization, and Kubernetes health.
- Identify whether token spend came from normal use, a token surge, a bounded agent loop, or retries.

## The Story

ShopMate Sports is a fictional athletic retail website with a shopping assistant. A shopper browses products, compares shoes and gear, checks inventory, asks return-policy questions, and gets cart recommendations. The assistant calls NVIDIA NIM for the final customer-facing response.

The business question at the end is:

```text
Which lab environment and request pattern spent the most tokens, and why?
```

You will answer that question using Splunk traces, metrics, dashboards, and resource attributes.

## Lab Architecture

```mermaid
flowchart LR
  User["You"] --> App["ShopMate Sports\nretail website"]
  App --> Agents["Shopping, catalog,\ninventory, policy,\ncheckout, cost agents"]
  Agents --> NIM["NVIDIA NIM\nLLM endpoint"]
  NIM --> GPU["Shared GPU nodes"]

  App --> Collector["Your student\nOpenTelemetry Collector"]
  Collector --> Splunk["Splunk Observability Cloud"]

  DCGM["DCGM exporter"] --> Collector
  NIM --> Collector
  K8s["Kubernetes metrics\nshared platform view"] --> Splunk
```

## Lab Flow

| Time | Module | What You Produce |
| --- | --- | --- |
| 0:00-0:20 | Orientation | You understand the app, telemetry path, and final challenge |
| Reference | Data Journey | You understand how collector config, app telemetry, NIM metrics, and GPU metrics connect |
| 0:20-0:55 | Student Collector | Your collector is running and exporting telemetry |
| 0:55-1:45 | App Instrumentation | You can find a full ShopMate Sports agent trace |
| 1:45-2:25 | GPU and NIM Scraping | Your collector scrapes shared GPU and NIM metrics |
| 2:25-2:50 | Correlation | You connect traces, NIM metrics, GPU metrics, and Kubernetes health |
| 2:50-3:40 | Tokenomics | You investigate token surge and agent-loop token burn |
| 3:40-4:00 | Final Review | You submit your evidence and recommendations |

## Your Lab Identity

Your lab handout gives you a student identity. You will use it throughout the lab.

Example:

```text
k8s.namespace.name=<STUDENT-NAMESPACE>
deployment.environment=<STUDENT-ID>
k8s.cluster.name=clus-ltrobs-2001-<STUDENT-ID>
```

!!! success "Checkpoint"
    Before starting Module 1, you should know your namespace, Splunk login, and assigned `deployment.environment` value.

## How To Use This Guide

Work through the modules in order. Each module has:

- a short explanation
- commands or UI actions
- expected results
- a checkpoint
- a knowledge check

Use the troubleshooting appendix when a checkpoint does not match your environment.
