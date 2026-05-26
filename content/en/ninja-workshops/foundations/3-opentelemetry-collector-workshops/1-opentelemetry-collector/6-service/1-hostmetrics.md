---
title: OpenTelemetry Collector Service
linkTitle: 6.1 Host Metrics
weight: 1
---

## Hostmetrics Receiver

If you recall from the Receivers portion of the workshop, we defined the [**Host Metrics Receiver**](../3-receivers/#host-metrics-receiver) to generate metrics about the host system, which are scraped from various sources. To enable the receiver, we must include the `hostmetrics` receiver in the metrics pipeline.

In the `metrics` pipeline, add `hostmetrics` to the metrics `receivers` section.

```yaml {hl_lines="11"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [debug]
```
