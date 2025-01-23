---
title: Advanced OpenTelemetry
description: In this workshop you will practice setting up the OpenTelemetry Collector configuration from scratch and go though several advanced configuration scenarios's
weight: 10
archetype: chapter
authors: ["Robert Castley,", "Charity Anderson", "&", "Pieter Hagen"]
time: 90 minutes
#draft: true
hidden: true
---

The goal of this workshop is to help you become comfortable creating and modifying OpenTelemetry Collector configuration files. You’ll start with a minimal `agent.yaml` file and gradually configure several common advanced scenarios.

To get the most out of this workshop, you should have a basic understanding of the OpenTelemetry Collector and its configuration file format. Additionally, proficiency in editing YAML files is required. The entire workshop is designed to run locally, using the File Exporter as the target output for the collector, so you won’t need a backend to send data to.

### Prerequisites

1. **Create a directory** on your machine for the workshop (e.g., `collector`). We will refer to this directory as `[WORKSHOP]` in the instructions.
2. **Download the latest OpenTelemetry Collector release** for your platform and place it in the `[WORKSHOP]` directory.

The appropriate binary for your platform is:

- **Apple Mac (Apple Silicon): [otelcol_darwin_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.117.0/otelcol_darwin_arm64)**
- **Apple Mac (Intel): [otelcol_darwin_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.117.0/otelcol_darwin_amd64)**
- **Windows AMD/64: [otelcol_windows_amd64.exe](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.117.0/otelcol_windows_amd64.exe)**
- **Linux (AMD/64): [otelcol_linux_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.117.0/otelcol_linux_amd64)**
- **Linux (ARM/64): [otelcol_linux_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.117.0/otelcol_linux_arm64)**

{{% notice title="Note" style="info" icon="info" %}}
If none of the above match your host platform, please select and download the correct of your required build [**here**](https://github.com/signalfx/splunk-otel-collector/releases/tag/v0.116.0).
{{% /notice %}}

Once downloaded, rename the file to `otelcol` (or `otelcol.exe` on Windows). For Mac/Linux, set the file permissions to allow execution:

```bash
chmod +x otelcol
```

```text
[WORKSHOP]
└── otelcol    # OpenTelemetry Collector binary
```

For Mac users you will need trust the executable - **[https://support.apple.com/en-mide/102445](https://support.apple.com/en-mide/102445)**.

### Workshop Overview

During this workshop, we will cover the following topics:

- **Setting up the agent locally**: Add metadata, and introduce the debug and file exporters.
- **Configuring a gateway**: Route traffic from the agent to the gateway.
- **Configuring the `filelog` receiver**: Collect log data from various log files.
- **Enhancing agent resilience**: Basic configurations for fault tolerance.
- **Configuring processors**:
  - Filter out noise by dropping specific spans (e.g., health checks).
  - Remove unnecessary tags.
  - Transform attributes to match the expected format.
  - Route data to different endpoints based on the values received.

By the end of this workshop, you'll be familiar with configuring the OpenTelemetry Collector for a variety of real-world use cases.
