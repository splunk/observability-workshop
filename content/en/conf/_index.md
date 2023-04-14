---
title: Newbie to Ninja - OpenTelemetry Collector
linkTitle: Newbie to Ninja - OpenTelemetry Collector
description: This workshop will equip you with the basic understanding of monitoring Kubernetes using the Splunk OpenTelemetry Collector
weight: 1
alwaysopen: false
draft: true
---

## Overview

[https://docs.splunk.com/Observability/gdi/other-ingestion-methods/upstream-collector.html#nav-Send-telemetry-using-OpenTelemetry-Collector-Contrib](https://docs.splunk.com/Observability/gdi/other-ingestion-methods/upstream-collector.html#nav-Send-telemetry-using-OpenTelemetry-Collector-Contrib)

- OpenTelemetry Collector Contrib - https://github.com/open-telemetry/opentelemetry-collector-releases/releases/tag/v0.75.0

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

**Default configuration**

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
