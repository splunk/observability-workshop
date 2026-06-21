---
title: タグをダッシュボードで使用する
linkTitle: 1. ダッシュボードでの使用
weight: 1
time: 5 minutes
---

### ダッシュボード

**Metric Finder** に移動し、タグの名前である `credit_score_category` を入力します（Monitoring MetricSet が作成された際に、タグ名のドットがアンダースコアに置換されたことを思い出してください）。このタグをディメンションとして含む複数のメトリクスが表示されます

![Metric Finder](../../images/metric_finder.png)

デフォルトでは、**Splunk Observability Cloud** は受信したトレースデータを使用していくつかのメトリクスを計算します。詳細については [Learn about MetricSets in APM](https://docs.splunk.com/observability/en/apm/span-tags/metricsets.html) を参照してください。

MMS を作成することで、`credit_score_category` がこれらのメトリクスにディメンションとして追加されました。これにより、このディメンションをアラートやダッシュボードに使用できるようになります。

その方法を確認するために、`service.request.duration.ns.p99` という名前のメトリクスをクリックしてみましょう。次のチャートが表示されます

![Service Request Duration](../../images/service_request_duration_chart.png)

`sf_environment`、`sf_service`、`sf_dimensionalized` のフィルターを追加します。次に、**Extrapolation policy** を `Last value` に、**Display units** を `Nanosecond` に設定します

![Chart with Seconds](../../images/chart_settings.png)

これらの設定により、クレジットスコアカテゴリ別のサービスリクエスト期間をチャートで可視化できます

![Duration by Credit Score](../../images/duration_by_credit_score.png)

これでクレジットスコアカテゴリ別の期間を確認できます。この例では、赤い線が `exceptional` カテゴリを表しており、これらのリクエストの期間が最大5秒まで達することがあることがわかります。

オレンジは `very good` カテゴリを表しており、非常に高速なレスポンスタイムを示しています。

緑の線は `poor` カテゴリを表しており、レスポンスタイムは2〜3秒の間です。

このチャートを今後の参照用にダッシュボードに保存すると便利かもしれません。そのためには、**Save as...** ボタンをクリックしてチャートの名前を入力します

![Save Chart As](../../images/save_chart_as.png)

チャートを保存するダッシュボードを尋ねられたら、`Credit Check Service - Your Name`（実際の名前に置き換えてください）という名前で**新しい**ダッシュボードを作成しましょう

![Save Chart As](../../images/create_dashboard.png)

これでダッシュボードにチャートが表示され、クレジットチェックサービスを監視するために必要に応じてさらにチャートを追加できます

![Credit Check Service Dashboard](../../images/credit_check_service_dashboard.png)
