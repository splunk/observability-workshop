---
title: OpenTelemetry Collector サービス
linkTitle: 6.2 Prometheus
weight: 2
---

## Prometheus Internal レシーバー

ワークショップの前半で、`prometheus` レシーバーの名前を変更し、コレクター内部のメトリクスを収集していることを反映して、`prometheus/internal` という名前にしました。

現在、メトリクスパイプラインの下で `prometheus/internal` レシーバーを有効にする必要があります。`metrics` パイプラインの下の `receivers` セクションを更新して、`prometheus/internal` を含めます

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
