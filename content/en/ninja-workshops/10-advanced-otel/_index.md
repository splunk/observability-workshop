---
title: Advanced OpenTelemetry
description: In this workshop you will practice setting up the OpenTelemetry Collector configuration from scratch and go though several advanced configuration scenarios's
weight: 10
archetype: chapter
authors: ["Robert Castley,", "Charity Anderson", "&", "Pieter Hagen"]
time: 90 minutes
draft: true
---

The goal of this workshop is to make you comfortable creating and adjusting Opentelemetry Collector configuration files. You will do this by starting with an almost empty `agent.yaml`, and configure several common advanced scenarios.

This workshop requires a basic understanding of the OpenTelemetry Collector and the configuration file format. You will also need to be proficient in editing **YAML** files. The whole workshop is run locally and uses the **File Exporter** as the target output for the collector, thus negating the need for a backend to send data to.

Create a directory on your machine where you will run the workshop e.g. `collector`, we will refer to this directory as `[WORKSHOP]` in the instructions. Download the latest of the collector (at the time of publication this was `v0.116.0`) for the device you will be using during the workshop and place it in the `[WORKSHOP]` directory.

* Apple Mac (Apple Silicon): [otelcol_darwin_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_darwin_arm64)
* Apple Mac (Intel): [otelcol_darwin_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.115.0/otelcol_darwin_amd64)
* Windows AMD/64: [otelcol_windows_amd64.exe](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_windows_amd64.exe)
* Linux (AMD/64): [otelcol_linux_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_linux_amd64)
* Linux (ARM/64): [otelcol_linux_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_linux_arm64)

{{% notice title="Note" style="info" icon="info" %}}
If none of the above match your host platform, please select and download the correct of your required build [**here**](https://github.com/signalfx/splunk-otel-collector/releases/tag/v0.116.0).
{{% /notice %}}

Once downloaded, rename the file to `otelcol` (or `otelcol.exe` on Windows).

<!--
Optionally, you can install `jq` to pretty view the json files:

###### Apple Mac

```bash
brew install jq
```

###### Windows 64

```bash
choco install  jq -y
```

###### Linux

Check your install **[here](https://jqlang.github.io/jq/download/)**

### Agenda
-->

During the workshop we will run though the following topics:

* Setting up the agent locally, add meta data and introduce the **debug** and **file** exporters
* Configure a gateway and route traffic from the agent to the gateway
* Configure basic resilience to the agent
* Configure the **filelog** receiver to collect log data from different files
* Configure processors:
  * Filter out noise (health checks) by dropping specific spans
  * Remove specific tags
  * Transform attributes to match expected format
* Configure routing to different endpoints based upon on values in the data received

---
<!-- {{% children containerstyle="ul" depth="1" description="true" %}} -->
