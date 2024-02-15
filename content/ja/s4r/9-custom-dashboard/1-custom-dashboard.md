---
title: ダッシュボードの拡張
linkTitle: 1. ダッシュボードの拡張
weight: 1
---

すでに Log Observer の演習でダッシュボードに便利なログチャートを保存していますので、そのダッシュボードを拡張します。

 ![Wall mounted](../images/wall-mount.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* 2つのログチャートが含まれたダッシュボードに戻るために、メインメニューから **Dashboards** をクリックし、Team Dashboard ビューに移動します。**Dashboards** の下にある **Search dashboards** をクリックして、Service Health Dashboard グループを検索します。
* 名前をクリックすると、以前に保存したダッシュボードが表示されます。
  ![log list](../../7-log-observer/images/log-observer-custom-dashboard.png)
* ログ情報は有用ですが、チームがこれが何かを理解できるようにするには、もう少し情報が必要です。
* まず最初のステップとして、ダッシュボードに説明チャートを追加してみましょう。{{% button style="grey" %}}New text note{{% /button %}} をクリックし、ノートのテキストを次のテキストに置き換えます。その後 {{% button style="blue" %}}Save and close{{% /button %}} ボタンをクリックし、チャートに **Instructions** という名前を付けます。
{{% notice title=" Text note に使用する情報" style="grey" %}}

これは **Payment service** 用のカスタムヘルスダッシュボードです。  
ログに含まれるエラーに注意してください。  
詳細については、[リンク](https://https://www.splunk.com/en_us/products/observability.html)を参照してください。

{{% /notice %}}

* チャートの順序があまりよくないので、役立つように順序を入れ替えてみましょう。
* マウスを **Instructions** チャートの上端に移動させると、マウスポインタが **☩** に変わります。あなたはダッシュボード内でチャートをドラッグして移動することができます。**Instructions** チャートを左上の場所に移動させましょう。さらに、チャートの右端をドラッグしてページの 1/3 にサイズを変更しましょう。
* **Log Timeline view** チャートを **Instruction** チャートの横にドラッグして移動させ、ページの残りの 2/3 を埋めるようにサイズを変更します。
* 次に、**Log lines** チャートをページの幅にリサイズし、少なくとも2倍の長さにリサイズします。
* 以下のダッシュボードのようになったはずです。
  ![Initial Dashboard](../images/inital-dashboard.png)

{{% /notice %}}

見栄えが良くなりました。さらに続けて、役立ちそうなチャートを追加していきましょう。
