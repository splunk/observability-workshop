---
title: 2. アプリケーションビュー
weight: 2
---

{{% exercise title="RUM ダッシュボードを探索する" %}}

* これで、**UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Events**、**Network Requests**、**Pages**、そして **Map View** ごとにメトリクスを分類し、過去のメトリクス（デフォルトでは 1 時間）と比較するダッシュボードビューが表示されます。

![RUM Dashboard](../images/rum-metric-map-charts.png)

* このページで利用できるタブは以下のとおりです:
  * **UX Metrics** ページビュー、ページロード、および Web Vitals メトリクス
  * **Front-end Health** JavaScript エラーと Long Task の時間およびカウントの内訳
  * **Back-end Health** ネットワークエラーとリクエスト、および Time to First Byte
  * **Custom Events** カスタムイベントの RED メトリクス（Rate、Error、Duration）
  * **Network Requests** ネットワーク URL のグループ化と主要メトリクス
  * **Pages** URL のグループ化と主要メトリクスおよび Web Vitals
  * **Map View** ロケーション別の地理的リクエスト

* 各タブをクリックして、データを確認してください。

{{< tabs >}}
{{% tab title="Questions" %}}

1. **Custom Events** タブのチャートを確認した場合、レイテンシースパイクを明確に示すチャートはどれですか？
2. **Map View** タブで、最も大きなリクエスト量はどこから発生していますか？

{{% /tab %}}
{{% tab title="Answers" %}}

1. **Custom Event Latency P75**
2. **Ireland**

{{% /tab %}}
{{< /tabs >}}

* **Custom Events** タブにいることを確認してください。
* 問題のあるユーザーセッションを特定するために、**Custom Event Latency P75** チャートのレイテンシースパイクを使用します。
* **Custom Event Latency** チャートで、チャートタイトルの下にある **see all** **(1)** リンクをクリックします。

![RUM See All](../images/rum-see-all.png)

{{% /exercise %}}
