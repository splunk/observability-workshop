---
title: Newbie to Ninja - OpenTelemetry Collector
linkTitle: Newbie to Ninja - OpenTelemetry Collector
description: This workshop will equip you with the basic understanding of monitoring Kubernetes using the Splunk OpenTelemetry Collector
weight: 2
alwaysopen: false
---

### Abstract

Adopting OpenTelemetry within your organisation can bring issues such as dealing with metric naming changes, rollout, and where to start. In this workshop, we will be focusing on using the OpenTelemetry collector and starting with the fundamentals of configuring the receivers, processors, and exporters ready to use with Splunk Cloud. The journey will take attendees from novices to being able to start adding custom components to help solve for their business observability needs for their distributed platform.

### Target Audience

This talk is for developers and system administrators who are interested in learning more about OpenTelemetry.

### Prerequisites

- Attendees should have a basic understanding of distributed systems and data collection.
- A instance/host/VM running Ubuntu 20.04 LTS or 22.04 LTS.

### Learning Objectives

By the end of this talk, attendees will be able to:

- Understand the components of OpenTelemetry
- Use receivers, processors, and exporters to collect, instrument, and analyze data from distributed systems
- Identify the benefits of using OpenTelemetry
- Building a custom component to solve for their business needs

{{< mermaid >}}
%%{
  init:{
    "theme":"base",
    "themeVariables": {
      "primaryColor": "#ffffff",
      "clusterBkg": "#eff2fb",
      "defaultLinkColor": "#333333"
    }
  }
}%%

flowchart LR;
    subgraph Collector
    A[OTLP] --> M(Receivers)
    B[JAEGER] --> M(Receivers)
    C[Prometheus] --> M(Receivers)
    end
    subgraph Processors
    M(Receivers) --> H(Filters, Attributes, etc)
    E(Extensions)
    end
    subgraph Exporters
    H(Filters, Attributes, etc) --> S(OTLP)
    H(Filters, Attributes, etc) --> T(JAEGER)
    H(Filters, Attributes, etc) --> U(Prometheus)
    end
{{< /mermaid >}}

## Overview

