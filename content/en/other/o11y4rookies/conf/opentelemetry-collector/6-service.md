---
title: OpenTelemetry Collector Service
linkTitle: 6. Service
weight: 6
---

The **Service** section is used to configure what components are enabled in the Collector based on the configuration found in the receivers, processors, exporters, and extensions sections. If a component is configured, but not defined within the service section then it is not enabled. The service section consists of three sub-sections:

- extensions
- pipelines
- telemetry

In the default configuration the extension section has been configured to enable `health_check`, `pprof` and `zpages` which we configured in the Extensions module earlier.

``` yaml
service:
  extensions: [health_check, pprof, zpages]
```

```yaml
service:
  pipelines:
    metrics:
      receivers: [prometheus, hostmetrics]
      processors: [batch, resourcedetection]
      exporters: [logging, otlphttp]
```

## Final configuration

``` yaml
extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679

receivers:
  hostmetrics:
    collection_interval: 10s
    scrapers:
      # CPU utilization metrics
      cpu:
      # Disk I/O metrics
      disk:
      # File System utilization metrics
      filesystem:
      # Memory utilization metrics
      memory:
      # Network interface I/O metrics & TCP connection metrics
      network:
      # CPU load metrics
      load:
      # Paging/Swap space utilization and I/O metrics
      paging:
      # Process count metrics
      processes:
      # Per process CPU, Memory and Disk I/O metrics. Disabled by default.
      # process:
  prometheus/internal:
    config:
      scrape_configs:
      - job_name: 'otel-collector'
        scrape_interval: 10s
        static_configs:
        - targets: ['0.0.0.0:8888']

processors:
  batch:
  resourcedetection:
    detectors: [system]
    override: true

exporters:
  logging:
    loglevel: info
  otlphttp:
    metrics_endpoint: https://ingest.eu0.signalfx.com/v2/datapoint/otlp
    compression: gzip
    headers:
      X-SF-TOKEN: Qz-qFy4Y85JRzw21U41f_w

service:
  pipelines:
    metrics:
      receivers: [prometheus/internal, hostmetrics]
      processors: [batch, resourcedetection]
      exporters: [logging, otlphttp]

  extensions: [health_check, pprof, zpages]
```
