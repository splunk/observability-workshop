---
title: 5. APM Trace Analyzer
weight: 5
---

**Trace Analyzer** に到達しました。

**Trace Analyzer** は、分散トレースを大規模に探索・分析するために設計された Splunk APM の強力なツールです。Splunk APM はすべてのトレースをフルフィデリティ (NoSample) でキャプチャするため、サービスを流れるすべてのトランザクションを完全に可視化できます。

Trace Analyzer では次のことが可能です。

* **ハイカーディナリティタグでの検索**: 顧客 ID、注文 ID、カスタムビジネス属性など、インデックス化された任意の span タグでトレースをフィルタリングできます。
* **トレースパターンの可視化**: トレース数とエラー数の時系列を表示して、傾向や異常を特定できます。
* **レイテンシ分布の分析**: heatmap ビューを使用して、トレース時間のパターンを把握し、外れ値を発見できます。
* **特定のトレースへのドリルダウン**: 顧客の苦情を調査する場合でも、特定のトランザクションをデバッグする場合でも、必要なトレースを素早く見つけられます。

これにより、Trace Analyzer は、未知の問題の調査、特定のトランザクションの調査、干し草の山から針を見つけるような根本原因分析を行うのに最適なツールとなります。

{{% exercise title="失敗した checkout トレースを見つける" %}}

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

* 次の条件のトレースを見つけてください:
  * **checkoutservice** と **paymentservice** にエラーがある **(1)**
  * **Initiating Operation** が `frontend: POST /cart/checkout` である
  * 続けるには、青色の **Trace ID** **(2)** を選択してください
* これにより、そのトレースの **Trace Waterfall** が開きます。

{{% /exercise %}}
