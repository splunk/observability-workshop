---
title: 1. RUM ダッシュボード
weight: 1
---

Splunk Observability Cloud のメインメニューから **RUM** をクリックします。RUM ホームページに移動しますが、このビューは以前の短い紹介で既に見たことがあるでしょう。

![multiple apps](../images/multiple-apps.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* あなたのワークショップ環境が選択されていることを確かめるために、次のようにドロップダウンが設定/選択されていることを確認してください：
  * **タイムフレーム**が **-15m** に設定されています。
  * 選択された **Environment** は **[NAME OF WORKSHOP]-workshop** です。
  * 選択された **App** は **[NAME OF WORKSHOP]-store** です。
  * **Source** は **All** に設定されています。
* 次に、**Page Views / JavaScript Errors** チャートの上にある **[NAME OF WORKSHOP]-store** をクリックします。
* これにより、新しいダッシュボードビューが表示され、メトリクスが **UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Events** に分解され、それらを過去のメトリクスと比較します（デフォルトでは1時間）。

{{% /notice %}}

![RUM Dashboard](../images/rum-dashboard.png)

* **UX Metrics:** ページビュー、ページ読み込み、Web Vitals メトリクス。
* **Front-end Health:** Javascript エラーおよび Long Task の期間と回数の分解。
* **Back-end Health:** ネットワークエラーおよびリクエスト、Time to First Byte。
* **Custom Events:** カスタムイベントの RED メトリクス（Rate、Error＆Duration）。

{{% notice title="Exercise" style="green" icon="running" %}}

* 各タブ（**UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Events**）をクリックしてデータを調査してください。

{{< tabs >}}
{{% tab title="Question" %}}
**もし *Custom Events* タブのチャートを調査した場合、どのチャートが*処理時間の急激な増加*を明確に示していますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
**それは *Custom Event Latency* チャートです。**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
