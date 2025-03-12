---
title: Advanced Collector Configuration
description: Practice setting up the OpenTelemetry Collector configuration from scratch and go though several advanced configuration scenarios's.
weight: 2
archetype: chapter
authors: ["Robert Castley,", "Charity Anderson,", "Pieter Hagen", "&", "Geoff Higginbottom"]
time: 90 minutes
---

The goal of this workshop is to help you become comfortable creating and modifying OpenTelemetry Collector configuration files. You’ll start with a minimal `agent.yaml` file and gradually configure several common advanced scenarios.

The workshop also explores how to configure the OpenTelemetry Collector to store telemetry data locally instead of transmitting it to a third-party vendor backend. Furthermore, this approach significantly enhances the debugging and troubleshooting process and is useful for testing and development environments where you don’t want to send data to a production system.

To get the most out of this workshop, you should have a basic understanding of the OpenTelemetry Collector and its configuration file format. Additionally, proficiency in editing YAML files is required. The entire workshop is designed to run locally.

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
