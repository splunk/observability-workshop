---
title: Using Filters & Formulas
weight: 7
---

# フィルターと数式の使い方

---

## 1 新しいチャートの作成

それでは、新しいチャートを作成し、ダッシュボードに保存してみましょう。

UIの右上にある + アイコンを選択し、ドロップダウンから **Chart** を選択します。
または、{{< labelbutton  >}}+ New Chart{{< /labelbutton >}} ボタンをクリックすると、新しいチャートが作成されます。

![Create new chart](../../../images/M-Filter-0.png)

これで、以下のようなチャートのテンプレートが表示されます。

![Empty Chart](../../../images/M-Editing-6.png)

プロットするメトリックを入力してみましょう。ここでは、**`demo.trans.latency`** というメトリックを使用します。

**Plot Editor** タブの **Signal** に **`demo.trans.latency`** を入力します。

![Signal](../../../images/plot-editor.png)

すると、折れ線グラフが表示されるはずです。時間を15分に切り替えてみてください。

![Signal](../../../images/M-Filter-10.png)

## 2. フィルタリングと分析

次に、**Paris** データセンターを選択して分析を行ってみましょう。そのためにはフィルタを使用します。

**Plot Editor** タブに戻り、**Add Filter**{: .label-button .sfx-ui-button-blue} をクリックして、入力補助として選択肢が出てくるので、そこから **`demo_datacenter`** を選択し、**`Paris`** を選択します。

![Filter](../../../images/M-Filter-1.png)

**F(x)** 列に、分析関数 **`Percentile:Aggregation`** を追加し、値を **`95`** にします（枠外をクリックすると設定が反映されます）。

![Analytics](../../../images/M-Filter-2.png)

**Percentile** 関数やその他の関数の情報は、[Chart Analytics](https://docs.splunk.com/Observability/data-visualization/charts/gain-insights-through-chart-analytics.html#gain-insights-through-chart-analytics) を参照してください。

---

## 3. タイムシフト分析機能の使用

それでは、以前のメトリックと比較してみましょう。**`...`** をクリックして、ドロップダウンから **Clone** をクリックし、Signal **A** をクローンします。

![Clone Signal](../../../images/M-Filter-3.png)

**A** と同じような新しい行が **B** という名前で表示され、プロットされているのがわかります。

![Plot Editor](../../../images/M-Filter-4.png)

シグナル **B** に対して、**F(x)** 列に分析関数 **Timeshift** を追加し、**`1w`**（もしくは `7d` でも同じ意味です）と入力し、外側をクリックして反映させます。

![Timeshift](../../../images/M-Filter-5.png)

右端の歯車をクリックして、**Plot Color** を選択（例：ピンク）すると、 **B** のプロットの色を変更できます。

![Change Plot Colour](../../../images/M-Filter-6.png)

**Close** をクリックして、設定を終えます。

シグナル **A** （過去15分）のプロットが青、1週間前のプロットがピンクで表示されています。

より見やすくするために、**Area chart** アイコンをクリックして表示方法を変更してみましょう。

![Area Chart](../../../images/M-Filter-8.png)

これで、前週にレイテンシーが高かった時期を確認することができます。

次に、Override バーの **Time** の隣にあるフィールドをクリックし、ドロップダウンから **`Past Hour`**を 選択してみましょう。

![Timeframe](../../../images/M-Filter-9.png)

---

## 4. 計算式を使う

ここでは、1日と7日の間のすべてのメトリック値の差をプロットしてみましょう。

**Enter Formula**{: .label-button .sfx-ui-button-blue} をクリックして、**`A-B`** （AからBを引いた値）を入力し、**C** を除くすべてのシグナルを隠します（目アイコンの選択を解除します）。

![Formulas](../../../images/M-Filter-11.png)

これで、 **A** と **B** のすべてのメトリック値の差だけがプロットされているのがわかります。**B** のメトリック値が、その時点での **A** のメトリック値よりも何倍か大きな値を持っているためです。

次のモジュールで、チャートとディテクターを動かすための SignalFlow を見てみましょう。
