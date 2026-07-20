---
title: OpenTelemetry Collector Receivers
linkTitle: 2. Prometheus
weight: 2
---

## Prometheus Receiver

**prometheus** というもう一つのReceiverがあることに気付くでしょう。[**Prometheus**](https://prometheus.io/docs/introduction/overview/) はOpenTelemetry Collectorが使用するオープンソースツールキットです。このReceiverはOpenTelemetry Collector自体からメトリクスをスクレイプするために使用されます。これらのメトリクスはCollectorの健全性を監視するために利用できます。

`prometheus` Receiverを修正して、Collector自体からメトリクスを収集するためのものであることを明確にしましょう。Receiverの名前を `prometheus` から `prometheus/internal` に変更することで、そのReceiverが何をしているのかがより明確になります。設定ファイルを以下のように更新します。

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

## ダッシュボードの例 - Prometheusメトリクス

以下のスクリーンショットは、Prometheus内部ReceiverがOpenTelemetry Collectorから収集するメトリクスの一部を表示するダッシュボードの例です。ここでは、受け入れられたSpan、メトリクス、ログレコードの送受信状況を確認できます。

{{% notice style="note" %}}
以下のスクリーンショットはSplunk Observability Cloudのすぐに使える（OOTB）ダッシュボードで、Splunk OpenTelemetry Collectorのインストール環境を簡単に監視できます。
{{% /notice %}}

![otel-charts](../../images/otel-charts.png)
