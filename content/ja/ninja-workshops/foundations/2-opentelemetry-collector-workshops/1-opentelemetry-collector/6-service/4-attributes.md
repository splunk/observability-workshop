---
title: OpenTelemetry Collector Service
linkTitle: 6.4 Attributes
weight: 4
---

## Attributes Processor

このワークショップのProcessorsセクションで、`attributes/conf` Processorを追加し、Collectorがすべてのメトリクスに `participant.name` という新しい属性を挿入するように設定しました。次に、metricsパイプラインでこれを有効にする必要があります。

`processors` セクションを更新して、`metrics` パイプラインに `attributes/conf` を追加します。

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
