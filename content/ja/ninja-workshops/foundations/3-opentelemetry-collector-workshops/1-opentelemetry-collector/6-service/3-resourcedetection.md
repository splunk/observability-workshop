---
title: OpenTelemetry Collector Service
linkTitle: 6.3 Resource Detection
weight: 3
---

## Resource Detection Processor

Collector がインスタンスのホスト名や AWS/EC2 メタデータを取得できるよう、`resourcedetection/system` と `resourcedetection/ec2` プロセッサーも追加しました。これら 2 つのプロセッサーを metrics パイプラインで有効化する必要があります。

`processors` セクションを更新して、`metrics` パイプラインに `resourcedetection/system` と `resourcedetection/ec2` を含めます。

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
