---
title: 2. Synthetics Test Detail
weight: 2
---

現在、ある1つの Synthetic Browser Test の結果を見ています。このテストは **Business Transactions** として分けられています。これは、1つまたは複数の論理的に関連する操作の集合であり、ビジネスクリティカルなユーザーフローを表すものと考えてください。

{{% notice title="Info" style="info" %}}

以下のスクリーンショットにはエラーが含まれていませんが、みなさんのテスト結果にはエラーが含まれている場合があります。テスト実行は時折失敗する場合があるため、これは想定通りの挙動であり、ワークショップにも影響ありません。

{{% /notice %}}

![waterfall](../images/synth-waterfall.png)

1. **Filmstrip:** サイトのパフォーマンスを一連のスクリーンショットで表示し、ページのリアルタイムな応答を確認できます。
2. **Video:** テスト実行元デバイスや地理的な場所からテスト対象のサイトを読み込むユーザーがどのような体験をするかを確認できます。
3. **Browser test metrics:** ウェブサイトのパフォーマンスの概要を確認することができます。
4. **Synthetic transactions:** ユーザーとサイト間での通信や操作からなる Synthetic トランザクションをリスト表示しています。
5. **Waterfall chart:** テスト実行元とテスト対象サイト間での通信や操作に関する一連の様子を視覚的に表現しています。

デフォルトでは、Splunk Syntheticsはテストのスクリーンショットとビデオのキャプチャを提供します。これは問題のデバッグに役立ちます。たとえば、大きな画像の遅い読み込み、ページの遅い描画などが確認できます。

{{% notice title="Exercise" style="green" icon="running" %}}

* マウスを使ってフィルムストリップを左右にスクロールし、テスト実行中、どのようにサイトが表示されていたかを確認します。
* ビデオペインでは、再生ボタン **▶** を押して録画を再生できます。再生画面右下の **⋮** をクリックすると、再生速度を変更したり、**Picture in Picture** で表示したり、ビデオを **Download** したりできます。
* Synthetic Transaction ペインで、*Business Transactions* のヘッダーの下に表示されている最初のボタン {{% button style="blue" %}}**Home**{{% /button %}} をクリックします。
* 以下のウォーターフォールでは、ページを構成するオブジェクトがすべて表示されます。最初の行は HTML ページそのものです。次の行はページを構成するオブジェクト（HTML、CSS、JavaScript、画像、フォントなど）です。
* ウォーターフォールで **GET** *splunk-otel-web.js* の行を見つけます。
* **>** ボタンをクリックして、メタデータセクションを開き、リクエスト/レスポンスヘッダー情報を確認します。
* Synthetic Transaction ペインで、2番目の Business Transaction {{% button style="blue" %}}**Shop**{{% /button %}} をクリックします。フィルムストリップが調整され、新しいトランザクションの先頭に移動します。
* 他のトランザクションについても同様に繰り返し、最後に {{% button style="blue" %}}**PlaceOrder**{{% /button %}} トランザクションを選択します。

{{% /notice %}}
