---
title: Advanced OpenTelemetry
description: In this workshop you will practice setting up the OpenTelemetry Collector configuration from scratch and go though several advanced configuration scenarios's
weight: 10
archetype: chapter
authors: ["Robert Castley", "&", "Pieter Hagen"]
time: 90 minutes
draft: true
---

The goal of this workshop is to make you comfortable creating and adjusting Opentelemetry Collector configuration files. We do this by starting with an almost empty `agent.yaml`, and configure several commonly asked scenarios.

This workshop requires a basic understanding of the OpenTelemetry Collector and the configuration file format. You will also need to be proficient in editing `YAML` files.

The whole workshop is run locally and uses the `fileexporter` as the target output for the collector.

As pre-work for the workshop, it is required that attendees download the latest of the collector (at the time of publication this was `v0.116.0`) for the device they will use during the workshop:

* Apple Mac (Arm): [otelcol_darwin_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_darwin_arm64)
* Apple Mac (Intel): [otelcol_darwin_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.115.0/otelcol_darwin_amd64)
* Windows 64: [splunk-otel-collector-0.116.0-amd64.msi](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/splunk-otel-collector-0.116.0-amd64.msi)
* Linux (Intel): [otelcol_linux_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_linux_amd64)
* Linux (Arm): [otelcol_linux_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_linux_arm64)

If none of the above match your host platform, please select and download the correct of your required build [here](https://github.com/signalfx/splunk-otel-collector/releases/tag/v0.116.0)

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

During the workshop we will run though the following topics:

* Setting up the agent locally, add meta data and introduce Debug exporter and File exporter
* Add a collector as a Gateway and route traffic from the Agent to the Gateway
* Add basic resilience to the agent
* Use the Filelog receiver to collect log data from different files
* Using processors
  * Filtering out noise (health checks) by dropping specific spans
  * Remove specific tags
  * Transform attributes to match expected format
* Setup routing to different endpoints depending on values in the data received

---
<!-- {{% children containerstyle="ul" depth="1" description="true" %}} -->
