---
title: OpenTelemetry Collector Service
linkTitle: 6.1 Host Metrics
weight: 1
---

## Hostmetrics Receiver

ワークショップの Receivers セクションで、さまざまなソースからスクレイプされるホストシステムに関するメトリクスを生成する [**Host Metrics Receiver**](../3-receivers/#host-metrics-receiver) を定義したことを思い出してください。この receiver を有効にするには、metrics パイプラインに `hostmetrics` receiver を含める必要があります。

`metrics` パイプラインで、metrics の `receivers` セクションに `hostmetrics` を追加します。

```yaml {hl_lines="11"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [debug]
```
