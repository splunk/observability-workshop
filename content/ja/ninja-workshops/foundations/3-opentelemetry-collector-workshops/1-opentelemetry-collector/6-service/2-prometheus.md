---
title: OpenTelemetry Collector Service
linkTitle: 6.2 Prometheus
weight: 2
---

## Prometheus Internal Receiver

ワークショップの前半で、`prometheus` レシーバーが Collector 内部のメトリクスを収集していることを反映させるため、`prometheus/internal` という名前に変更しました。

ここで、メトリクスパイプラインで `prometheus/internal` レシーバーを有効化する必要があります。`receivers` セクションを更新し、`metrics` パイプラインに `prometheus/internal` を追加してください:

```yaml {hl_lines="11"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch]
      exporters: [debug]
```
