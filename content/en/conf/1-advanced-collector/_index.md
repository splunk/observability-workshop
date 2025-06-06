---
title: Advanced Collector Configuration
description: Practice setting up the OpenTelemetry Collector configuration from scratch and go though several advanced configuration scenarios's.
weight: 2
archetype: chapter
authors: ["Robert Castley,", "Charity Anderson,", "Pieter Hagen", "&", "Geoff Higginbottom"]
time: 90 minutes
---

The goal of this workshop is to help you gain confidence in creating and modifying OpenTelemetry Collector configuration files. You’ll start with a minimal `agent.yaml` file and progressively build it out to handle several advanced, real-world scenarios.

A key focus of this workshop is learning how to configure the OpenTelemetry Collector to store telemetry data locally, rather than sending it to a third-party vendor backend. This approach not only simplifies debugging and troubleshooting but is also ideal for testing and development environments where you want to avoid sending data to production systems.

To make the most of this workshop, you should have:

- A basic understanding of the OpenTelemetry Collector and its configuration file structure.
- Proficiency in editing YAML files.

Everything in this workshop is designed to run locally, ensuring a hands-on and accessible learning experience. Let’s dive in and start building!

### Workshop Overview

During this workshop, we will cover the following topics:

- **Setting up the agent locally**: Add metadata, and introduce the debug and file exporters.
- **Configuring a gateway**: Route traffic from the agent to the gateway.
- **Configuring the FileLog receiver**: Collect log data from various log files.
- **Enhancing agent resilience**: Basic configurations for fault tolerance.
- **Configuring processors**:
  - Filter out noise by dropping specific spans (e.g., health checks).
  - Remove unnecessary tags, and handle sensitive data.
  - Transform data using OTTL (OpenTelemetry Transformation Language) in the pipeline before exporting.
- **Configuring Connectors**:
  - Route data to different endpoints based on the values received.
  - Convert log and span data to metrics.

By the end of this workshop, you'll be familiar with configuring the OpenTelemetry Collector for a variety of real-world use cases.
