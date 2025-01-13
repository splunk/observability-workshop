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
** adding basic resillince to the agent
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


Pre req  done before the session:

 download the splunk version of the collector  for your platform version X -> urls for mac os arm macos intel windows 64 and linux 64 AMD

  https://github.com/signalfx/splunk-otel-collector/releases/download/v0.115.0/otelcol_darwin_arm64
  https://github.com/signalfx/splunk-otel-collector/releases/download/v0.115.0/splunk-otel-collector-0.115.0-amd64.msi 

  https://github.com/signalfx/splunk-otel-collector/releases/download/v0.115.0/otelcol_darwin_amd64



  install brew macos
 
 chocolatey install windows:
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
 
 install jq using  either platform

 install collect D vi brew on mac  -> windows 

<!-- {{% children containerstyle="ul" depth="1" description="true" %}} -->
