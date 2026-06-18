---
title: 5. APM Trace Analyzer
weight: 5
---

Splunk APM はすべてのサービスに対して **NoSample** のエンドツーエンドの可視性を提供するため、Splunk APM はすべてのトレースをキャプチャします。このワークショップでは、送金の **orderId** がタグとして利用可能です。これにより、ユーザーが経験した悪いユーザー体験の正確なトレースを検索することができます。

{{% notice title="Trace Analyzer" style="info" %}}

Splunk Observability Cloud は、アプリケーション監視データを探索するためのいくつかのツールを提供しています。**Trace Analyzer** は、高カーディナリティかつ高粒度の検索や探索を行い、未知の問題や新しい問題を調査するシナリオに適しています。
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* **wire-transfer-service** の外枠が選択された状態で、右側のペインで **Traces** をクリックします。
* **Time Range** を **Last 15 minutes** に設定します。
* **Sample Ratio** が `1:10` では**なく** `1:1` に設定されていることを確認します。

{{% /notice %}}

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

**Trace & error count** ビューは、トレースの合計とエラーのあるトレースを積み上げ棒グラフで表示します。マウスを使用して、利用可能な時間枠内の特定の期間を選択できます。

{{% notice title="Exercise" style="green" icon="running" %}}

* **Trace & error count** と表示されているドロップダウンメニューをクリックし、**Trace duration** に変更します。

{{% /notice %}}

![APM Trace Analyzer Heat Map](../images/apm-trace-analyzer-heat-map.png)

**Trace Duration** ビューは、トレースの期間別ヒートマップを表示します。ヒートマップは3次元のデータを表現しています

* X軸に時間
* Y軸にトレースの期間
* ヒートマップの色の濃淡で1秒あたりのトレース（またはリクエスト）数を表現

ヒートマップ上でマウスを使用して領域を選択し、特定の時間帯とトレース期間の範囲にフォーカスすることができます。

{{% notice title="Exercise" style="green" icon="running" %}}

* **Trace duration** から **Trace & Error count** に戻します。
* タイムピッカーで **Last 1 hour** を選択します。
* トレースのほとんどにエラーがあり（赤）、エラーのないトレース（青）は限られていることに注目してください。
* **Sample Ratio** が `1:10` では**なく** `1:1` に設定されていることを確認します。
* **Add filters** をクリックし、`orderId` と入力してリストから **orderId** を選択します。
* ワークショップリーダーから提供された **orderId** を見つけて選択し、Enter を押します。
  ![Traces by Duration](../images/apm-trace-by-id.png)

{{% /notice %}}

これで、ユーザーが非常に長い処理待ちによる悪い体験を報告した正確なトレースにフィルタリングできました。

このトレースを表示することの副次的なメリットは、トレースが最大13か月間アクセス可能であることです。これにより、開発者は後の段階でこの問題に戻ってきても、このトレースを確認することができます。

{{% notice title="Exercise" style="green" icon="running" %}}

* リスト内のトレースをクリックします。

{{% /notice %}}

次に、トレースウォーターフォールを確認していきます。
