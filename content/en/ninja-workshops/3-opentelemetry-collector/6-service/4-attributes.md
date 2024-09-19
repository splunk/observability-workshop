---
title: OpenTelemetry Collector Service
linkTitle: 6.4 Attributes
weight: 4
---

## Attributes Processor

Also in the Processors section of this workshop, we added the `attributes/conf` processor so that the collector will insert a new attribute called `participant.name` to all the metrics. We now need to enable this under the metrics pipeline.

Update the `processors` section to include `attributes/conf` under the `metrics` pipeline:

```yaml {hl_lines="12"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf]
      exporters: [logging]
```
