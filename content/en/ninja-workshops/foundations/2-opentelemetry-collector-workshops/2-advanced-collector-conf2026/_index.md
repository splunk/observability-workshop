---
title: Advanced OpenTelemetry Collector - .conf26
description: Practice reviewing and modifying a host-installed OpenTelemetry Collector configuration.
weight: 3
type: chapter
authors: ["Kyle Wang", "Antoine Toulme"]
original_authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
ai_assistance: "Codex"
time: 55 minutes
---

{{% notice title="Workshop credits" style="info" %}}
**.conf26 edition:** Kyle Wang and Antoine Toulme, developed with Codex.

**Original workshop:** Robert Castley, Charity Anderson, Pieter Hagen, and
Geoff Higginbottom.
{{% /notice %}}

In this workshop, you will run one portable Splunk OpenTelemetry Collector in
**agent mode** on a Linux host or Apple Silicon Mac. The Collector
receives synthetic traces, reads synthetic logs, and collects host metrics.
The starter configuration combines Splunk Distribution default pipelines with
local console and file exporters used by the workshop.

When valid Observability Cloud credentials are supplied, default metrics and
traces pipelines send data to Splunk. Local exporters remain active so every
exercise can also be completed without a cloud connection.

## Workshop Overview

During this workshop, you will:

- Run the portable Splunk OpenTelemetry Collector `0.157.0` as one Agent.
- Generate traces and logs and collect host metrics on Linux or Apple Silicon.
- Validate all three signals locally and, when available, validate metrics and
  traces in Splunk Observability Cloud.
- Download the starter `agent_config.yaml` and inspect it in OTel Collector
  Config Builder.
- Progressively explore span filtering, sensitive-data handling, and log
  transformation in Config Builder.
- Download the completed configuration once, deploy it to the Agent, and
  validate every change locally and in Splunk Observability Cloud when the
  applicable backend connection is available.

Chapter 6 provides additional learning paths for resilience, deployment at
scale, zero-code instrumentation, migration, logs, and profiling.
