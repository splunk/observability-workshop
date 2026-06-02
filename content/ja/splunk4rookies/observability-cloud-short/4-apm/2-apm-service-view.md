---
title: 2. APM Service View
weight: 2
---
{{% notice title="Service View" style="info" %}}

サービスのオーナーは、Splunk APMのservice viewを使うことで、サービスのヘルス状態を単一の画面で完全に把握できます。service viewには、可用性のService-Level Indicator (SLI)、依存関係、Request, Error, Duration (RED) メトリクス、ランタイムメトリクス、インフラストラクチャメトリクス、Tag Spotlight、エンドポイント、選択したサービスのログが含まれます。また、service viewからコードプロファイリングやメモリプロファイリングへもすばやく移動できます。

{{% /notice %}}

{{% exercise title="エラーを表示するために時間範囲を広げる" %}}

* **Time** ボックスを確認すると、ダッシュボードには、先ほど選択したAPMトレースが完了するまでにかかった時間に関連するデータのみが表示されていることがわかります（チャートが静的になっている点に注意してください）。
* **Time** ボックスで時間範囲を **-1h** に変更します **(1)**。

![Service Dashboard](../images/apm-service-dashboard.png)

* **Success rate** が100%ではないことがはっきりとわかります。これは、サービスにエラーが発生しているためです。
* このエラー率にパターンがあるかどうかを把握する必要があります。そのための便利なツールがあります。**Tag Spotlight** タブをクリックしてください **(2)**。

{{% /exercise %}}
