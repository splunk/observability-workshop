---
title: チャートの探索
linkTitle: 1.02. Exploring Charts
weight: 1.02
---
このセクションでは、Splunk Observabilityでチャートがどのように構築・表示されるかを探索します。既存のチャートを確認・操作することで、チャートエディターの仕組み（データソースの選択方法、ビジュアルオプションの設定方法、各種設定が表示にどう影響するか）を理解できます。

## 1. チャートを選択する

まず、 **SAMPLE CHARTS** ダッシュボードが開いていることを確認し、ダッシュボード右上の時間範囲を **-5M**（過去5分間）に戻すか、 **reset to default** を選択します。

**Latency histogram** チャートを見つけ、チャートの右上にある **三点リーダー** (...) **(1)** をクリックします。メニューから **Open (3)** を選択します。チャートのタイトル（ **Latency histogram** ） **(2)** をクリックして直接開くこともできます。

![Sample Charts](../../images/latency-histogram-open.png)

---
チャートエディターが開くと、Latency histogramチャートの設定が表示されます。

チャートエディターでは、データの可視化方法を制御できます。チャートタイプの変更、変換関数の適用、時間設定の調整、その他のビジュアルおよびデータ関連オプションのカスタマイズが可能です。

![Latency Histogram](../../images/latency-histogram.png)

---

**Plot Editor (1)** タブの **Signal (2)** セクションに、現在使用されているメトリクス `demo.trans.latency` **(3)** があります。このシグナルは、チャートがプロットしているレイテンシデータを表しています。この領域で、シグナルを編集したり、追加のシグナルを加えて比較や可視化の強化ができます。

チャートには複数の **Line** プロットが表示されています。ラベル `18 ts` **(4)** は、チャートが現在 **18個の個別メトリクス時系列** をプロットしていることを示しています。
![Plot Editor](../../images/plot-editor.png)

さまざまな可視化スタイルを試すには、エディター内のチャートタイプアイコンをクリックします。各アイコンにカーソルを合わせると名前が表示され、各タイプが何を表すかを理解できます。

![Chart Types](../../images/chartbartypes.png)

例えば、 **Heat Map** アイコンをクリックすると、同じデータが異なるフォーマットでどのように表現されるかを確認できます。

![Change to Heatmap](../../images/change-to-heatmap.png)

{{% notice title="注意" style="info" %}}
さまざまなチャートタイプを使用してメトリクスを可視化できます。強調したいインサイトに最も適したタイプを選択してください。

利用可能なチャートタイプとその使い分けの詳細については、[Choosing a chart type](https://docs.splunk.com/Observability/data-visualization/charts/chart-types.html#chart-types)を参照してください。
{{% /notice %}}
