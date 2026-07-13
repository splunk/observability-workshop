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
- Deploy a polyglot (that means many languages) microservices stack with Docker Compose and add distributed tracing with one container
- Deploy the same stack to Kubernetes using the Splunk OTel Collector Helm chart and enable OBI with one flag
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
| Helm 3 | Pre-installed |
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

These services have **zero observability code**  no OpenTelemetry SDKs, no tracing headers, no instrumentation of any kind. OBI instruments them from the kernel using eBPF probes, generates OpenTelemetry-compatible traces, and sends them to a Splunk OTel Collector which forwards to Splunk Observability Cloud.

## What is OBI?

[OBI (OpenTelemetry eBPF Instrumentation)](https://opentelemetry.io/docs/zero-code/obi/) is a standalone agent that uses Linux kernel eBPF probes to observe HTTP/gRPC traffic flowing through applications. It attaches to processes **from the kernel** no SDK, no code changes, no recompilation. It sees the requests, generates OpenTelemetry-compatible trace spans, and sends them to a collector.

This is valuable for organizations that **cannot** or **will not** instrument with SDKs:

- Legacy systems with no source access
- Compiled languages where recompilation isn't an option
- Developer resistance ("we don't have time to add instrumentation")
- Regulatory constraints where any code change triggers a full audit cycle

## The Value Proposition

Many organizations have applications they **cannot** or **will not** instrument with OpenTelemetry SDKs:

- **Legacy systems**: COBOL-to-Java migrations, decade-old .NET Framework apps, vendor-provided binaries with no source access
- **Compiled languages**: Go, Rust, C++ services where recompilation isn't an option or the team has moved on
- **Developer resistance**: "We don't have time", "It's not in the sprint", "We're not changing working code"
- **Regulatory constraints**: Any code change triggers a full audit/certification cycle

OBI gives you **full distributed tracing without any code changes**:

- **Zero SDK integration**: no imports, no dependencies, no compile-time changes
- **Zero application restarts**: OBI attaches to already-running processes via eBPF
- **Language agnostic**: works with Go, Node.js, Python, Java, Rust, C++ or anything that speaks HTTP or gRPC
- **One container or one Helm flag**: add it to your compose or enable `obi.enabled=true` in your Helm chart and you're done

## OBI vs Traditional Zero-Code Instrumentation

OBI and existing traditional language-specific zero-code instrumentation (Java, JS, .NET, Python, Go, PHP) serve complementary roles in an observability strategy. Understanding the differences helps determine when to use each approach.

### 1. Instrumentation Model

| Aspect | OBI | Traditional Zero-Code Instrumentations |
|---|---|---|
| Execution model | Out-of-process | In-process |
| Instrumentation layer | Linux kernel / network | Application runtime |
| Requires code changes | No | No or minimal |
| Requires application restart | No | Yes |
| Security profile | Isolated | Same permission profile as the application |

### 2. Level of Visibility

| Capability | OBI | Traditional Zero-Code Instrumentations |
|---|---|---|
| Distributed tracing | Protocol-level | Full-fidelity |
| RED metrics | Yes | Yes |
| Application logs collection | No | Yes |
| Application log-trace correlation | Yes | Yes |
| Application internals (frameworks, functions) | No (partial, mostly in Go) | Yes |
| Custom spans / business attributes | No | Yes |
| Runtime metrics (JVM, memory, threads) | No, for now | Yes |

### 3. Coverage & Compatibility

| Scenario | OBI | Traditional Zero-Code Instrumentations |
|---|---|---|
| Multi-language environments | Strong (protocol-based) | Language-specific |
| Third-party applications | Supported | Limited, contrib repos |
| Legacy systems | Supported | Limited |
| Compiled languages (C/C++/Rust) | Supported (with some limitations in async) | Limited |
| Async / complex frameworks | Limited in some cases | Strong |

### 4. Operational Characteristics

| Aspect | OBI | Traditional Zero-Code Instrumentations |
|---|---|---|
| Deployment effort | Low (drop-in) | Medium (agent attachment) |
| Time to first visibility | Minutes | "More" minutes |
| Changes to application lifecycle | No | Yes |
| Performance overhead | Minimal and isolated | Varies by language/runtime |

### 5. Splunk Distro Features

| Feature | OBI | Traditional Zero-Code Instrumentations |
|---|---|---|
| Always-on Profiling | No (may be bundled with eBPF profiler in future) | CPU for most, Memory for some |
| Call graphs | No | CPU for most, Memory for some |
| File-based configuration | Incoming | Java, Node.js, .NET, Python (incoming) |
| No-code instrumentation | N/A | Yes |
