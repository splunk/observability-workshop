---
title: OpenTelemetry Collector Service
linkTitle: 6.3 Resource Detection
weight: 3
---

## Resource Detection Processor

また、Collector がインスタンスのホスト名と AWS/EC2 メタデータをキャプチャできるように、`resourcedetection/system` と `resourcedetection/ec2` processor を追加しました。ここで、metrics パイプラインでこれら2つの processor を有効にする必要があります。

`metrics` パイプラインの `processors` セクションに `resourcedetection/system` と `resourcedetection/ec2` を含めるように更新します：

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
