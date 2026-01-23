---
title: OpenTelemetry Collector Receivers
linkTitle: 2. Prometheus
weight: 2
---

## Prometheus Receiver

**prometheus** という別の Receiver があることにも気づくでしょう。[**Prometheus**](https://prometheus.io/docs/introduction/overview/) は、OpenTelemetry Collector が使用するオープンソースのツールキットです。この Receiver は、OpenTelemetry Collector 自体からメトリクスをスクレイピングするために使用されます。これらのメトリクスは、Collector の健全性を監視するために使用できます。

`prometheus` Receiver を変更して、Collector 自体からメトリクスを収集するためのものであることを明確にしましょう。Receiver の名前を `prometheus` から `prometheus/internal` に変更することで、その Receiver が何をしているかがより明確になります。設定ファイルを以下のように更新してください

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

## ダッシュボード例 - Prometheus メトリクス

以下のスクリーンショットは、Prometheus internal Receiver が OpenTelemetry Collector から収集するメトリクスの一部を表示するダッシュボード例です。ここでは、受け入れられたスパン、メトリクス、ログレコードと送信されたものを確認できます。

{{% notice style="note" %}}
以下のスクリーンショットは、Splunk Observability Cloud の標準（OOTB）ダッシュボードで、Splunk OpenTelemetry Collector のインストール状況を簡単に監視できます。
{{% /notice %}}

![otel-charts](../../images/otel-charts.png)
