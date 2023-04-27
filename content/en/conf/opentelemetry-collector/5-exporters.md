---
title: OpenTelemetry Collector Exporters
linkTitle: 5. Exporters
weight: 5
---

An exporter, which can be push or pull based, is how you send data to one or more backends/destinations. Exporters may support one or more data sources.

```yaml
exporters:
  logging:
    verbosity: detailed
  otlphttp:
    metrics_endpoint: https://ingest.eu0.signalfx.com/v2/datapoint/otlp
    compression: gzip
    headers:
      X-SF-TOKEN: <redacted>
```

```yaml
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [otlp, opencensus, prometheus, hostmetrics]
      processors: [batch, resourcedetection]
      exporters: [logging, otlphttp]
```
