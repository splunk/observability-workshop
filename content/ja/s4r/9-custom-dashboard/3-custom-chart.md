---
title: カスタムチャートの追加
linkTitle: 3. カスタムチャートの追加
weight: 3
---

ワークショップのこのセクションでは、ダッシュボードに追加するチャートを作成し、以前に構築した Detector と紐づけします。これにより、テスト時の振る舞いを確認し、テストによって SLA 違反が発生した場合にアラートを受け取ることができます。

{{% notice title="Exercise" style="green" icon="running" %}}

* ダッシュボードの上部で **+** をクリックし、**Chart** を選択します。
  ![new chart screen](../images/new-chart.png)
* まず、{{% button style="grey" %}}Untitled chart{{% /button %}} の入力フィールドを使用して、チャートの名前を **Overall Test Duration** にします。
* このエクササイズでは、棒グラフまたはカラムグラフを使いたいので、チャートオプションの3番目のアイコン {{% icon icon="chart-bar" %}} をクリックします。
* **Plot editor** で、**Signal** の入力欄に `synthetics.run.duration.time.ms`（これはテストの実行の所要時間を表します）を入力し Enter キーを押します。
* 現時点では、異なる色の棒が表示されます。これはテスト実行元の地域ごとに色分けされたものです。ですが、これは不要なので、いくつかの解析ルールを追加してこの表示を変更できます。
* では {{% button style="blue" %}}Add analytics{{% /button %}} ボタンをクリックします。
* ドロップダウンから **Mean** オプションを選択し、`mean:aggregation` を選択してダイアログの外側をクリックします。メトリクスが統合され、チャートが単一の色に変わることに着目してください。
* x 軸は現在、時間を表していません。これを変更するには、プロットラインの末尾にある設定 {{% icon icon="cog" %}} アイコンをクリックします。次のダイアログが表示されるはずです。
  ![signal setup](../images/signal-setup.png)
* **Display units**（**2**）を **None** から **Time (autoscaling)/Milliseconds(ms)** に変更します。ドロップダウンが **Millisecond** に変わり、チャートの x 軸がテストの実行時間を表すようになります。
* 設定 {{% icon icon="cog" %}} アイコンまたは{{% button style="gray" %}}close{{% /button %}}ボタンをクリックし、ダイアログを閉じます。
* Detector を追加するには、{{% button style="blue" %}}Link Detector{{% /button %}} ボタンをクリックして、以前に作成した Detector の名前を入力します。
* Detector の名前をクリックして選択します。
* チャートの周りにカラーの枠が表示されることに着目しましょう。これは、アラートの状態を示しています。ダッシュボードの上部にあるベルアイコンについても同様です。以下の画像のように見えるはずです。
  ![detector added](../images/detector-added.png)
* 完了したら、{{% button style="blue" %}}Save and close{{% /button %}} ボタンをクリックします。
* ダッシュボードで、チャートを以下のスクリーンショットのように移動させます。
  ![Service Health Dashboard](../images/service-health-dashboard.png)
* 最後に、ページの上部の三点リーダー **...**（**Event Overlay** の横）をクリックし、**View fullscreen** をクリックします。これで壁に取り付けられたTVモニターで表示するのにも利用できます（戻るにはEscキーを押します）。

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

時間がある場合には、RUM メトリクスを使用してダッシュボードに別のカスタムチャートを追加してみてください。事前に用意・提供されている **RUM applications** ダッシュボードグループからチャートをコピーするか、`rum.client_error.count` を使用してアプリケーションのクライアントエラーの数を表示するチャートを作成できます。

{{% /notice %}}

最後に、ワークショップの締めくくりを行います。
