---
title: Workshop Overview
linkTitle: 1. Overview
weight: 1
archetype: chapter
time: 5 minutes
description: Use case, architecture, prerequisites, and the differences between hybrid and dual signal mode.
---

## The Use Case

Your organization runs AppDynamics for APM today. As part of a data visibility and governance initiative, leadership wants application performance data flowing into **Splunk Observability Cloud** as well giving teams a unified view alongside infrastructure metrics, logs, and other signals already in Splunk.

Rather than re-instrumenting every service with a separate OpenTelemetry SDK, the AppDynamics Java Agent supports **dual signal mode**: a single agent produces both AppDynamics APM data and OpenTelemetry traces simultaneously. This lets you maintain full AppDynamics functionality while streaming the same telemetry to Splunk Observability Cloud through an OpenTelemetry Collector.

This is especially helpful for your current L1 and L2 teams who currently know and rely on AppDynamics. Dual ingest helps maintain context as the applications and services they are responsible become more connected to new services hosted in SaaS platforms in the cloud.

## What You'll Learn

By the end of this workshop, you will:

- Build and run a simple Java service with the AppDynamics Java Agent
- Understand the difference between **hybrid mode** and **dual signal mode**
- Enable dual signal mode to send APM data to both AppDynamics and Splunk Observability Cloud
- Verify traces and metrics in both platforms
- Create a **global data link** in Splunk Observability Cloud for one-click navigation to AppDynamics

## Architecture

In this workshop you will run a Spring Boot Java application directly on your EC2 instance. The AppDynamics Java Agent attaches to the JVM process.

**Phase 1: Normal AppD instrumentation:**

```text
Java App + AppD Agent  ──▶  AppD Controller
```

**Phase 2: Dual signal mode enabled:**

```text
Java App + AppD Agent  ──▶  AppD Controller        (AppD protocol, unchanged)
                       ──▶  OTel Collector          (OTLP on localhost:4317)
                                 │
                                 ▼
                           Splunk Observability Cloud
```

The OpenTelemetry Collector runs on the same EC2 instance, receives OTLP from the agent, and exports traces and metrics to Splunk Observability Cloud.  

**Note:** It is possible to send data directly from the agent to our [OTLP ingest endpoint](https://dev.splunk.com/observability/docs/datamodel/ingest/#Send-data-points) without a collector but you may lose some attributes and association taking part in your OTel config.

## Hybrid Mode vs Dual Signal Mode

The AppDynamics Java Agent supports two modes for emitting OpenTelemetry data.  

Understanding the difference matters!

### Hybrid Mode - Old and Dusty (GA, Java Agent 22.3+)

- AppDynamics' **own instrumentation rules** generate OTel-format spans
- The agent reuses its existing instrumentation to produce OTel data (outdated semantic version)
- Framework coverage limited to what AppDynamics instruments
- Enable with: `-Dagent.deployment.mode=hybrid`

### Dual Signal Mode - New Hotness (Beta, Java Agent 25.6+)

- The full [OpenTelemetry Java auto-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/) runs **alongside** the AppD agent
- Two independent instrumentation engines operate in parallel
- **Broader framework coverage** anything the OTel Java agent supports
- Higher CPU and memory consumption
- Enable with: `-Dagent.deployment.mode=dual` or env var `AGENT_DEPLOYMENT_MODE=dual`

### Why Dual Mode for This Workshop

Dual signal mode adds **correlation attributes** to root spans that hybrid mode does not:

| Attribute | Description |
|---|---|
| `appd.app.name` | The AppDynamics application name |
| `appd.tier.name` | The AppDynamics tier name (also appears mid-trace when the tier changes) |
| `appd.bt.name` | The AppDynamics business transaction name |
| `appd.request.guid` | The AppDynamics request GUID |

These attributes enable **global data links** clickable links on Splunk Observability Cloud traces that navigate directly to the corresponding AppDynamics view. Additionally, AppDynamics snapshots captured in dual mode include the OTel `TraceId` in the Data Collectors tab, enabling navigation in both directions.

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

## Prerequisites

Your workshop instance comes pre-configured with the tools you need:

| Requirement | Status on Workshop Instance |
|---|---|
| Linux host (Ubuntu) | Provided |
| OpenJDK 17 | Pre-installed |
| Maven | Pre-installed |
| Workshop assets | Pre-deployed at `~/workshop/appd/` |

You will also need:

| Requirement | How to Get It |
|---|---|
| Splunk Observability Cloud account | Provided by your instructor |
| **Splunk Access Token** (Ingest) | `echo $ACCESS_TOKEN` on your instance |
| **Splunk Realm** (e.g. `us0`, `us1`, `eu0`) | `echo $REALM` on your instance |
| **Instance name** | `echo $INSTANCE` on your instance |
| AppDynamics Controller access | [SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) log in with your Cisco credentials |