[https://www.aspecto.io/blog/opentelemetry-collector-guide/](https://www.aspecto.io/blog/opentelemetry-collector-guide/)

[https://docs.splunk.com/Observability/gdi/other-ingestion-methods/upstream-collector.html#nav-Send-telemetry-using-OpenTelemetry-Collector-Contrib](https://docs.splunk.com/Observability/gdi/other-ingestion-methods/upstream-collector.html#nav-Send-telemetry-using-OpenTelemetry-Collector-Contrib)

- OpenTelemetry Collector Contrib - [https://github.com/open-telemetry/opentelemetry-collector-releases/releases/tag/v0.75.0](https://github.com/open-telemetry/opentelemetry-collector-releases/releases/tag/v0.75.0)

[https://opentelemetry.io/docs/collector/configuration/](https://opentelemetry.io/docs/collector/configuration/)

- Extensions
- Recievers
- Processors
  - [https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/metricstransformprocessor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/metricstransformprocessor)
- Exporters
- Pipelines

![OTel Collector](https://opentelemetry.io/docs/collector/img/otel-collector.svg)

Vanilla/Contrib/Vendor

- Host metrics and metadata into O11y Cloud
- Research using OTel Log Collection

- Metrics into O11y
- Logs into Core

- Building a custom component
- Edit config to include new component
- Demonstate metrics from new component

### Default configuration

```yaml
extensions:
  health_check:
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679

receivers:
  otlp:
    protocols:
      grpc:
      http:

  opencensus:

  # Collect own metrics
  prometheus:
    config:
      scrape_configs:
      - job_name: 'otel-collector'
        scrape_interval: 10s
        static_configs:
        - targets: ['0.0.0.0:8888']

  jaeger:
    protocols:
      grpc:
      thrift_binary:
      thrift_compact:
      thrift_http:

  zipkin:

processors:
  batch:

exporters:
  logging:
    verbosity: detailed

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [logging]

  extensions: [health_check, pprof, zpages]
```

### Splunk OTel Host install default configuration

```yaml
# Default configuration file for the Linux (deb/rpm) and Windows MSI collector packages

# If the collector is installed without the Linux/Windows installer script, the following
# environment variables are required to be manually defined or configured below:
# - SPLUNK_ACCESS_TOKEN: The Splunk access token to authenticate requests
# - SPLUNK_API_URL: The Splunk API URL, e.g. https://api.us0.signalfx.com
# - SPLUNK_BUNDLE_DIR: The path to the Smart Agent bundle, e.g. /usr/lib/splunk-otel-collector/agent-bundle
# - SPLUNK_COLLECTD_DIR: The path to the collectd config directory for the Smart Agent, e.g. /usr/lib/splunk-otel-collector/agent-bundle/run/collectd
# - SPLUNK_HEC_TOKEN: The Splunk HEC authentication token
# - SPLUNK_HEC_URL: The Splunk HEC endpoint URL, e.g. https://ingest.us0.signalfx.com/v1/log
# - SPLUNK_INGEST_URL: The Splunk ingest URL, e.g. https://ingest.us0.signalfx.com
# - SPLUNK_TRACE_URL: The Splunk trace endpoint URL, e.g. https://ingest.us0.signalfx.com/v2/trace

extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  http_forwarder:
    ingress:
      endpoint: 0.0.0.0:6060
    egress:
      endpoint: "${SPLUNK_API_URL}"
      # Use instead when sending to gateway
      #endpoint: "${SPLUNK_GATEWAY_URL}"
  smartagent:
    bundleDir: "${SPLUNK_BUNDLE_DIR}"
    collectd:
      configDir: "${SPLUNK_COLLECTD_DIR}"
  zpages:
    #endpoint: 0.0.0.0:55679
  memory_ballast:
    # In general, the ballast should be set to 1/3 of the collector's memory, the limit
    # should be 90% of the collector's memory.
    # The simplest way to specify the ballast size is set the value of SPLUNK_BALLAST_SIZE_MIB env variable.
    size_mib: ${SPLUNK_BALLAST_SIZE_MIB}

receivers:
  fluentforward:
    endpoint: 127.0.0.1:8006
  hostmetrics:
    collection_interval: 10s
    scrapers:
      cpu:
      disk:
      filesystem:
      memory:
      network:
      # System load average metrics https://en.wikipedia.org/wiki/Load_(computing)
      load:
      # Paging/Swap space utilization and I/O metrics
      paging:
      # Aggregated system process count metrics
      processes:
      # System processes metrics, disabled by default
      # process:
  jaeger:
    protocols:
      grpc:
        endpoint: 0.0.0.0:14250
      thrift_binary:
        endpoint: 0.0.0.0:6832
      thrift_compact:
        endpoint: 0.0.0.0:6831
      thrift_http:
        endpoint: 0.0.0.0:14268
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
  # This section is used to collect the OpenTelemetry Collector metrics
  # Even if just a Splunk APM customer, these metrics are included
  prometheus/internal:
    config:
      scrape_configs:
      - job_name: 'otel-collector'
        scrape_interval: 10s
        static_configs:
        - targets: ['0.0.0.0:8888']
        metric_relabel_configs:
          - source_labels: [ __name__ ]
            regex: '.*grpc_io.*'
            action: drop
  smartagent/signalfx-forwarder:
    type: signalfx-forwarder
    listenAddress: 0.0.0.0:9080
  smartagent/processlist:
    type: processlist
  signalfx:
    endpoint: 0.0.0.0:9943
    # Whether to preserve incoming access token and use instead of exporter token
    # default = false
    #access_token_passthrough: true
  zipkin:
    endpoint: 0.0.0.0:9411

processors:
  batch:
  # Enabling the memory_limiter is strongly recommended for every pipeline.
  # Configuration is based on the amount of memory allocated to the collector.
  # For more information about memory limiter, see
  # https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/memorylimiter/README.md
  memory_limiter:
    check_interval: 2s
    limit_mib: ${SPLUNK_MEMORY_LIMIT_MIB}

  # Detect if the collector is running on a cloud system, which is important for creating unique cloud provider dimensions.
  # Detector order is important: the `system` detector goes last so it can't preclude cloud detectors from setting host/os info.
  # Resource detection processor is configured to override all host and cloud attributes because instrumentation
  # libraries can send wrong values from container environments.
  # https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor#ordering
  resourcedetection:
    detectors: [system, gcp, ecs, ec2, azure]
    override: true

  # Optional: The following processor can be used to add a default "deployment.environment" attribute to the logs and
  # traces when it's not populated by instrumentation libraries.
  # If enabled, make sure to enable this processor in the pipeline below.
  #resource/add_environment:
    #attributes:
      #- action: insert
        #value: staging/production/...
        #key: deployment.environment

exporters:
  # Traces
  sapm:
    access_token: "${SPLUNK_ACCESS_TOKEN}"
    endpoint: "${SPLUNK_TRACE_URL}"
  # Metrics + Events
  signalfx:
    access_token: "${SPLUNK_ACCESS_TOKEN}"
    api_url: "${SPLUNK_API_URL}"
    ingest_url: "${SPLUNK_INGEST_URL}"
    # Use instead when sending to gateway
    #api_url: http://${SPLUNK_GATEWAY_URL}:6060
    #ingest_url: http://${SPLUNK_GATEWAY_URL}:9943
    sync_host_metadata: true
    correlation:
  # Logs
  splunk_hec:
    token: "${SPLUNK_HEC_TOKEN}"
    endpoint: "${SPLUNK_HEC_URL}"
    source: "otel"
    sourcetype: "otel"
  # Send to gateway
  otlp:
    endpoint: "${SPLUNK_GATEWAY_URL}:4317"
    tls:
      insecure: true
  # Debug
  logging:
    loglevel: debug

service:
  extensions: [health_check, http_forwarder, zpages, memory_ballast, smartagent]
  pipelines:
    traces:
      receivers: [jaeger, otlp, smartagent/signalfx-forwarder, zipkin]
      processors:
      - memory_limiter
      - batch
      - resourcedetection
      #- resource/add_environment
      exporters: [sapm, signalfx]
      # Use instead when sending to gateway
      #exporters: [otlp, signalfx]
    metrics:
      receivers: [hostmetrics, otlp, signalfx, smartagent/signalfx-forwarder]
      processors: [memory_limiter, batch, resourcedetection]
      exporters: [signalfx]
      # Use instead when sending to gateway
      #exporters: [otlp]
    metrics/internal:
      receivers: [prometheus/internal]
      processors: [memory_limiter, batch, resourcedetection]
      # When sending to gateway, at least one metrics pipeline needs
      # to use signalfx exporter so host metadata gets emitted
      exporters: [signalfx]
    logs/signalfx:
      receivers: [signalfx, smartagent/processlist]
      processors: [memory_limiter, batch, resourcedetection]
      exporters: [signalfx]
      # Use instead when sending to gateway
      #exporters: [otlp]
    logs:
      receivers: [fluentforward, otlp]
      processors:
      - memory_limiter
      - batch
      - resourcedetection
      #- resource/add_environment
      exporters: [splunk_hec]
      # Use instead when sending to gateway
      #exporters: [otlp]
```
