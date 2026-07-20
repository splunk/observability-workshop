---
title: OpenTelemetry Collector Service
linkTitle: 6.2 Prometheus
weight: 2
---

## Prometheus Internal Receiver

このワークショップの前半で、`prometheus` Receiverがコレクター内部のメトリクスを収集していることを反映するために、`prometheus/internal`にリネームしました。

ここで、metricsパイプラインの下で `prometheus/internal` Receiverを有効にする必要があります。`metrics`パイプラインの`receivers`セクションに `prometheus/internal` を追加します:

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
