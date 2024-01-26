---
title: ダッシュボードの拡張
linkTitle: 1. ダッシュボードの拡張
weight: 1
---

すでにログオブザーバーの演習でダッシュボードに便利なログチャートを保存していますので、それを拡張します。

 ![Wall mounted](../images/wall-mount.png)

{{% notice title="練習" style="green" icon="running" %}}

* 2 つのログチャートが含まれたダッシュボードに戻るには、メインメニューから **Dashboards** をクリックし、Team Dashboard ビューに移動します。**Dashboards** の下にある **Search dashboards** をクリックして、Service Health Dashboard グループを検索します。名前をクリックすると、以前に保存したダッシュボードが表示されます。
  ![log list](../../7-log-observer/images/log-observer-custom-dashboard.png)
* ログ情報が有用であっても、チームにとってそれが理解できるようにするには、もう少し情報が必要です。チャートに説明チャートを追加する最初のステップは、{{% button style="grey" %}}New text note{{% /button %}} をクリックし、ノートのテキストを次のテキストに置き換え、その後 {{% button style="blue" %}}Save and close{{% /button %}} ボタンをクリックしてチャートに名前を付けることです。名前は **Instructions**
{{% notice title=" Text note に使用する情報" style="grey" %}}

これは**Payment service**のためのカスタムヘルスダッシュボードです。ログのエラーに注意してください。
詳細については、[リンク](https://https://www.splunk.com/en_us/products/observability.html)を参照してください。

{{% /notice %}}

* チャートの順序がよくないので、それを修正して、それが役立つようにします。
* マウスを **Instructions** チャートの上端に移動させると、マウスポインタが **☩** に変わります。これにより、ダッシュボードでチャートをドラッグできます。**Instructions** チャートを左上の場所にドラッグし、右端をドラッグしてページの 1/3 にサイズを変更します。
* **Log Timeline view** チャートを **Instruction** チャートの横にドラッグして追加し、ページの残りの 2/3 を埋めるようにサイズを変更します。次に、エラーレートチャートを追加して、チャートをページ全体にサイズ変更します。
* 次に、**Log lines** チャートをページの幅にリサイズし、少なくとも 2 倍の長さにリサイズします。
* 次のダッシュボードのようになるはずです:
  ![Initial Dashboard](../images/inital-dashboard.png)

{{% /notice %}}

これは素晴らしい見た目です。続行して意味のあるチャートを追加しましょう。
