---
title: 2. Synthetics Test Detail
weight: 2
---

{{% exercise title="テスト再生の確認" %}}

* ここでは、単一の Synthetic Browser Test の結果を確認しています。

![waterfall](../images/synth-waterfall.png)

* デフォルトで、Splunk Synthetics はテストのスクリーンショットとビデオキャプチャを提供します。これは問題のデバッグに役立ちます。たとえば、大きな画像の読み込みが遅い、ページのレンダリングが遅いといった状況を確認できます。

* マウスを使って filmstrip を左右にスクロールし、テスト実行中にサイトがどのようにレンダリングされていたかを確認します。
* Video ペインで再生ボタン **▶** **(1)** を押して、テストの再生を確認します。
* filmstrip の上にあるフィルターで、**Filter by a synthetic transaction, page, or step** **(2)** という見出しの下、**Synthetic transactions** にある **Place Order** をクリックします。

{{% /exercise %}}
