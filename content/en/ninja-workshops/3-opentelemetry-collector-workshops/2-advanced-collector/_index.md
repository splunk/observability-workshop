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

---

### Prerequisites

- Proficiency in editing YAML files using `vi`, `vim`, `nano`, or your preferred text editor.
- Supported Environments:
  - Splunk Workshop Instance (preferred)
  - Apple Mac (Apple Silicon)

{{% notice title="Exercise" style="green" icon="running" %}}

**Create a workshop directory**: In your workshop instance create a new directory (e.g., `advanced-otel`). We will refer to this directory as `[WORKSHOP]` in the instructions.

**Download workshop binaries**: Change into your `[WORKSHOP]` directory and download the OpenTelemetry Collector and Load Generator binaries:

{{% tabs %}}
{{% tab title="Splunk Workshop Instance" %}}

```bash
wget https://github.com/signalfx/splunk-otel-collector/releases/download/{{< otel-version >}}/otelcol_linux_amd64 -O otelcol && \
wget https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64 -O loadgen && \
```

{{% /tab %}}
{{% tab title="Apple Silicon" %}}

```bash
wget https://github.com/signalfx/splunk-otel-collector/releases/download/{{< otel-version >}}/otelcol_darwin_arm64 -O otelcol && \
wget https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-darwin-arm64 -O loadgen
```

{{% notice style="warning" title="macOS Users" icon="desktop" %}}
Before running the binaries on macOS, you need to remove the quarantine attribute that macOS applies to downloaded files. This step ensures they can execute without restrictions.

Run the following command in your terminal:

```bash { title="Remove Quarantine Attribute"}
xattr -dr com.apple.quarantine otelcol && \
xattr -dr com.apple.quarantine loadgen
```

{{% /notice %}}

{{% /tab %}}
{{% /tabs %}}

<!--
| Platform                         | OpenTelemetry Collector | Load Generator |
|----------------------------------|-------------------------|----------------|
|  Apple Mac (Apple Silicon)   | **[otelcol_darwin_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.117.0/otelcol_darwin_arm64)** | [**loadgen_darwin_arm64**](https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-darwin-arm64) |
|  Apple Mac (Intel)           | **[otelcol_darwin_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.117.0/otelcol_darwin_amd64)** | [**loadgen_darwin_amd64**](https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-darwin-amd64)|
|  Linux (AMD/64)              |**[otelcol_linux_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.117.0/otelcol_linux_amd64)** | [**loadgen_linux_amd64**](https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64)|
|  Linux (ARM/64)              |**[otelcol_linux_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.117.0/otelcol_linux_arm64)** | [**loadgen_linux_arm64**](https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-arm64)|
-->

Once downloaded, update the file permissions to make them executable:

```bash { title="Update File Permissions"}
chmod +x otelcol loadgen && \
./otelcol -v && \
./loadgen --help
```

```text { title="Initial Linux/Mac Directory Structure" }
[WORKSHOP]
├── otelcol      # OpenTelemetry Collector binary
└── loadgen      # Load Generator binary
```

{{% notice note %}}
Having access to [**jq**](https://jqlang.org/download/) is recommended (installed by default on Splunk workshop instances). This lightweight command-line tool helps process and format JSON data, making it easier to inspect traces, metrics, and logs from the OpenTelemetry Collector.
{{% /notice %}}

{{% /notice %}}
