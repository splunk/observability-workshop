---
title: 新しいチャートの作成
linkTitle: 1.05. Create New Chart
weight: 1.05
---

### 1 新しいチャートの作成

それでは、新しいチャートを作成して、作業中のダッシュボードに追加しましょう！

開始するには、インターフェースの上部中央にあるプラスアイコン **(1)** をクリックします。ドロップダウンから **Chart (2)** を選択します。
または、{{< button style="blue">}}+ New Chart{{< /button >}} ボタン **(3)** をクリックして、新しいチャートを直接作成することもできます。

![Create new chart](../../images/new-chart.png)

設定の準備ができた空白のチャートテンプレートが表示されます：

![Empty Chart](../../images/empty-new-chart.png)

まず、可視化するメトリクスを追加しましょう。この例では、先ほど使用したのと同じメトリクス **`demo.trans.latency`** を引き続き使用します。

**Plot Editor (1)** で、**Signal (2)** セクションに移動し、入力フィールドに **`demo.trans.latency`(3)** を入力します。これにより、レイテンシの時系列データがチャートにロードされ、可視化の構築とカスタマイズを開始できます。

![Signal](../../images/plot-editor.png)

**18個の時系列 (4)** を表示する見慣れた折れ線グラフが表示されるはずです。最近のアクティビティを表示するには、**Time dropdown (1)** から **Past 15 minutes** を選択して時間範囲を変更します。

![Signal](../../images/line-chart-15-mins.png)
