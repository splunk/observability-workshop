---
title: 2. Application View
weight: 2
---

{{% exercise title="RUMダッシュボードを探索する" %}}

* **UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Workflows**、**Network Requests**、**Pages**、**Map View** ごとにメトリクスを分類したダッシュボードビューが表示され、過去のメトリクス（デフォルトでは1時間）と比較できます。

![RUM Dashboard](../images/rum-metric-map-charts.png)

* このページで利用可能なタブは以下の通りです
  * **UX Metrics** ページビュー、ページロード、Web Vitalsメトリクス
  * **Front-end Health** JavaScriptエラーとLong Taskの期間およびカウントの内訳
  * **Back-end Health** ネットワークエラー、リクエスト、Time to First Byte
  * **Custom Workflows** カスタムワークフローのREDメトリクス（Rate、Error、Duration）
  * **Network Requests** ネットワークURLのグループ化と主要メトリクス
  * **Pages** URLのグループ化と主要メトリクスおよびWeb Vitals
  * **Map View** 地理的なロケーション別リクエスト

* 各タブをクリックしてデータを確認します。

{{< tabs >}}
{{% tab title="質問" %}}

1. **Custom Workflows** タブのチャートを確認すると、レイテンシスパイクが明確に表示されているチャートはどれですか？
2. **Map View** タブで、最もリクエスト量が多いのはどこですか？

{{% /tab %}}
{{% tab title="回答" %}}

1. **Custom Workflow Duration P75**
2. **Ireland**

{{% /tab %}}
{{< /tabs >}}

* **Custom Workflows** タブが表示されていることを確認してください。
* 問題のあるユーザーセッションを特定するために、**Custom Workflow Duration P75** チャートのレイテンシスパイクを使用します。
* **Custom Workflows Duration** チャートのタイトル下にある **see all** **(1)** リンクをクリックします。

![RUM See All](../images/rum-see-all.png)

{{% /exercise %}}
