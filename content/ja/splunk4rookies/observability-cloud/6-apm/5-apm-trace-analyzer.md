---
title: 5. APMトレースアナライザー
weight: 5
---

Splunk APMはすべてのサービスの**NoSample**（サンプリングなし）エンドツーエンドの可視性を提供するため、Splunk APMはすべてのトレースをキャプチャします。このワークショップでは、**Order Confirmation ID**がタグとして利用可能です。これは、ワークショップの前半で遭遇した不良なユーザー体験の正確なトレースを検索するためにこれを使用できることを意味します。

{{% notice title="トレースアナライザー" style="info" %}}

Splunk Observability Cloudは、アプリケーション監視データを探索するためのいくつかのツールを提供しています。**Trace Analyzer**は、未知または新しい問題を調査するための高カーディナリティ、高粒度の検索と探索が必要なシナリオに適しています。
{{% /notice %}}

{{% notice title="演習" style="green" icon="running" %}}

- **paymentservice**の外側のボックスを選択した状態で、右側のペインで**Trace**をクリックします。
- **Trace Analyzer**を使用していることを確認するため、{{% button %}}クSwitch to Classic View{{% /button %}}ボタンが表示されていることを確認します。表示されていない場合は、{{% button style="blue" %}}Switch to Trace Analyzer{{% /button %}}をクリックします。
- **時間範囲**を**過去 15 分**に設定します。
- **Sample Ratio**が `1:10` ではなく `1:1` に設定されていることを確認します。

{{% /notice %}}

![APMトレースアナライザー](../images/apm-trace-analyzer.png)

**Trace & Error count**ビューは、積み上げ棒グラフで合計トレース数とエラーのあるトレース数を表示します。マウスを使用して、利用可能な時間枠内の特定の期間を選択できます。

{{% notice title="演習" style="green" icon="running" %}}

- **Trace & Error count**と表示されているドロップダウンメニューをクリックし、**Trace Duration**に変更します

{{% /notice %}}

![APMトレースアナライザーヒートマップ](../images/apm-trace-analyzer-heat-map.png)

**Trace Duration**ビューは、期間ごとのトレースのヒートマップを表示します。ヒートマップは3次元のデータを表しています

- x軸の時間
- y軸のトレース期間
- ヒートマップの色合いで表される1秒あたりのトレース（またはリクエスト）数

マウスを使ってヒートマップ上の領域を選択し、特定の時間帯とトレース期間の範囲にフォーカスすることができます。

{{% notice title="演習" style="green" icon="running" %}}

- **Trace Duration**から**Trace & Error count**に戻します。
- 時間選択で**過去 1 時間**を選択します。
- ほとんどのトレースにエラー（赤）があり、エラーのないトレース（青）は限られていることに注意してください。
- **Sample Ratio**が `1:10` ではなく `1:1` に設定されていることを確認します。
- **Add filters**をクリックし、`orderId` と入力してリストから**orderId**を選択します。
- ワークショップの前半でショッピングを行った際の**Order Confirmation ID**を貼り付けてEnterキーを押します。もしIDを記録していない場合は、インストラクターに確認してください。
  ![期間別トレース](../images/apm-trace-by-duration.png)

{{% /notice %}}

これで、非常に長いチェックアウト待ちという不良なユーザーエクスペリエンスに遭遇した正確なトレースまでフィルタリングできました。

このトレースを表示することの二次的な利点は、トレースが最大13か月間アクセス可能であることです。これにより、開発者は後の段階でこの問題に戻り、このトレースを引き続き表示することができます。

{{% notice title="演習" style="green" icon="running" %}}

- リスト内のトレースをクリックします。

{{% /notice %}}

次に、トレースウォーターフォールを確認していきます。
