---
title: ダッシュボードの拡張
linkTitle: 1. ダッシュボードの拡張
weight: 1
---

Log Observer の演習でいくつかの便利なログチャートをダッシュボードに保存済みなので、そのダッシュボードを拡張していきます。

 ![Wall mounted](../images/wall-mount.png)

{{% exercise title="カスタムダッシュボードを開く" %}}

* 2 つのログチャートを含むダッシュボードに戻るには、メインメニューから **Dashboards** をクリックしてください。Team Dashboard ビューが表示されます。**Dashboards** の下にある **Search dashboards** をクリックして、Service Health Dashboard グループを検索します。
* 名前をクリックすると、以前に保存したダッシュボードが表示されます。
  ![log list](../../7-log-observer/images/log-observer-custom-dashboard.png)
* ログ情報そのものは有用ですが、チームにとって意味のあるものにするにはさらに情報が必要です。情報を追加していきましょう。
* 最初のステップとして、説明用のチャートをダッシュボードに追加します。{{% button style="grey" %}}New text note{{% /button %}} をクリックし、ノート内のテキストを以下の内容に置き換えてください。その後 {{% button style="blue" %}}Save and close{{% /button %}} ボタンをクリックし、チャート名を **Instructions** にします。
{{% notice title=" テキストノートに使用する情報" style="grey" %}}

```text

This is a Custom Health Dashboard for the **Payment service**,  
Please pay attention to any errors in the logs.
For more detail visit [link](https://https://www.splunk.com/en_us/products/observability.html)

```

{{% /notice %}}

* チャートの並びがきれいではないので、これを修正して有用な配置に並べ替えましょう。
* **Instructions** チャートの上端にマウスを移動すると、マウスポインターが **☩** に変わります。これによりダッシュボード内でチャートをドラッグできます。**Instructions** チャートを左上にドラッグし、右端をドラッグしてページの 1/3 の幅にリサイズしてください。
* **Log Timeline view** チャートを **Instruction** チャートの隣にドラッグして配置し、ページの残り 2/3 を埋めるようにリサイズします。
* 次に、**Log lines** チャートをページ幅いっぱいにリサイズし、少なくとも 2 倍の長さになるよう縦にもリサイズしてください。
* 以下のようなダッシュボードに近い見た目になるはずです:
  ![Initial Dashboard](../images/initial-dashboard.png)

{{% /exercise %}}

良い感じです。引き続きより意味のあるチャートを追加していきましょう。
