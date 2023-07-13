---
title: OpenTelemetry Collector Service
linkTitle: 6.3 Resource Detection
weight: 3
---

## Resource Detection Processor

We also added `resourcedetection/system` and `resourcedetection/ec2` processors so that the collector can capture the instance hostname and AWS/EC2 metadata. We now need to enable these two processors under the metrics pipeline.

Update the `processors` section to include `resourcedetection/system` and `resourcedetection/ec2` under the `metrics` pipeline:

```yaml {hl_lines="12"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2]
      exporters: [logging]
```
