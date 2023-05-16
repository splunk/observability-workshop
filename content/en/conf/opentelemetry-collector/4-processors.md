---
title: OpenTelemetry Collector Processors
linkTitle: 4. Processors
weight: 4
---

[Processors](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/README.md) are run on data between being received and being exported. Processors are optional though some are recommended. There are [a large number of processors](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor) included in the OpenTelemetry contrib Collector.

## Batch Processor

By default, only the **batch** processor is enabled. This processor is used to batch up data before it is exported. This is useful for reducing the number of network calls made to exporters. For this workshop we will accept the defaults (`send_batch_size: 8192`, `timeout: 200ms`, `send_batch_size_max: 0`).

## Resource Detection Processor

The resource detection processor can be used to detect resource information from the host and append or override the resource value in telemetry data with this information.

By default, the hostname is set to the FQDN if possible, otherwise the hostname provided by the OS is used as a fallback. This logic can be changed from using using the `hostname_sources` configuration option. To avoid getting the FQDN and use the hostname provided by the OS, we will set the `hostname_sources` to `os`.

{{< tabs >}}
{{% tab name="Resource Detection Processor Configuration" %}}

``` yaml
processors:
  batch:
  resourcedetection:
    detectors: [system]
    system:
      hostname_sources: [os]
```

{{% /tab %}}
{{% tab name="Resource Detection Processor Configuration Complete" %}}

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
  otlp:
    protocols:
      grpc:
      http:

  opencensus:

  # Collect own metrics
  prometheus/internal:
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
  resourcedetection:
    detectors: [system]
    system:
      hostname_sources: [os]

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
  
{{% /tab %}}
{{< /tabs >}}

Robert, thoughts on metrics transform processor example here?

https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/metricstransformprocessor
