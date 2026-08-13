---
title: Advanced OpenTelemetry Collector - .conf26
description: Practice reviewing and modifying a host-installed OpenTelemetry Collector configuration.
weight: 3
type: chapter
authors: ["Kyle Wang", "Antoine Toulme"]
original_authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
ai_assistance: "Codex"
time: 55 minutes
hidden: true
---

{{% notice title="Workshop credits" style="info" %}}
**.conf26 edition:** Kyle Wang and Antoine Toulme.

**Original workshop:** Robert Castley, Charity Anderson, Pieter Hagen, and
Geoff Higginbottom.
{{% /notice %}}

In this workshop, you run one Splunk Distribution of the OpenTelemetry
Collector in **agent mode** on a Linux host or Apple silicon Mac. The Collector
receives sample traces, reads sample logs, and collects host metrics. You then
use OTel Collector Config Builder to improve the data before it leaves the
Collector.

## Workshop overview

During this workshop, you will:

- Run version `0.157.0` of the Collector as one agent.
- Generate traces and logs, and collect host metrics.
- Check all three signals locally and, when available, in Splunk Observability
  Cloud.
- Upload `agent_config.yaml` and inspect it in OTel Collector Config Builder.
- Filter noisy spans, protect sensitive attributes, and transform logs.
- Download the completed configuration, apply it to the agent, and verify the
  results.

Chapter 6 includes more ways to continue learning after the workshop.
