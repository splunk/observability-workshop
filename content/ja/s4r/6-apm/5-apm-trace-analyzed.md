---
title: 5. APM Trace Analyzer
weight: 5
---

Splunk APM では、**NoSample** の End to End の可視性が提供され、すべてのサービスのトレースがキャプチャされます。このワークショップでは、**Order Confirmation ID** がタグとして利用可能です。これにより、ワークショップの前半で遭遇したユーザーエクスペリエンスの問題のトレースを正確に検索できます。

{{% notice title="Trace Analyzer" style="info" %}}

Splunk Observability Cloud は、アプリケーションモニタリングデータを探索するための複数のツールを提供しています。**Trace Analyzer** は、未知の問題や新しい問題を調査するために高カーディナリティで粒度の細かなデータを検索・探索するシナリオに適しています。
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* **paymentservice** の外側のボックスを選択した状態で、右側のペインで **Traces** をクリックします。
* **Trace Analyzer** を使用していることを確認するために、{{% button %}}Switch to Classic View{{% /button %}} が表示されていることを確認します。表示されていない場合は、{{% button style="blue" %}}Switch to Trace Analyzer{{% /button %}} をクリックします。

{{% /notice %}}

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* 表示する時間枠として **Last 1 hour** を選択します。
* ほとんどのトレースがエラー（赤）であり、エラーのない（青の）トレースは限られています。
* **Sample Ratio** が `1:10` ではなく `1:1` に設定されていることを確認します。
* **Add filters** をクリックし、`orderId` を入力し、リストから **orderId** を選択します。
* ワークショップの前半でショッピングを行った際の **Order Confirmation ID** を貼り付けて Enter キーを押します。入力する ID が分からない場合は、インストラクターにお問い合わせください。
  ![Traces by Duration](../images/apm-trace-by-duration.png)

{{% /notice %}}

これで、あなたが体験した、チェックアウト処理で長時間待たされユーザーエクスペリエンスを損ねていた処理のトレースを絞り込むことができました。このトレースは最大13ヶ月間アクセスすることができます。そのため、例えば、開発者は後日この問題に再び取り組む際にも、このトレースを確認できるでしょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* リスト内のトレースをクリックします。

{{% /notice %}}

次に、トレースのウォーターフォールを見ていきましょう。
