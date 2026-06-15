---
title: 5. APM Trace Analyzer
weight: 5
---

Splunk APM はすべてのサービスに対して **NoSample** のエンドツーエンドの可視性を提供するため、すべてのトレースをキャプチャします。このワークショップでは、**Order Confirmation ID** がタグとして利用可能です。これにより、ワークショップの前半で体験した悪いユーザーエクスペリエンスの正確なトレースを検索できます。

{{% notice title="Trace Analyzer" style="info" %}}

Splunk Observability Cloud は、アプリケーション監視データを調査するためのいくつかのツールを提供しています。**Trace Analyzer** は、高カーディナリティで高粒度の検索や調査を行い、未知の問題や新しい問題を調べるシナリオに適しています。
{{% /notice %}}

{{% exercise title="Trace Analyzer を開く" %}}

* **paymentservice** の外側のボックスが選択された状態で、右側のペインで **Traces** をクリックします。
* **Time Range** を **Last 15 minutes** に設定します。
* **Sample Ratio** が `1:1` に設定されていることを確認してください（`1:10` では**ありません**）。

{{% /exercise %}}

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

**Trace & error count** ビューは、トレースの合計とエラーのあるトレースを積み上げ棒グラフで表示します。マウスを使用して、利用可能な時間枠内の特定の期間を選択できます。

{{% exercise title="トレース時間ビューに切り替える" %}}

* **Trace & error count** と表示されているドロップダウンメニューをクリックし、**Trace duration** に変更します。

{{% /exercise %}}

![APM Trace Analyzer Heat Map](../images/apm-trace-analyzer-heat-map.png)

**Trace Duration** ビューは、トレースの所要時間をヒートマップで表示します。ヒートマップは3次元のデータを表現しています

* X軸に時間
* Y軸にトレースの所要時間
* ヒートマップの濃淡で1秒あたりのトレース（リクエスト）数を表現

マウスを使用してヒートマップ上の領域を選択し、特定の時間帯とトレース所要時間の範囲に絞り込むことができます。

{{% exercise title="1時間のエラートレースを比較する" %}}

* **Trace duration** から **Trace & Error count** に戻します。
* タイムピッカーで **Last 1 hour** を選択します。
* トレースのほとんどにエラーがあり（赤）、エラーのないトレース（青）は限られていることに注目してください。
* **Sample Ratio** が `1:1` に設定されていることを確認してください（`1:10` では**ありません**）。
* **Add filters** をクリックし、`orderId` と入力して、リストから **orderId** を選択します。
* ワークショップの前半で買い物をした際の **Order Confirmation ID** を貼り付けて Enter キーを押します。メモしていない場合は、インストラクターにお尋ねください。
  ![Traces by Duration](../images/apm-trace-by-duration.png)

{{% /exercise %}}

これで、チェックアウト時に非常に長い待ち時間が発生した悪いユーザーエクスペリエンスの正確なトレースに絞り込むことができました。

このトレースを表示するもう一つの利点は、トレースが最大13か月間アクセス可能であることです。これにより、開発者は後日この問題に戻ってきても、このトレースを確認することができます。

{{% exercise title="失敗したトレースを開く" %}}

* リスト内のトレースをクリックします。

{{% /exercise %}}

次に、トレースのウォーターフォールを確認していきます。
