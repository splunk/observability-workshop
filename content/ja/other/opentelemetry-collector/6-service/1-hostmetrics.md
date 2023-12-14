---
title: OpenTelemetry Collector サービス
linkTitle: 6.1 Host Metrics
weight: 1
---

## Hostmetrics レシーバー

ワークショップのレシーバー部分で振り返ると、ホストシステムに関するメトリクスを生成するために、様々なソースからスクレイピングする [Host Metrics](../3-receivers/#host-metrics-receiver) レシーバーを定義しました。このレシーバーを有効にするためには、メトリクスパイプラインに `hostmetrics` レシーバーを含める必要があります。

`metrics` パイプラインで、メトリクスの `receivers` セクションに `hostmetrics` を追加します。

```yaml {hl_lines="11"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [logging]
```
