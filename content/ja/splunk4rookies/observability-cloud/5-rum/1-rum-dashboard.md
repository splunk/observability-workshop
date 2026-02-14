---
title: 1. RUMダッシュボード
weight: 1
---

Splunk Observability Cloudのメインメニューから、**RUM**をクリックします。RUMホームページに到着します。このビューについては、先ほどの短い紹介ですでに説明しました。

![複数のアプリ](../images/rum-dashboard.png)

{{% notice title="演習" style="green" icon="running" %}}

- ドロップダウンが以下のように設定/選択されていることを確認して、ワークショップを選択してください
  - **時間枠**は **-15m** に設定されていること。
  - 選択されている**Environment**は **[ワークショップ名]-workshop** であること。
  - 選択されている**App**は **[ワークショップ名]-store** であること。
  - **Source**は**All**に設定されていること。
- 次に、**Page Views / JavaScript Errors**チャートの上にある **[ワークショップ名]-store** をクリックします。
- これにより、**UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Events**ごとにメトリクスを分類し、過去のメトリクス（デフォルトでは1時間）と比較する新しいダッシュボードビューが表示されます。

{{% /notice %}}

![RUMダッシュボード](../images/rum-metrics-dashboard.png)

- **UX Metrics:** ページビュー、ページロード、Webバイタルメトリクス。
- **Front-end Health:** JavaScriptエラーとロングタスクの期間と数の内訳。
- **Back-end Health:** ネットワークエラー、リクエスト、最初のバイトまでの時間。
- **Custom Events:** Custom EventsのREDメトリクス（レート、エラー、期間）。

{{% notice title="演習" style="green" icon="running" %}}

- 各タブ（**UX Metrics**、**Front-end Health**、**Back-end Health**、**Custom Events**）をクリックしてデータを調べます。

{{< tabs >}}
{{% tab title="質問" %}}
「Custom Events」タブのチャートを調べると、**どのチャート**が**レイテンシースパイクを**明確に示していますか？
{{% /tab %}}
{{% tab title="回答" %}}
それは **「Custom Event Latency」** チャートです
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
