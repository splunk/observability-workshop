---
title: OpenTelemetry Collector Service
linkTitle: 6.1 Host Metrics
weight: 1
---

## Hostmetrics Receiver

ワークショップのReceiversセクションで、ホストシステムに関するメトリクスを生成するために [**Host Metrics Receiver**](../3-receivers/#host-metrics-receiver) を定義したことを思い出してください。このメトリクスはさまざまなソースから収集されます。Receiverを有効にするには、metricsパイプラインに `hostmetrics` Receiverを含める必要があります。

`metrics` パイプラインで、metricsの `receivers` セクションに `hostmetrics` を追加します。

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
