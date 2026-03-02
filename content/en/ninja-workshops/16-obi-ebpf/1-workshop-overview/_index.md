---
title: Workshop Overview
linkTitle: 1. Workshop Overview
weight: 1
archetype: chapter
time: 5 minutes
description: Goals, prerequisites, and architecture for the OBI workshop.
---

## What You'll Learn

By the end of this workshop, you will:

- Understand how eBPF enables zero-code instrumentation at the Linux kernel level
- Instrument a running application with the OBI binary on a bare host
- Deploy a polyglot microservices stack with Docker Compose and add distributed tracing with one container
- Deploy the same stack to Kubernetes and add tracing with one DaemonSet
- Navigate Splunk APM to view distributed traces, service maps, and request flows

## Prerequisites

Your workshop instance comes pre-configured with everything you need:

| Requirement | Status on Workshop Instance |
|---|---|
| Linux host | Provided (Ubuntu) |
| Python 3.9+ | Pre-installed |
| Docker & Docker Compose | Pre-installed |
| K3s (Kubernetes) | Pre-installed |
| kubectl | Pre-installed |
| Workshop assets | Pre-deployed at `~/workshop/obi/` |

You will also need:

| Requirement | How to Get It |
|---|---|
| Splunk Observability Cloud account | Provided by your instructor |
| **Splunk Access Token** (Ingest) | type `env` in your instance look for `ACCESS_TOKEN` |
| **Splunk Realm** (e.g. `us0`, `us1`, `eu0`) |  type `env` in your instance look for `REALM` |
| A **unique name** (e.g. `shw-2c74`) | `env` and look for `INSTANCE` Used as `host.name` |

## Architecture

The workshop uses three simple microservices that form a request chain:

```text
Frontend (Node.js :3000)  →  Order-Processor (Go :8080)  →  Payment-Service (Go :8081)
```

These services have **zero observability code** -- no OpenTelemetry SDKs, no tracing headers, no instrumentation of any kind. OBI instruments them from the kernel using eBPF probes, generates OpenTelemetry-compatible traces, and sends them to a Splunk OTel Collector which forwards to Splunk Observability Cloud.

## What is OBI?

[OBI (OpenTelemetry eBPF Instrumentation)](https://opentelemetry.io/docs/zero-code/obi/) is a standalone agent that uses Linux kernel eBPF probes to observe HTTP/gRPC traffic flowing through applications. It attaches to processes **from the kernel** -- no SDK, no code changes, no recompilation. It sees the requests, generates OpenTelemetry-compatible trace spans, and sends them to a collector.

This is valuable for organizations that **cannot** or **will not** instrument with SDKs:

- Legacy systems with no source access
- Compiled languages where recompilation isn't an option
- Developer resistance ("we don't have time to add instrumentation")
- Regulatory constraints where any code change triggers a full audit cycle
