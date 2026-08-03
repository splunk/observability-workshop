---
title: 2. アプリケーションビュー
weight: 2
---

{{% exercise title="RUM ダッシュボードを確認する" %}}

* **UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Workflows**、**Network Requests**、**Pages**、**Map View** ごとにメトリクスを分類したダッシュボードビューが表示されます。これらは過去のメトリクス（デフォルトでは1日）と比較されます。

![RUM Dashboard](../images/rum-metric-map-charts.png)

* このページで利用可能なタブは以下のとおりです:
  * **UX Metrics** ページビュー、ページロード、Web Vitalsメトリクス
  * **Front-end Health** JavaScriptエラーとLong Taskの期間とカウントの内訳
  * **Back-end Health** ネットワークエラー、リクエスト、Time to First Byte
  * **Custom Workflows** カスタムワークフローのREDメトリクス（Rate、Error、Duration）
  * **Network Requests** ネットワークURLのグルーピングと主要メトリクス
  * **Pages** URLのグルーピングと主要メトリクス、Web Vitals
  * **Map View** 地域別のリクエスト分布

* 各タブをクリックしてデータを確認します。

{{< tabs >}}
{{% tab title="質問" %}}

1. **Custom Workflows** タブのチャートを確認した場合、レイテンシースパイクが明確に表示されるチャートはどれですか？
2. **Map View** タブで、最もリクエスト量が多い地域はどこですか？

{{% /tab %}}
{{% tab title="回答" %}}

1. **Custom Workflow Duration P75**
2. **Ireland**

{{% /tab %}}
{{< /tabs >}}

* **Custom Workflows** タブ **(1)** が選択されていることを確認します。
* 問題のあるユーザーセッションを特定するために、**Custom Workflow Duration P75** チャートのレイテンシースパイクを使用します。
* **Custom Workflows Duration** チャートのタイトル下にある **see all** **(2)** リンクをクリックします。

![RUM See All](../images/rum-see-all.png)

{{% /exercise %}}
