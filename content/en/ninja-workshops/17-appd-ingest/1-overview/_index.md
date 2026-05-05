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

Rather than re-instrumenting every service with a separate OpenTelemetry SDK, the **AppDynamics Java Agent** supports **dual signal mode**: a single agent produces both AppDynamics APM data and OpenTelemetry traces simultaneously. This lets you maintain full AppDynamics functionality while streaming the same telemetry to Splunk Observability Cloud through an OpenTelemetry Collector.

This is especially helpful for your current L1 and L2 teams who currently know and rely on AppDynamics. Dual ingest helps maintain context as the applications and services they are responsible become more connected to new services hosted in SaaS platforms in the cloud.

## What You'll Learn

By the end of this workshop, you will:

- Build and run a simple Java service with the AppDynamics Java Agent
- Add infrastructure dual signal with the **AppDynamics Combined Machine Agent**, the lowest-effort step to get hosts into both AppDynamics and Splunk Observability Cloud
- Understand the difference between **hybrid mode** and **dual signal mode** on the Java agent
- Customize the bundled OTel collector inside the AppDynamics machine agent with the workshop config and feel the friction of doing it that way
- Replace the bundled collector with the **standalone Splunk OpenTelemetry Collector** (the configuration we recommend for production observability) and watch that friction disappear
- Verify traces and metrics in both platforms
- Create a **global data link** in Splunk Observability Cloud for one-click navigation to AppDynamics

## Architecture

In this workshop you will run a Spring Boot Java application directly on your EC2 instance. The AppDynamics Java Agent attaches to the JVM process. Each phase changes one part of the picture.

**Phase 1: Normal AppD instrumentation:**

```text
Java App + AppD Agent  ──▶  AppD Controller
```

**Phase 2: Combined Machine Agent with the bundled config (infrastructure dual signal):**

```text
Java App + AppD Agent  ──▶  AppD Controller        (APM, unchanged)

Machine Agent (combined)        ──▶  AppD Controller       (Server Visibility)
  └─▶ Bundled OTel Collector    ──▶  Splunk Observability Cloud  (hostmetrics)
        (config: agent_config.yaml, AppD default, metrics-only)
```

The AppDynamics Combined Machine Agent ships with a bundled OTel collector built in (this is **not** a fully-configured Splunk OTel Collector, just the Splunk Distribution binary AppD packages and updates on its own cadence). The default config is metrics-only. APM still flows only to AppDynamics.

**Phase 3: Bundled collector running the workshop config (APM dual signal, the hard way):**

```text
Java App + AppD Agent (dual)  ──▶  AppD Controller        (APM, unchanged)
                              ──▶  localhost:4318 (OTLP)
                                          │
Machine Agent (combined)                  │
  └─▶ Bundled OTel Collector  ◀───────────┘
        (config: workshop collector-config.yaml in place of agent_config.yaml)
        (env vars: SPLUNK_INGEST_URL, SPLUNK_API_URL, SPLUNK_HEC_*, SPLUNK_BUNDLE_DIR, ... exported by hand)
        ──▶  Splunk Observability Cloud  (APM + Hosts + Logs, mostly)
```

Same Splunk Distribution binary as Phase 4, just running inside the AppDynamics install. You manually export every `SPLUNK_*` env var the workshop config needs, and the Smart Agent monitor bundle is missing because AppD does not ship it. The path works for APM and host metrics, the friction is the lesson.

**Phase 4: Standalone Splunk OTel Collector (recommended end-state):**

```text
Java App + AppD Agent (dual)  ──▶  AppD Controller        (APM, unchanged)
                              ──▶  localhost:4318 (OTLP)
                                          │
Machine Agent (AppD-only)                 │
  └─▶  AppD Controller (Server Visibility) │
                                          ▼
              Splunk OTel Collector (systemd-managed)
                (config: /etc/otel/collector/agent_config.yaml = workshop config)
                (env vars: /etc/otel/collector/splunk-otel-collector.conf, written by install script)
                (Smart Agent bundle: /usr/lib/splunk-otel-collector/agent-bundle, shipped by package)
                ──▶  Splunk Observability Cloud  (APM + Hosts + Logs + Profiling + Process List)
```

Same workshop config as Phase 3, run by a `systemd`-managed standalone install. Every `SPLUNK_*` env var lives in `/etc/otel/collector/splunk-otel-collector.conf`, the Smart Agent monitor bundle is on disk so `smartagent/processlist` actually works, and the collector lifecycle is independent of the AppD machine agent. This is the configuration we recommend for production observability and the natural step toward an OTel-native footprint.

**Note:** It is possible to send data directly from the Java agent to our [OTLP ingest endpoint](https://dev.splunk.com/observability/docs/datamodel/ingest/#Send-data-points) without a collector, but you lose the resource processors, high-cardinality trim, and other pipeline configuration the workshop config provides.

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
