---
title: 5. APM Trace Analyzer
weight: 5
---

Splunk APM はあらゆるサービスに対して **NoSample** のエンドツーエンドの可視性を提供しているため、すべてのトレースをキャプチャしています。本ワークショップでは、**Order Confirmation ID** がタグとして利用可能になっています。これを使うことで、ワークショップ前半で遭遇した、ユーザー体験が悪かった際のまさにそのトレースを検索できます。

{{% notice title="Trace Analyzer" style="info" %}}

Splunk Observability Cloud には、アプリケーション監視データを探索するためのツールがいくつか用意されています。**Trace Analyzer** は、未知の問題や新たな問題を調査するために、高カーディナリティ・高粒度の検索や探索を行うシナリオに適しています。
{{% /notice %}}

{{% exercise title="Open the Trace Analyzer" %}}

* **paymentservice** の外側のボックスを選択した状態で、右側のペインの **Traces** をクリックします。
* **Time Range** を **Last 15 minutes** に設定します。
* **Sample Ratio** が `1:10` ではなく `1:1` に設定されていることを確認します。

{{% /exercise %}}

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

**Trace & error count** ビューでは、トレースの総数とエラーを含むトレースが積み上げ棒グラフで表示されます。マウスを使って、利用可能な時間範囲内の特定の期間を選択できます。

{{% exercise title="Switch to trace-duration view" %}}

* **Trace & error count** と表示されているドロップダウンメニューをクリックし、**Trace duration** に変更します。

{{% /exercise %}}

![APM Trace Analyzer Heat Map](../images/apm-trace-analyzer-heat-map.png)

**Trace Duration** ビューは、所要時間別のトレースをヒートマップで表示します。このヒートマップは、3 つのデータ次元を表しています。

* x 軸の時間
* y 軸のトレース所要時間
* ヒートマップの濃淡で表される、1 秒あたりのトレース数 (リクエスト数)

マウスでヒートマップ上のエリアを選択することで、特定の時間帯およびトレース所要時間の範囲に焦点を当てることができます。

{{% exercise title="Compare error traces over an hour" %}}

* **Trace duration** から **Trace & Error count** に切り替えます。
* タイムピッカーで **Last 1 hour** を選択します。
* ほとんどのトレースにエラー (赤) が含まれており、エラーのないトレース (青) はわずかしかないことを確認します。
* **Sample Ratio** が `1:10` ではなく `1:1` に設定されていることを確認します。
* **Add filters** をクリックし、`orderId` と入力してリストから **orderId** を選択します。
* ワークショップ前半でショッピングを行った際の **Order Confirmation ID** を貼り付けて Enter キーを押します。Order Confirmation ID を控えていなかった場合は、講師に確認してください。
  ![Traces by Duration](../images/apm-trace-by-duration.png)

{{% /exercise %}}

これで、チェックアウトの待ち時間が非常に長く、ユーザー体験が悪かったまさにそのトレースに絞り込むことができました。

このトレースを参照できることのもう 1 つのメリットは、トレースが最大 13 か月間アクセス可能であるという点です。これにより、開発者は後日この問題に立ち戻り、たとえばこのトレースを引き続き参照することができます。

{{% exercise title="Open a failing trace" %}}

* リスト内のトレースをクリックします。

{{% /exercise %}}

次に、トレースのウォーターフォールを見ていきます。
