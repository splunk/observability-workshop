---
title: 1. RUM ダッシュボード
weight: 1
---

メインメニューで **Digital Experience** をクリックし、Real User Monitoring の下にある **Overview** をクリックします。RUM のホームページが表示されますが、このビューについては前のセクションの簡単な紹介で既に説明しています。

![multiple apps](../images/rum-dashboard.png)

{{% exercise title="ワークショップに RUM をフィルタリングする" %}}

* ドロップダウンが以下のように設定/選択されていることを確認して、ご自身のワークショップを選択してください:
  * **Time frame** が **-15m** に設定されています。
  * 選択されている **Environment** が **[NAME OF WORKSHOP]-workshop** です。
  * 選択されている **App** が **[NAME OF WORKSHOP]-store** です。
  * **Source** が **All** に設定されています。
* 次に、**Page Views / JavaScript Errors** チャートの上にある **[NAME OF WORKSHOP]-store** をクリックします。
* これにより、メトリクスを **UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Workflows** に分類し、過去のメトリクス（デフォルトでは 1 時間）と比較する新しいダッシュボードビューが表示されます。

{{% /exercise %}}

![RUM Dashboard](../images/rum-metrics-dashboard.png)

* **UX Metrics:** Page Views、Page Load、および Web Vitals メトリクス。
* **Front-end Health:** JavaScript エラーと Long Task の duration および count の内訳。
* **Back-end Health:** Network Errors と Requests、Time to First Byte。
* **Custom Workflows:** カスタムイベントの RED メトリクス（Rate、Error、Duration）。

{{% exercise title="RUM タブを探索する" %}}

* 各タブ（**UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Workflows**）をクリックして、データを確認してください。

{{< tabs >}}
{{% tab title="Question" %}}
***Custom Workflows* タブのチャートを確認すると、レイテンシのスパイクを明確に示しているのはどのチャートですか?**
{{% /tab %}}
{{% tab title="Answer" %}}
***Custom Workflow Duration* チャートです**
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}
