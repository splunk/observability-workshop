---
title: Exploring Charts
linkTitle: 1.02. Exploring Charts
weight: 1.02
---
このセクションでは、Splunk Observability におけるチャートの構築方法と表示方法を確認していきます。既存のチャートを観察し操作することで、チャートエディタの動作の仕組み（データソースの選択方法、ビジュアルオプションの構成方法、各種設定が表示にどう影響するか）を体感できます。

## 1. チャートを選択する

まずは **SAMPLE CHARTS** ダッシュボードを開いた状態にし、ダッシュボード右上の時間範囲を **-5M** (Last 5 Minutes) に戻すか、**reset to default** を選択してください。

**Latency histogram** チャートを見つけ、チャート右上の **三点リーダー** (...) **(1)** をクリックします。メニューから **Open (3)** を選択します。あるいは、チャートタイトル（**Latency histogram**）**(2)** を直接クリックして開くこともできます。

![Sample Charts](../../images/latency-histogram-open.png)

---
チャートエディタが開くと、Latency histogram チャートの構成設定が表示されます。

チャートエディタは、データの可視化方法を制御するための場所です。チャートタイプの変更、変換関数の適用、時間設定の調整、その他のビジュアル関連やデータ関連のオプションを、目的に合わせてカスタマイズできます。

![Latency Histogram](../../images/latency-histogram.png)

---

**Plot Editor (1)** タブの **Signal (2)** セクションには、現在使用されているメトリクス `demo.trans.latency` **(3)** が表示されています。このシグナルは、チャートでプロットされているレイテンシーデータを表しています。このエリアでは、シグナルを編集したり、比較や情報の追加のために別のシグナルを追加したりできます。

チャートには、複数の **Line** プロットが表示されていることがわかります。`18 ts` **(4)** というラベルは、チャートが現在 **18 個の個別のメトリクス時系列** をプロットしていることを示しています。
![Plot Editor](../../images/plot-editor.png)

さまざまな可視化スタイルを試すために、エディタにある各チャートタイプのアイコンをクリックしてみてください。各アイコンにマウスカーソルを合わせると名前が表示され、それぞれのタイプが何を表しているかを把握できます。

![Chart Types](../../images/chartbartypes.png)

たとえば、**Heat Map** アイコンをクリックして、同じデータが別の形式でどのように表現されるかを確認してみましょう。

![Change to Heatmap](../../images/change-to-heatmap.png)

{{% notice title="Note" style="info" %}}
メトリクスはさまざまなチャートタイプで可視化できます。強調したいインサイトを最もよく表すものを選んでください。

利用可能なチャートタイプとその使い分けの詳細については、[Choosing a chart type.](https://docs.splunk.com/Observability/data-visualization/charts/chart-types.html#chart-types) を参照してください。
{{% /notice %}}
