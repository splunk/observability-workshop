---
title: OpenTelemetry Collector Receivers
linkTitle: 2. Prometheus
weight: 2
---

## Prometheus Receiver

**prometheus** という別の receiver にも気づくはずです。[**Prometheus**](https://prometheus.io/docs/introduction/overview/) は OpenTelemetry Collector で利用されているオープンソースのツールキットです。この receiver は OpenTelemetry Collector 自身からメトリクスをスクレイピングするために使用されます。これらのメトリクスは Collector の健全性を監視するために利用できます。

`prometheus` receiver が Collector 自身からメトリクスを収集していることを明確に示すよう変更してみましょう。receiver の名前を `prometheus` から `prometheus/internal` に変更することで、その receiver が何をしているのかがより分かりやすくなります。設定ファイルを以下のように更新します:

{{% tab title="Prometheus Receiver Configuration" %}}

```yaml {hl_lines="1"}
prometheus/internal:
  config:
    scrape_configs:
    - job_name: 'otel-collector'
      scrape_interval: 10s
      static_configs:
      - targets: ['0.0.0.0:8888']
```

{{% /tab %}}

## ダッシュボードの例 - Prometheus メトリクス

次のスクリーンショットは、Prometheus internal receiver が OpenTelemetry Collector から収集するメトリクスのいくつかをダッシュボードで示した例です。ここでは、受け入れられた、および送信された spans、metrics、log records を確認できます。

{{% notice style="note" %}}
次のスクリーンショットは、Splunk Observability Cloud のすぐに使える (OOTB) ダッシュボードであり、Splunk OpenTelemetry Collector のインストール基盤を簡単に監視できます。
{{% /notice %}}

![otel-charts](../../images/otel-charts.png)
