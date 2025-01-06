---
title: Advanced otel building Dashboards & Detectors
description: The following workshops introduce you to advanced otel
weight: 8
archetype: chapter
authors: ["Pieter Hagen", "Robert Castley"]
time: 45 minutes
draft: true
---

The goal of this workshop is to introduce you to the concepts of ....

### Agenda

****  Setting up agent as and via Gateway
* Adding different log files  https://github.com/signalfx/splunk-otel-collector/tree/main/examples/otel-logs-routing
**** * set up resilience, (network outage etc) https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/examples/fault-tolerant-logs-collection
* Using processors
  - filtering out noise (health checks)
  - removing specific tags
  - adding meta data [log-enrichment](https://github.com/signalfx/splunk-otel-collector/blob/main/examples/log-enrichment/otel-collector-config.yml)
* Sampling
**** * sending to different org conditionally  https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/connector/routingconnector/README.md
****  Get Data from collectd [collectd] (https://github.com/signalfx/splunk-otel-collector/tree/main/examples/collectd)
* otel bin
---

<!-- {{% children containerstyle="ul" depth="1" description="true" %}} -->
