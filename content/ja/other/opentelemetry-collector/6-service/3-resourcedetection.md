---
title: OpenTelemetry Collector サービス
linkTitle: 6.3 Resource Detection
weight: 3
---

## Resource Detection プロセッサー

また、コレクターがインスタンスのホスト名やAWS/EC2のメタデータを取得できるように、`resourcedetection/system` および `resourcedetection/ec2` プロセッサーを追加しました。これらのプロセッサーをメトリクスパイプライン下で有効にする必要があります。

`metrics` パイプラインの下の `processors` セクションを更新して、`resourcedetection/system` および `resourcedetection/ec2` を追加します

```yaml {hl_lines="12"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2]
      exporters: [logging]
```
