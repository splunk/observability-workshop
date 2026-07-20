---
title: OpenTelemetry Collector Service
linkTitle: 6.3 Resource Detection
weight: 3
---

## Resource Detection Processor

また、Collectorがインスタンスのホスト名とAWS/EC2メタデータを取得できるように、`resourcedetection/system` と `resourcedetection/ec2` Processorを追加しました。次に、metricsパイプラインでこれら2つのProcessorを有効にする必要があります。

`processors` セクションを更新して、`metrics` パイプラインに `resourcedetection/system` と `resourcedetection/ec2` を追加します。

```yaml {hl_lines="12"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2]
      exporters: [debug]
```
