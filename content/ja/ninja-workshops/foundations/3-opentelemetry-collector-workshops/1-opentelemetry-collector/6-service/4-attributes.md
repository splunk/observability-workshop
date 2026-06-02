---
title: OpenTelemetry Collector Service
linkTitle: 6.4 Attributes
weight: 4
---

## Attributes Processor

このワークショップの Processors セクションでも、`attributes/conf` プロセッサーを追加して、Collector がすべてのメトリクスに `participant.name` という新しい属性を挿入するようにしました。次に、これを metrics パイプラインで有効化する必要があります。

`processors` セクションを更新して、`metrics` パイプラインに `attributes/conf` を含めます。

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
