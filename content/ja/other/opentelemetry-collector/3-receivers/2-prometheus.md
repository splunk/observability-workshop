---
title: OpenTelemetry Collector レシーバー
linkTitle: 2. Prometheus
weight: 2
---

## Prometheus レシーバー

**Prometheus** のレシーバーも、もちろんあります。[Prometheus](https://prometheus.io/docs/introduction/overview/) は OpenTelemetry Collector で使われているオープンソースのツールキットです。このレシーバーは、OpenTelemetry Collector 自身からメトリクスをスクレイピングするためにも使われます。これらのメトリクスは、コレクタの健全性をモニタリングするために使用できる。

ここでは、**prometheus** レシーバーを変更して、コレクター自身からメトリクスを収集できるようにしてみます。レシーバーの名前を **prometheus** から **prometheus/internal** に変更して、レシーバーが何をしているのかをより明確しましょう。設定ファイルを以下のように更新します：

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


上記の設定では、OpenTelemetry Collector 自身が公開している Prometheus エンドポイントをスクレイピングしています。どのような情報が得られるか、`curl` コマンドで試すことができます:

```bash
curl http://localhost:8888/metrics
```


{{% notice title="Tips: コンポーネントに名前をつける" style="info" %}}
レシーバー、プロセッサー、エクスポーター、パイプラインなどのコンポーネントは、 `otlp` や `otlp/2` のように、 `type[/name]` 形式に従った識別子によって定義されます。識別子が一意である限り、与えられたタイプのコンポーネントを複数回定義することができるようになります。

ここでは `prometheus/internal` という識別子でこのコンポーネントを特定できるようにしたので、別の `prometheus` レシーバーを追加して、監視対象インスタンスの Prometheus エンドポイントをスクレイピングさせることもできます。
{{% /notice %}}


## ダッシュボード例 - Prometheus メトリクス

このスクリーンショットは、 `prometheus/internal` レシーバーが OpenTelemetry Collector から収集したメトリクスの、spmeのダッシュボードの例です。ここではスパン・メトリクス・ログの、それぞれの受信および送信の様子を見ることができます。

{{% notice style="note" %}}
このダッシュボードはSplunk Observability Cloud にある組み込みダッシュボードで、Splunk OpenTelemetry Collector のインストールの状況を簡単にモニタリングできます。
{{% /notice %}}


![otel-charts](../../images/otel-charts.png)
