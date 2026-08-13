---
title: RUM アプリケーション概要
linkTitle: 2. App Overview
weight: 2
time: 3 minutes
---

セッションページの上部で、ワークショップアプリへのパンくずリンクをクリックします。または、左側の「Digital Experience」メニュー項目にカーソルを合わせ、Real User Monitoringの `Overview` をクリックし、そのページでワークショップアプリの名前をクリックします。

{{% exercise title="重要なワークフローを見つける" %}}

RUM Metricを **User Experience**、**Front-end Health**、**Back-end Health**、**Custom Workflows**、**Pages**、**Network Requests**、**Map View** で分類したダッシュボードが表示されます。現在のMetricは過去のMetric（デフォルトでは1時間）と比較されます。

![RUM Dashboard](../images/rum-metric-map-charts.png)

各タブをクリックしてデータを確認します。

{{< tabs >}}
{{% tab title="質問" %}}

1. **Custom Workflows** タブのチャートを確認すると、`PlaceOrder` の **レイテンシー** を示すチャートはどれですか？
2. 地理的に、ユーザートラフィックはどこから来ていますか？

{{% /tab %}}
{{% tab title="回答" %}}

1. Custom Workflow Duration
2. US、UK、フランス、ドイツ（`Map View` タブを参照）

{{% /tab %}}
{{< /tabs >}}

**Custom Workflows** タブが表示されていることを確認してください。

* 問題のあるユーザーセッションを特定するために、**Custom Workflow Latency** チャートのレイテンシースパイクを使用します。
* **Custom Workflow Duration** チャートで、チャートタイトルの下にある **see all (1)** リンクをクリックします。

![RUM See All Custom Workflows](../images/rum-workflows-see-all.png)

{{% /exercise %}}
