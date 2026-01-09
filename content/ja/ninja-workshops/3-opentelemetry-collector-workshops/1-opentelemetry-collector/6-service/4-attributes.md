---
title: OpenTelemetry Collector Service
linkTitle: 6.4 Attributes
weight: 4
---

## Attributes Processor

また、このワークショップの Processors セクションで、Collector がすべてのメトリクスに `participant.name` という新しい属性を挿入するように `attributes/conf` processor を追加しました。ここで、metrics パイプラインでこれを有効にする必要があります。

`metrics` パイプラインの `processors` セクションに `attributes/conf` を含めるように更新します：

```yaml {hl_lines="12"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf]
      exporters: [debug]
```
