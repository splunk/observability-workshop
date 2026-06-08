---
title: トレースウォーターフォールでの Always-On Profiling
linkTitle: 2. Trace Waterfall
weight: 2
---

APM ウォーターフォールビューで元の（または類似の）Trace & Span **(1)** が選択されていることを確認し、右側のペインから **Memory Stack Traces (2)** を選択します:

![profiling from span](../../images/flamechart-in-waterfall.png)

ペインに Memory Stack Trace Flame Graph **(3)** が表示されます。下にスクロールしたり、ペインの右側をドラッグして拡大したりできます。

AlwaysOn Profiling は、アプリケーションのコードのスナップショット（スタックトレース）を常に取得しています。何千ものスタックトレースを読み通すことを想像してみてください！それは現実的ではありません。これを支援するために、AlwaysOn Profiling はプロファイリングデータを集約・要約し、**Flame Graph** と呼ばれるビューでコールスタックを探索する便利な方法を提供します。これはアプリケーションからキャプチャされたすべてのスタックトレースの要約を表します。Flame Graph を使用して、パフォーマンスの問題を引き起こしている可能性のあるコード行を発見し、コードに加えた変更が意図した効果を持っているかどうかを確認できます。

Always-on Profiling をさらに詳しく調べるには、**Memory Stack Traces** の下にある Profiling ペインで Span **(3)**（上の画像を参照）を選択します。これにより、Memory ビューが事前に選択された状態で Always-on Profiling のメイン画面が開きます:

![Profiling main](../../images/profiling-memory.png)

* Time フィルターは、選択したスパンの時間枠に設定されます **(1)**
* Java Memory Metric Charts **(2)** では、ヒープメモリ、メモリ割り当て率などのアプリケーションアクティビティ、およびガベージコレクションを監視できます。
* スパンに関連するメトリクスとスタックトレースのみにフォーカス/表示する機能 **(3)**。必要に応じて、Java アプリケーションで実行されているバックグラウンドアクティビティをフィルタリングできます。
* 識別された Java 関数呼び出し **(4)**。その関数から呼び出されたメソッドにドリルダウンできます。
* Flame Graph **(5)**。プロファイリングされたサービスのスタックトレースに基づく階層の視覚化です。
* サービスが複数のバージョンを起動している場合に、サービスインスタンスを選択する機能 **(6)**。

さらに調査するために、UI ではスタックトレースをクリックして、呼び出された関数とフレームチャートの関連する行を確認できます。その後、お好みのコーディングプラットフォームでこれを相互参照して、関連するソースコードの実際の行を表示できます。

<!-- Once you have identified the relevant Function or Method you are interested in, `com.mysql.cj.protocol.a.NativePacketPayload.readBytes` in our example but yours may differ, so pick the top one **(1)**  and find it at the e bottom of the Flame Graph **(2)**. Click on it in the Flame Graph, it will show a pane as shown in the image below, where you can see the Thread information **(3)** by clicking on the blue *Show Thread Info* link. If you click on the *Copy Stack Trace* **(4)** button, you grab the actual stack trace that you can use in your coding platform to go to the actual lines of code used at this point (depending of course on your preferred Coding platform)

![stack trace](../../images/grab-stack-trace.png)

For more details on Profiling, check the the **Debug Problems workshop**, or  check the documents [here](https://docs.splunk.com/observability/en/apm/profiling/intro-profiling.html#introduction-to-alwayson-profiling-for-splunk-apm)> -->
