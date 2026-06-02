---
title: 2. APM Service View
weight: 2
---
{{% notice title="Service View" style="info" %}}

サービスオーナーとして、Splunk APMのservice viewを使うことで、サービスの健全性を1つの画面でまとめて確認できます。service viewには、可用性のservice-level indicator (SLI)、依存関係、request、error、duration (RED) メトリクス、runtimeメトリクス、infrastructureメトリクス、Tag Spotlight、エンドポイント、選択したサービスのログが含まれます。さらに、service viewからcode profilingやmemory profilingにすばやく移動することもできます。

{{% /notice %}}

{{% exercise title="エラーを表示するために期間を広げる" %}}

* **Time** ボックスを確認すると、ダッシュボードには先ほど選択したAPMトレースが完了するまでにかかった時間に対応するデータのみが表示されていることがわかります（チャートが静的になっている点に注意してください）。
* **Time** ボックスで期間を **-1h** に変更します **(1)**。

![Service Dashboard](../images/apm-service-dashboard.png)

* **Success rate** が100%になっていないことがはっきりとわかります。これはサービス内にエラーが発生しているためです。
* このエラー率にパターンがあるかどうかを把握する必要があります。そのための便利なツールがあるので、**Tag Spotlight** タブをクリックしましょう **(2)**。

{{% /exercise %}}
