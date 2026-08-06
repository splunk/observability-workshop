---
title: RUM アプリケーション概要
linkTitle: 2. App Overview
weight: 2
time: 3 minutes
---

セッションページの上部にあるパンくずリストのリンクをクリックして、ワークショップアプリに移動します。

{{% exercise title="重要なワークフローを見つける" %}}

* RUMメトリクスを **User Experience**、**Front-end Health**、**Back-end Health**、**Custom Workflows**、**Pages**、**Network Requests**、**Map View** ごとに分類したダッシュボードが表示されます。現在のメトリクスは過去のメトリクス（デフォルトでは1時間）と比較されます。

![RUM Dashboard](../images/rum-metric-map-charts.png)

* 各タブをクリックしてデータを確認します。

{{< tabs >}}
{{% tab title="質問" %}}

1. **Custom Workflows** タブのチャートを確認すると、`PlaceOrder` の **latency** を表示しているチャートはどれですか？
2. **Map View** タブで、最もリクエスト量が多いのはどの地域ですか？

{{% /tab %}}
{{% tab title="回答" %}}

1. **Custom Event Latency P75**
2. **US**

{{% /tab %}}
{{< /tabs >}}

* **Custom Workflows** タブが表示されていることを確認してください。
* 問題のあるユーザーセッションを特定するために、**Custom Event Latency** チャートのレイテンシースパイクを使用します。
* **Custom Workflow Latency** チャートのタイトルの下にある **see all** リンクをクリックします。

![RUM See All Custom Workflows](../images/rum-see-all.png)

{{% /exercise %}}
