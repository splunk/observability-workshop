---
title: OpenTelemetry Collector Service
linkTitle: 6.2 Prometheus
weight: 2
---

## Prometheus Internal Receiver

Earlier in the workshop, we also renamed the `prometheus` receiver to reflect that is was collecting metrics internal to the collector, renaming it to `prometheus/internal`.

 We now need to enable the `prometheus/internal` receiver under the metrics pipeline. Update the `receivers` section to include `prometheus/internal` under the `metrics` pipeline:

```yaml {hl_lines="11"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch]
      exporters: [logging]
```
