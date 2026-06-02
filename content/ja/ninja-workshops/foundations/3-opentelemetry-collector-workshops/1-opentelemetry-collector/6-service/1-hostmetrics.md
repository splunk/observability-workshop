---
title: OpenTelemetry Collector Service
linkTitle: 6.1 Host Metrics
weight: 1
---

## Hostmetrics Receiver

ワークショップの Receivers セクションを思い出してください。[**Host Metrics Receiver**](../3-receivers/#host-metrics-receiver) は、さまざまなソースからスクレイピングされる、ホストシステムに関するメトリクスを生成するために定義しました。このレシーバーを有効化するには、metrics パイプラインに `hostmetrics` レシーバーを含める必要があります。

`metrics` パイプラインの `receivers` セクションに `hostmetrics` を追加します。

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
