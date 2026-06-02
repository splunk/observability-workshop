---
title: 2. Application View
weight: 2
---

{{% exercise title="Explore the RUM dashboard" %}}

* **UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Events**、**Network Requests**、**Pages**、および **Map View** ごとにメトリクスを分類したダッシュボードビューが表示され、過去のメトリクス（デフォルトでは 1 時間）と比較できます。

![RUM Dashboard](../images/rum-metric-map-charts.png)

* このページで利用可能なタブは次のとおりです。
  * **UX Metrics** Page Views、Page Load、および Web Vitals メトリクス
  * **Front-end Health** JavaScript エラーおよび Long Task の継続時間と件数の内訳
  * **Back-end Health** ネットワークエラー、リクエスト、および Time to First Byte
  * **Custom Events** カスタムイベントの RED メトリクス（Rate、Error、Duration）
  * **Network Requests** ネットワーク URL のグルーピングと主要メトリクス
  * **Pages** URL のグルーピング、主要メトリクス、および Web Vitals
  * **Map View** ロケーション別の地理的なリクエスト

* 各タブをクリックして、データを確認してください。

{{< tabs >}}
{{% tab title="Questions" %}}

1. **Custom Events** タブのチャートを確認したとき、レイテンシーのスパイクを明確に示しているチャートはどれですか？
2. **Map View** タブで、最も多くのリクエストが発生している地域はどこですか？

{{% /tab %}}
{{% tab title="Answers" %}}

1. **Custom Event Latency P75**
2. **Ireland**

{{% /tab %}}
{{< /tabs >}}

* **Custom Events** タブにいることを確認してください。
* 問題のあるユーザーセッションを特定するために、**Custom Event Latency P75** チャート内のレイテンシースパイクを利用します。
* **Custom Event Latency** チャート内で、チャートタイトルの下にある **see all** **(1)** リンクをクリックしてください。

![RUM See All](../images/rum-see-all.png)

{{% /exercise %}}
