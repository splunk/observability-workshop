---
title: 1. RUM ダッシュボード
weight: 1
---

Splunk Observability Cloudのメインメニューから**RUM**をクリックします。RUMホームページに移動しますが、このビューは以前の短い導入で既に紹介されています。

![multiple apps](../images/multiple-apps.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* ワークショップを選択するために、次のようにドロップダウンが設定/選択されていることを確認してください：
  * **タイムフレーム**が **-15m** に設定されています。
  * 選択された **Environment** は **[NAME OF WORKSHOP]-workshop** です。
  * 選択された **App** は **[NAME OF WORKSHOP]-store** です。
  * **Source** は **All** に設定されています。
* 次に、**Page Views / JavaScript Errors** チャートの上にある **[NAME OF WORKSHOP]-store** をクリックします。
* これにより、新しいダッシュボードビューが表示され、メトリクスが **UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Events** に分解され、それらを過去のメトリクスと比較します（デフォルトでは1時間）。

{{% /notice %}}

![RUM Dashboard](../images/rum-dashboard.png)

* **UX Metrics:** ページビュー、ページ読み込み、Web Vitalsメトリクス。
* **Front-end Health:** JavascriptエラーおよびLong Taskの期間と回数の分解。
* **Back-end Health:** ネットワークエラーおよびリクエスト、Time to First Byte。
* **Custom Events:** カスタムイベントのREDメトリクス（Rate、Error＆Duration）。

{{% notice title="Exercise" style="green" icon="running" %}}

* 各タブ（**UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Events**）をクリックしてデータを調査してください。

{{< tabs >}}
{{% tab title="Question" %}}
**もし*Custom Events*タブのチャートを調査した場合、どのチャートが明確に**レイテンシースパイク**を示していますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
**それは*Custom Event Latency*チャートです。**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
