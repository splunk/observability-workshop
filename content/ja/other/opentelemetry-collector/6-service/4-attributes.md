---
title: OpenTelemetry Collector サービス
linkTitle: 6.4 Attributes
weight: 4
---

## Attributes プロセッサー

また、このワークショップのプロセッサーセクションでは、`attributes/conf` プロセッサーを追加し、コレクターがすべてのメトリクスに `participant.name` という新しい属性を挿入するようにしました。これをメトリクスパイプライン下で有効にする必要があります。

`metrics` パイプラインの下の `processors` セクションを更新して、`attributes/conf` を追加します

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
