---
title: Create New Chart
linkTitle: 1.05. Create New Chart
weight: 1.05
---

### 1 新しいチャートの作成

それでは、新しいチャートを作成し、これまで作業してきたダッシュボードに追加してみましょう。

まず、画面上部中央のプラスアイコン **(1)** をクリックします。ドロップダウンから **Chart (2)** を選択してください。
あるいは、{{< button style="blue">}}+ New Chart{{< /button >}} ボタン **(3)** をクリックすることで、直接新しいチャートを作成することもできます。

![Create new chart](../../images/new-chart.png)

これで、設定可能な空のチャートテンプレートが表示されます:

![Empty Chart](../../images/empty-new-chart.png)

可視化するメトリクスを追加することから始めましょう。今回の例では、これまでと同じく **`demo.trans.latency`** を引き続き使用します。

**Plot Editor (1)** の **Signal (2)** セクションに移動し、入力フィールドに **`demo.trans.latency`(3)** を入力します。これにより、レイテンシーの時系列データがチャートに読み込まれ、可視化の構築とカスタマイズを開始できるようになります。

![Signal](../../images/plot-editor.png)

これで、見慣れたラインチャートに **18 個の時系列 (4)** が表示されているはずです。最近のアクティビティを確認するには、**Time dropdown (1)** から **Past 15 minutes** を選択して時間範囲を変更してください。

![Signal](../../images/line-chart-15-mins.png)
