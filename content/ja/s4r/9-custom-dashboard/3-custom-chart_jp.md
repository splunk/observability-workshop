---
title: カスタムチャートの追加
linkTitle: 3. カスタムチャートの追加
weight: 3
---

このワークショップのこのセクションでは、ダッシュボードに追加するチャートを作成し、以前に構築したディテクタにリンクします。これにより、テストの動作を確認し、テストがSLAを違反した場合にアラートを受け取ることができます。

{{% notice title="Exercise" style="green" icon="running" %}}

* ダッシュボードの上部で**+**をクリックし、**Chart**を選択します。
  ![new chart screen](../images/new-chart.png)
* まず、{{% button style="grey" %}}Untitled chart{{% /button %}}の入力フィールドを使用して、チャートの名前を**Overall Test Duration**にします。
* このエクササイズでは、棒グラフまたはカラムグラフが必要なので、チャートオプションボックスの3番目のアイコン {{% icon icon="chart-bar" %}} をクリックします。
* **Plot editor**に `synthetics.run.duration.time.ms`（これはテストの実行時間の期間です）を入力して、**Signal**ボックスでEnterキーを押します。
* 現時点では、異なる色の棒が表示されますが、これはテストが実行される各地域ごとの色分けが必要ないため、いくつかの解析を追加してこの動作を変更できます。
* {{% button style="blue" %}}Add analytics{{% /button %}}ボタンをクリックします。
* ドロップダウンから**Mean**オプションを選択し、`mean:aggregation`を選択してダイアログボックスの外側をクリックします。メトリクスが統合されるため、チャートが単一の色に変わります。
* x軸は現在、時間を表していません。これを変更するには、プロットラインの末尾にある設定 {{% icon icon="cog" %}} アイコンをクリックします。次のダイアログが表示されます：
  ![signal setup](../images/signal-setup.png)
* **Display units**（**2**）を**None**から**Time (autoscaling)/Milliseconds(ms)**に変更します。ドロップダウンが**Millisecond**に変わり、チャートのx軸がテストの実行時間を表すようになります。
* ダイアログを閉じるには、設定 {{% icon icon="cog" %}} アイコンまたは{{% button style="gray" %}}close{{% /button %}}ボタンをクリックします。
* ディテクタを追加するには、{{% button style="blue" %}}Link Detector{{% /button %}}ボタンをクリックして、以前に作成したディテクタの名前を入力し始めます。
* ディテクタの名前をクリックして選択します。
* チャートの周りに着色されたボーダーが表示され、ダッシュボードの上部にベルアイコンが表示されます（以下の画像参照）：
  ![detector added](../images/detector-added.png)
* {{% button style="blue" %}}Save and close{{% /button %}}ボタンをクリックします。
* ダッシュボードで、チャートを以下のスクリーンショットのように移動させます：
  ![Service Health Dashboard](../images/service-health-dashboard.png)
* 最後のタスクとして、ページの上部の三点リーダー **...**（**Event Overlay**の横）をクリックし、**View fullscreen**をクリックします。これが、壁に取り付けられたTVモニターで使用する表示方法です（戻るにはEscキーを押します）。

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

暇な時間には、RUMメトリクスを使用してダッシュボードに別のカスタムチャートを追加してみてください。既存の**RUM applications**ダッシュボードグループからチャートをコピーするか、`rum.client_error.count`を使用してアプリケーションのクライアントエラーの数を表示するチャートを作成できます。

{{% /notice %}}

最後に、ワークショップの締めくくりを行います。
