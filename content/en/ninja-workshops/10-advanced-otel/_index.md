---
title: Advanced Opentelemetry configurations
description: In this workshop you will practice setting up the otel collector configuration from scratch and go though several  advanced configuration scenarios's
weight: 10
archetype: chapter
authors: ["Pieter Hagen", "Robert Castley"]
time: 90 minutes
draft: true
---

The goal of this workshop is to make you  comfortable creating and adjusting Opentelemetry Collector configuration files. We do this by starting with an almost empty agent.yaml, and setup though several commonly asked scenarios.

We assume basic opentelemetry collector knowledge, like understanding exporter, receivers, processors, pipelines etc. 

The whole workshop can be run locally and is using the file exporter as the target for the collector. As pre-work for the workshop, we require  attendees to download version 0.116 of the collector for the device they will use during the workshop: 

* Apple Mac (Arm):    [otelcol_darwin_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_darwin_arm64)
* Apple Mac (Intel):  [otelcol_darwin_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.115.0/otelcol_darwin_amd64)
* Windows 64:         [splunk-otel-collector-0.116.0-amd64.msi](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/splunk-otel-collector-0.116.0-amd64.msi)
* Linux (Intel):      [otelcol_linux_amd64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_linux_amd64)
* Linux (Arm):        [otelcol_linux_arm64](https://github.com/signalfx/splunk-otel-collector/releases/download/v0.116.0/otelcol_linux_arm64)

If neither of the above matches you device please choose and download the right version for your build [here](https://github.com/signalfx/splunk-otel-collector/releases/tag/v0.116.0)

Optionally you can install **jq** to pretty view the json files

Apple Mac   - brew reinstall jq
Windows 64  - choco install  jq -y
Linux       - check your install [here](https://jqlang.github.io/jq/download/)

### Agenda

during the workshop we will run though the following topics:

* Setting up the agent locally, add meta data and introduce Debug exporter and File exporter
* Add a collector as a Gateway and route traffic from the Agent to the Gateway
* Add basic resilience to the agent
* Use the Filelog receiver to collect log data from different files
* Using processors
  * filtering out noise (health checks) by dropping specific spans
  * Remove specific tags
  * Transform attributes to match expected format
* Setup routing to different endpoints depending on values in the data received

---

<!-- {{% children containerstyle="ul" depth="1" description="true" %}} -->
