---
title: カスタムチャートの追加
linkTitle: 2. カスタムチャートの追加
weight: 3
---

ワークショップのこのパートでは、ダッシュボードに追加するチャートを作成し、以前作成したディテクターにリンクします。これにより、テストの動作を確認し、1つ以上のテスト実行がSLAに違反した場合にアラートを受け取ることができます。

{{% notice title="Exercise" style="green" icon="running" %}}

* ダッシュボードの上部で **+** をクリックし、**Chart** を選択します。
  ![new chart screen](../images/new-chart.png)
* まず、{{% button style="grey" %}}Untitled chart{{% /button %}} 入力フィールドを使用して、チャートに **Overall Test Duration** という名前を付けます。
* この演習では棒グラフまたは縦棒グラフを使用するため、チャートオプションボックスの3番目のアイコン {{% icon icon="chart-bar" %}} をクリックします。
* **Plot editor** で、**Signal** ボックスに `synthetics.run.duration.time.ms`（テストの実行時間）を入力して Enter キーを押します。
* 現在、異なる色のバーが表示されており、テストが実行される各リージョンごとに異なる色になっています。これは必要ないため、分析を追加してこの動作を変更できます。
* {{% button style="blue" %}}Add analytics{{% /button %}} ボタンをクリックします。
* ドロップダウンから **Mean** オプションを選択し、`mean:aggregation` を選んでダイアログボックスの外側をクリックします。メトリクスが集約されるため、チャートが単一の色に変わることに注目してください。
* 現在、x軸は時間を表していません。これを変更するには、プロットラインの末尾にある設定 {{% icon icon="cog" %}} アイコンをクリックします。以下のダイアログが開きます：
  ![signal setup](../images/signal-setup.png)
* ドロップダウンボックスで **Display units** **(2)** を **None** から **Time (autoscaling)/Milliseconds(ms)** に変更します。ドロップダウンが **Millisecond** に変わり、チャートのx軸がテストの実行時間を表すようになります。
* 設定 {{% icon icon="cog" %}} アイコンまたは {{% button style="gray" %}}close{{% /button %}} ボタンをクリックしてダイアログを閉じます。
* {{% button style="blue" %}}Link Detector{{% /button %}} ボタンをクリックし、先ほど作成したディテクターの名前を入力し始めて、ディテクターを追加します。
* ディテクター名をクリックして選択します。
* 以下に示すように、チャートの周りにアラートのステータスを示す色付きの枠線が表示され、ダッシュボードの上部にベルアイコンが表示されることに注目してください：
  ![detector added](../images/detector-added.png)
* {{% button style="blue" %}}Save and close{{% /button %}} ボタンをクリックします。
* ダッシュボードで、以下のスクリーンショットのようにチャートを移動します：
  ![Service Health Dashboard](../images/service-health-dashboard.png)
* 最後のタスクとして、ページの右上（**AI Assistant** の横）にある3つの縦のドット **⋮** をクリックし、**View fullscreen** をクリックします。これは壁掛けテレビモニターで使用するビューです（Esc キーを押すと戻ります）。

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

時間があれば、RUM メトリクスを使用してダッシュボードに別のカスタムチャートを追加してみてください。標準搭載の **RUM applications** ダッシュボードグループからチャートをコピーすることもできます。または、RUM メトリクス `rum.client_error.count` を使用して、アプリケーションのクライアントエラー数を表示するチャートを作成することもできます。

{{% /notice %}}

最後に、ワークショップのまとめを行います。
