---
title: 5. APM トレースアナライザー
weight: 5
---

Splunk APMでは、**NoSample™** エンドツーエンドの可視性が提供され、すべてのサービスのトレースがキャプチャされます。このワークショップでは、**Order Confirmation ID** がタグとして利用可能です。これにより、ワークショップの前半で遭遇したユーザーエクスペリエンスの問題のトレースを正確に検索できます。

{{% notice title="トレースアナライザー" style="info" %}}

Splunk Observability Cloudは、アプリケーションモニタリングデータを探索するための複数のツールを提供しています。**トレースアナライザー** は、高基数で高精度な検索と、未知または新しい問題を調査するためのシナリオに適しています。
{{% /notice %}}

{{% notice title="演習" style="green" icon="running" %}}

* **paymentservice** の外側のボックスを選択した状態で、右側のペインで **Traces** をクリックします。
* **Trace Analyzer** を使用していることを確認するには、ボタン {{% button %}}Switch to Classic View{{% /button %}} が表示されていることを確認します。表示されていない場合は、{{% button style="blue" %}}Switch to Trace Analyzer{{% /button %}} をクリックします。

{{% /notice %}}

![APM トレースアナライザー](../images/apm-trace-analyzer.png)

{{% notice title="演習" style="green" icon="running" %}}

* タイムピッカーで **Last 1 hour** を選択します。
* 注意：ほとんどのトレースがエラー（赤）であり、エラーのない（青の）トレースは限られています。
* **Sample Ratio** が `1:1` に設定されていることを確認し、`1:10` ではないことを確認します。
* **Add filters** をクリックし、`orderId` を入力し、リストから **orderId** を選択します。
* ワークショップの前半でショッピングを行った際の **Order Confirmation ID** を貼り付けて enter キーを押します。持っていない場合は、インストラクターにお問い合わせください。
  ![Traces by Duration](../images/apm-trace-by-duration.png)

{{% /notice %}}

これで、非常に長いチェックアウト待ちでユーザーエクスペリエンスが悪かったトレースに絞り込みました。このトレースを表示することで、開発者は後でこの問題に戻ってきて、このトレースを確認できるようになります。

{{% notice title="演習" style="green" icon="running" %}}

* リスト内のトレースをクリックします。

{{% /notice %}}

次に、トレースのウォーターフォールを見ていきましょう。
