---
title: 新しいチャートの作成
linkTitle: 1.05. Create New Chart
weight: 1.05
---

### 1 新しいチャートの作成

新しいチャートを作成し、これまで操作してきたダッシュボードに追加しましょう！

まず、インターフェース上部中央のプラスアイコン **(1)** をクリックします。ドロップダウンから **Chart (2)** を選択します。
または、 {{< button style="blue">}}+ New Chart{{< /button >}} ボタン **(3)** をクリックして、直接新しいチャートを作成することもできます。

![Create new chart](../../images/new-chart.png)

空白のチャートテンプレートが表示され、設定の準備が整います。

![Empty Chart](../../images/empty-new-chart.png)

可視化するメトリクスを追加することから始めましょう。この例では、先ほど使用したものと同じメトリクス **`demo.trans.latency`** を引き続き使用します。

**Plot Editor (1)** で **Signal (2)** セクションに移動し、入力フィールドに **`demo.trans.latency`(3)** を入力します。これにより、レイテンシの時系列データがチャートに読み込まれ、可視化の構築とカスタマイズを開始できます。

![Signal](../../images/plot-editor.png)

**18個の時系列 (4)** を表示するおなじみの折れ線グラフが表示されます。最近のアクティビティを確認するには、 **Time ドロップダウン (1)** から **Past 15 minutes** を選択して時間範囲を変更します。

![Signal](../../images/line-chart-15-mins.png)
