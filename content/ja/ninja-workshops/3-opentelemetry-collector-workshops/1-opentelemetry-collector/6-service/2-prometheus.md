---
title: OpenTelemetry Collector Service
linkTitle: 6.2 Prometheus
weight: 2
---

## Prometheus Internal Receiver

ワークショップの前半で、Collector 内部のメトリクスを収集していることを反映するために `prometheus` receiver の名前を `prometheus/internal` に変更しました。

ここで、metrics パイプラインで `prometheus/internal` receiver を有効にする必要があります。`metrics` パイプラインの `receivers` セクションに `prometheus/internal` を含めるように更新します：

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
