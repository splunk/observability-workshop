---
title: 1. RUM ダッシュボード
weight: 1
---

メインメニューで **Digital Experience** をクリックし、Real User Monitoring の下にある **Overview** をクリックします。RUM ホームページが表示されます。このビューは先ほどの簡単な紹介で既に説明しました。

![multiple apps](../images/rum-dashboard.png)

{{% exercise title="RUM をワークショップ用にフィルタリングする" %}}

* ドロップダウンが以下のように設定/選択されていることを確認して、ワークショップを選択します
  * **Time frame** が **-15m** に設定されていること。
  * **Environment** で **[NAME OF WORKSHOP]-workshop** が選択されていること。
  * **App** で **[NAME OF WORKSHOP]-store** が選択されていること。
  * **Source** が **All** に設定されていること。
* 次に、**Page Views / JavaScript Errors** チャートの上にある **[NAME OF WORKSHOP]-store** をクリックします。
* 新しいダッシュボードビューが表示され、メトリクスが **UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Workflows** ごとに分類され、過去のメトリクス（デフォルトでは1時間）と比較されます。

{{% /exercise %}}

![RUM Dashboard](../images/rum-metrics-dashboard.png)

* **UX Metrics:** Page Views、Page Load、Web Vitals メトリクス。
* **Front-end Health:** Javascript Errors と Long Task の期間およびカウントの内訳。
* **Back-end Health:** Network Errors、Requests、Time to First Byte。
* **Custom Workflows:** カスタムイベントの RED メトリクス（Rate、Error、Duration）。

{{% exercise title="RUM タブを探索する" %}}

* 各タブ（**UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Workflows**）をクリックして、データを確認します。

{{< tabs >}}
{{% tab title="Question" %}}
***Custom Workflows* タブのチャートを確認した場合、レイテンシーのスパイクを明確に示しているチャートはどれですか？**
{{% /tab %}}
{{% tab title="Answer" %}}
***Custom Workflow Duration* チャートです。**
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}
