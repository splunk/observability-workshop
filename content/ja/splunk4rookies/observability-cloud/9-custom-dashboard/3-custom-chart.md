---
title: カスタムチャートの追加
linkTitle: 2. カスタムチャートの追加
weight: 3
---

このワークショップのパートでは、ダッシュボードに追加するチャートを作成し、先ほど作成したディテクターにリンクします。これにより、テストの挙動を可視化し、テスト実行のいずれかがSLAに違反した場合にアラートを受け取れるようになります。

{{% exercise title="カスタムバーチャートを追加する" %}}

* ダッシュボードの上部にある **+** をクリックし、**Chart** を選択します。
  ![new chart screen](../images/new-chart.png)
* まず、{{% button style="grey" %}}Untitled chart{{% /button %}} の入力フィールドを使い、チャート名を **Overall Test Duration** とします。
* この演習ではバーチャートまたはカラムチャートを使うため、チャートオプションボックスの3番目のアイコン {{% icon icon="chart-bar" %}} をクリックします。
* **Plot editor** で **Signal** ボックスに `synthetics.run.duration.time.ms`（テストの実行時間）を入力し、Enterキーを押します。
* 現時点では、テストが実行されるリージョンごとに色の異なるバーが表示されています。これは不要なため、アナリティクスを追加して挙動を変更します。
* {{% button style="blue" %}}Add analytics{{% /button %}} ボタンをクリックします。
* ドロップダウンから **Mean** オプションを選択し、`mean:aggregation` を選んでダイアログボックスの外側をクリックします。メトリクスが集計されたことで、チャートが単色に変わります。
* 現状ではX軸が時間を表していないため、これを変更するにはプロットライン末尾の設定 {{% icon icon="cog" %}} アイコンをクリックします。次のダイアログが開きます:
  ![signal setup](../images/signal-setup.png)
* **Display units** **(2)** のドロップダウンボックスを **None** から **Time (autoscaling)/Milliseconds(ms)** に変更します。ドロップダウンが **Millisecond** に変わり、チャートのX軸がテスト実行時間を表すようになります。
* 設定 {{% icon icon="cog" %}} アイコンか {{% button style="gray" %}}close{{% /button %}} ボタンをクリックして、ダイアログを閉じます。
* {{% button style="blue" %}}Link Detector{{% /button %}} ボタンをクリックし、先ほど作成したディテクターの名前を入力し始めて、ディテクターを追加します。
* ディテクター名をクリックして選択します。
* 下記のように、アラートのステータスを示す色付きの枠線がチャートの周囲に表示され、ダッシュボード上部にベルアイコンが表示されます:
  ![detector added](../images/detector-added.png)
* {{% button style="blue" %}}Save and close{{% /button %}} ボタンをクリックします。
* ダッシュボード上で、下のスクリーンショットのようにチャートを並べ替えます:
  ![Service Health Dashboard](../images/service-health-dashboard.png)
* 最後のタスクとして、ページ右上（**AI Assistant** の隣）の縦の3点リーダー **⋮** をクリックし、**View fullscreen** をクリックします。これが壁掛けのTVモニターで使用するビューになります（Escキーで戻ります）。

{{% /exercise %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

時間に余裕があれば、RUMメトリクスを使ってもう1つカスタムチャートをダッシュボードに追加してみてください。すぐに使える **RUM applications** ダッシュボードグループからチャートをコピーしてもよいでしょう。また、RUMメトリクス `rum.client_error.count` を使って、アプリケーションのクライアントエラー数を表示するチャートを作成することもできます。

{{% /notice %}}

最後に、ワークショップのまとめに進みます。
