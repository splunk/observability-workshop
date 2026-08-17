---
title: チャートの探索
linkTitle: 1.02. Exploring Charts
weight: 1.02
---
このセクションでは、Splunk Observabilityでチャートがどのように構築され表示されるかを探索することから始めます。既存のチャートを調べて操作することで、チャートエディタの動作方法、データソースの選択方法、ビジュアルオプションの設定方法、そしてさまざまな設定が表示内容にどのように影響するかを理解できます。

## 1. チャートの選択

開始するには、**SAMPLE CHARTS** ダッシュボードを開いていることを確認し、ダッシュボードの右上隅にある時間範囲を **-5M**（過去5分間）に戻すか、**reset to default** を選択してください。

**Latency histogram** チャートを見つけて、チャートの右上隅にある **three dots** (...) **(1)** をクリックします。メニューから **Open (3)** を選択します。また、チャートタイトル (**Latency histogram**) **(2)** をクリックして直接開くこともできます。

![Sample Charts](../../images/latency-histogram-open.png)

---
チャートエディタが開くと、Latency histogramチャートの設定が表示されます。

チャートエディタは、データの可視化方法を制御できる場所です。チャートタイプの変更、変換関数の適用、時間設定の調整、その他のビジュアルおよびデータ関連のオプションを特定のニーズに合わせてカスタマイズできます。

![Latency Histogram](../../images/latency-histogram.png)

---

**Plot Editor (1)** タブの **Signal (2)** セクションで、現在使用されているメトリクス `demo.trans.latency` **(3)** を確認できます。このシグナルは、チャートがプロットしているレイテンシデータを表しています。このエリアを使用して、シグナルを編集したり、追加のシグナルを追加して可視化を比較または充実させることができます。

チャートには複数の **Line** プロットが表示されています。ラベル `18 ts` **(4)** は、チャートが現在 **18個の個別のメトリクス時系列** をプロットしていることを示しています。
![Plot Editor](../../images/plot-editor.png)

さまざまな可視化スタイルを探索するには、エディタ内のさまざまなチャートタイプアイコンをクリックしてみてください。各アイコンにカーソルを合わせると、その名前が表示され、各タイプが何を表すかを理解するのに役立ちます。

![Chart Types](../../images/chartbartypes.png)

たとえば、**Heat Map** アイコンをクリックして、同じデータが異なるフォーマットでどのように表現されるかを確認してみてください。

![Change to Heatmap](../../images/change-to-heatmap.png)

{{% notice title="Note" style="info" %}}
さまざまなチャートタイプを使用してメトリクスを可視化できます。強調したい洞察を最もよく表現するものを選択してください。

利用可能なチャートタイプとその使用タイミングの詳細な概要については、[Choosing a chart type.](https://docs.splunk.com/Observability/data-visualization/charts/chart-types.html#chart-types) を参照してください。
{{% /notice %}}
