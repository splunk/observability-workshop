---
title: Trace Waterfall内のAlways-On Profiling
linkTitle: 2. Trace Waterfall
weight: 2
---

APM WaterfallビューでオリジナルのTrace & Span **(1)**（または類似のもの）を選択し、右側のペインから**Memory Stack Traces (2)**を選択してください：

![profiling from span](../../images/flamechart-in-waterfall.png)

ペインにMemory Stack Trace Flame Graph **(3)**が表示されます。スクロールするか、ペインの右側をドラッグして拡大できます。

AlwaysOn Profilingは、アプリケーションのコードのスナップショット、つまりスタックトレースを常に取得しています。何千ものスタックトレースを読まなければならないことを想像してみてください！それは現実的ではありません。これを支援するために、AlwaysOn Profilingはプロファイリングデータを集約して要約し、**Flame Graph**と呼ばれるビューでCall Stacksを探索する便利な方法を提供します。これは、アプリケーションからキャプチャされたすべてのスタックトレースの要約を表します。Flame Graphを使用して、パフォーマンスの問題を引き起こしている可能性のあるコードの行を発見し、コードに加えた変更が意図した効果を持っているかどうかを確認できます。

Always-on Profilingをさらに詳しく調べるには、**Memory Stack Traces**の下のProfiling Paneで上の画像で参照されているSpan **(3)**を選択してください。これにより、Always-on Profilingのメイン画面が開き、Memoryビューがあらかじめ選択されています：

![Profiling main](../../images/profiling-memory.png)

- Timeフィルタは、選択したスパンの時間枠に設定されます **(1)**
- Java Memory Metric Charts **(2)**では、`Heap Memoryのモニター`、`Memory Allocation Rate` や `Garbage Collecting` Metricsなどの `Application Activity` を確認できます。
- スパン **(3)**に関連するメトリクスとStack Tracesのみにフォーカス/表示する機能。これにより、必要に応じてJavaアプリケーションで実行されているバックグラウンドアクティビティをフィルタで除外できます。
- 識別されたJava Function calls **(4)**により、その関数から呼び出されたメソッドにドリルダウンできます。
- プロファイルされたサービスのスタックトレースに基づく階層の視覚化を持つFlame Graph **(5)**。
- サービスが複数のバージョンを起動する場合に備えて、Service instance **(6)**を選択する機能。

さらなる調査のために、UIではスタックトレースをクリックして、呼び出された関数と、フレームチャートから関連する行を確認できます。これを使用して、コーディングプラットフォームで実際のコードの行を表示できます（もちろん、お好みのコーディングプラットフォームによって異なります）。

<!-- Once you have identified the relevant Function or Method you are interested in, `com.mysql.cj.protocol.a.NativePacketPayload.readBytes` in our example but yours may differ, so pick the top one **(1)**  and find it at the e bottom of the Flame Graph **(2)**. Click on it in the Flame Graph, it will show a pane as shown in the image below, where you can see the Thread information **(3)** by clicking on the blue *Show Thread Info* link. If you click on the *Copy Stack Trace* **(4)** button, you grab the actual stack trace that you can use in your coding platform to go to the actual lines of code used at this point (depending of course on your preferred Coding platform)

![stack trace](../../images/grab-stack-trace.png)

For more details on Profiling, check the the **Debug Problems workshop**, or  check the documents [here](https://docs.splunk.com/observability/en/apm/profiling/intro-profiling.html#introduction-to-alwayson-profiling-for-splunk-apm)> -->
