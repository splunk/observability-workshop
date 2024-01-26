---
title: 2. Synthetics Test Detail
weight: 2
---

現時点では、単一のSynthetic Browser Testの結果を見ています。このテストは**Business Transactions**に分割されています。これは、ビジネスクリティカルなユーザーフローを表す、1つまたは複数の論理的に関連するインタラクションのグループと考えてください。

{{% notice title="情報" style="info" %}}

以下のスクリーンショットにはエラーが含まれていませんが、テストランの結果でエラーが表示される場合があります。これは、テストランが失敗し、ワークショップに影響を与えない場合があるためです。

{{% /notice %}}

![waterfall](../images/synth-waterfall.png)

1. **Filmstrip:** サイトのパフォーマンスをスクリーンショットで確認できるため、ページのリアルタイムな応答を確認できます。
2. **Video:** 特定のテストランの場所とデバイスからサイトを読み込もうとするユーザーがどのような体験をするかを確認できます。
3. **Browser test metrics:** ウェブサイトのパフォーマンスの概要を提供するビュー。
4. **Synthetic transactions:** サイトとの対話を構成するSyntheticトランザクションのリスト
5. **Waterfall chart:** ウォーターフォールチャートは、テストランナーとテストされているサイトとの相互作用を視覚的に表現したものです。

デフォルトでは、Splunk Syntheticsはテストのスクリーンショットとビデオのキャプチャを提供します。これは問題のデバッグに役立ちます。たとえば、大きな画像の遅い読み込み、ページの遅い描画などが確認できます。

{{% notice title="実習" style="green" icon="running" %}}

* マウスを使用して、フィルムストリップを左右にスクロールして、テスト実行中のサイトの表示方法を確認します。
* ビデオペインでは、再生ボタン **▶** を押してテストの再生を確認できます。ellipsis **⋮** をクリックすると、再生速度を変更したり、**Picture in Picture** で表示したり、ビデオを **Download** したりできます。
* Synthetic Transactionペインで、ヘッダー*Business Transactions*の下の最初のボタン {{% button style="blue" %}}**Home**{{% /button %}} をクリックします。
* 以下のウォーターフォールでは、ページを構成するオブジェクトがすべて表示されます。最初の行はHTMLページそのものです。次の行はページを構成するオブジェクト（HTML、CSS、JavaScript、画像、フォントなど）です。
* ウォーターフォールで **GET** *splunk-otel-web.js* の行を見つけます。
* **>** ボタンをクリックして、メタデータセクションを開き、リクエスト/レスポンスヘッダー情報を確認します。
* Synthetic Transactionペインで、2番目のBusiness Transaction {{% button style="blue" %}}**Shop**{{% /button %}} をクリックします。フィルムストリップが調整され、新しいトランザクションの先頭に移動します。
* 他のトランザクションについても同様に繰り返し、最後に {{% button style="blue" %}}**PlaceOrder**{{% /button %}} トランザクションを選択します。

{{% /notice %}}
