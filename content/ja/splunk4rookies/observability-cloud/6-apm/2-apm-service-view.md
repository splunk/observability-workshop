---
title: 2. APM Service View
weight: 2
---
{{% notice title="Service View" style="info" %}}

サービスオーナーは、Splunk APM のサービスビューを使用することで、シングルペインオブグラスでサービスの健全性を網羅的に確認できます。サービスビューには、選択したサービスについて、可用性のサービスレベルインジケーター (SLI)、依存関係、リクエスト・エラー・期間 (RED) メトリクス、ランタイムメトリクス、インフラストラクチャメトリクス、Tag Spotlight、エンドポイント、およびログが含まれます。さらに、サービスビューからサービスのコードプロファイリングおよびメモリプロファイリングへ素早く遷移することもできます。

{{% /notice %}}

![Service Dashboard](../images/apm-service-dashboard.png)

{{% exercise title="Widen the timeframe and explore the dashboards" %}}

* **Time** ボックスを確認すると、ダッシュボードには先ほど選択した APM トレースが完了するまでの時間に関するデータのみが表示されていることがわかります (チャートが静的になっている点に注意してください)。
* **Time** ボックスで時間範囲を **-1h** に変更します。
* これらのチャートは、パフォーマンス問題を素早く特定するのに非常に役立ちます。このダッシュボードを使ってサービスの健全性を継続的に監視できます。
* ページをスクロールし、**Infrastructure Metrics** を展開します。ここでは Host および Pod のメトリクスを確認できます。
* Node.js で書かれたサービスではプロファイリングデータが利用できないため、**Runtime Metrics** は表示されません。
* それでは、explore ビューに戻りましょう。ブラウザの戻るボタンを押してください。

{{% /exercise %}}

![APM Explore](../images/apm-business-workflow.png)

{{% exercise title="Read the service map popup" %}}

{{< tabs >}}
{{% tab title="Question" %}}
**Service Map で **paymentservice** にカーソルを合わせてください。ポップアップのサービスチャートから何が読み取れますか?**
{{% /tab %}}
{{% tab title="Answer" %}}
**エラー率が非常に高いことがわかります。**
{{% /tab %}}
{{< /tabs >}}
{{% /exercise %}}

![APM Service Chart](../images/apm-service-popup-chart.png)

このエラー率にパターンがあるかどうかを把握する必要があります。そのために便利なツールが **Tag Spotlight** です。
