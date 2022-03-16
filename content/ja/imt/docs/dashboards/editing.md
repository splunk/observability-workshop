---
title: Editing charts
linkTitle: Editing charts
weight: 3
---

# チャートを編集する

## 1. チャートの編集

**Sample Data** ダッシュボードにある **Latency histogram** チャートの3点 **`...`** をクリックして、**Open** をクリックします（または、チャートの名前をクリックしてください、ここでは **Latency histogram** です）。

![Sample Charts](../../../images/sample-charts.png)

チャートエディターのUIには、**Latency histogram** チャートのプロットオプション、カレントプロット、シグナル（メトリック）が表示されます。

![Latency Histogram](../../../images/latency-histogram.png)

**Plot Editor** タブの **Signal** には、現在プロットしている **`demo.trans.latency`** というメトリックが表示されます。

![Plot Editor](../../../images/plot-editor.png)

いくつかの **Line** プロットが表示されます。**`18 ts`** という数字は、18個の時系列メトリックをチャートにプロットしていることを示しています。

異なるチャートタイプのアイコンをクリックして、それぞれの表示を確認してください。スワイプしながらその名前を確認してください。例えば、ヒートマップのアイコンをクリックします。

![Chart Types](../../../images/M-Editing-2.png)

チャートがヒートマップに変わります。。

![Change to Heatmap](../../../images/change-to-heatmap.png)

!!! note
    様々なチャートを使用してメトリクスを視覚化することができます。自分が望む視覚化に最も適したチャートタイプを選択してください。

    各チャートタイプの詳細については、[Choosing a chart type](https://docs.splunk.com/Observability/data-visualization/charts/chart-types.html#chart-types) を参照してください。

チャートタイプの **Line** をクリックすると、線グラフが表示されます。

![Line Chart](../../../images/M-Editing-3b.png)

## 2. タイムウィンドウの変更

また、**Time** ドロップダウンから **Past 15 minutes** に変更することで、チャートの時間枠を変更することができます。

![Line Chart](../../../images/line-chart.png)

## 3. データテーブルの表示

**Data Table** タブをクリックします。

![Data Table](../../../images/data-table.png)

18行が表示され、それぞれがいくつかの列を持つ時系列メトリックを表しています。これらの列は、メトリックのディメンションを表しています。`demo.trans.latency` のディメンジョンは次のとおりです。

- `demo_datacenter`
- `demo_customer`
- `demo_host`

**`demo_datacenter`** 列では、メトリクスを取得している2つのデータセンター、**Paris** と **Tokyo** があることがわかります。

グラフの線上にカーソルを横に移動させると、それに応じてデータテーブルが更新されるのがわかります。チャートのラインの1つをクリックすると、データテーブルに固定された値が表示されます。

---

ここでもう一度 **Plot editor** をクリックしてデータテーブルを閉じ、このチャートをダッシュボードに保存して、後で使用しましょう。
