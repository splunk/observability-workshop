---
title: Always-On Profiling in the Trace Waterfall
linkTitle: 2. Trace Waterfall
weight: 2
---

APM Waterfall ビューで元の (または類似の) Trace と Span **(1)** を選択していることを確認し、右側のペインから **Memory Stack Traces (2)** を選択してください。

![profiling from span](../../images/flamechart-in-waterfall.png)

ペインに Memory Stack Trace Flame Graph **(3)** が表示されます。スクロールしたり、ペインの右端をドラッグして拡大したりできます。

AlwaysOn Profiling はアプリケーションのコードのスナップショット (スタックトレース) を継続的に取得しています。何千ものスタックトレースを読み込まなければならないことを想像してみてください。これは現実的ではありません。これを支援するために、AlwaysOn Profiling はプロファイリングデータを集約・サマライズし、**Flame Graph** と呼ばれるビューで Call Stack を簡単に探索できるようにしています。これはアプリケーションから取得したすべてのスタックトレースのサマリーを表しています。Flame Graph を使用して、どのコード行がパフォーマンス問題を引き起こしている可能性があるかを発見し、コードに加えた変更が意図した効果をもたらすかを確認できます。

Always-on Profiling をさらに詳しく調べるには、Profiling ペインの **Memory Stack Traces** の下にある Span **(3)** (上記画像で参照) を選択します。これにより、Memory ビューが事前選択された状態で Always-on Profiling のメイン画面が開きます。

![Profiling main](../../images/profiling-memory.png)

* Time フィルターは、選択した Span の時間枠に設定されます **(1)**
* Java Memory Metric Charts **(2)** では、`Monitor Heap Memory, Application Activity` として `Memory Allocation Rate` や `Garbage Collecting` などのメトリクスを確認できます。
* Span に関連するメトリクスとスタックトレースのみにフォーカス/表示する機能 **(3)**。これにより、必要に応じて Java アプリケーションで実行されているバックグラウンドアクティビティをフィルタリングできます。
* 識別された Java 関数呼び出し **(4)**。その関数から呼び出されたメソッドにドリルダウンできます。
* Flame Graph **(5)**。プロファイル対象サービスのスタックトレースに基づいた階層を可視化します。
* サービスが自身の複数バージョンを起動する場合に Service インスタンスを選択する機能 **(6)**。

さらなる調査のために、UI ではスタックトレースをクリックして、呼び出された関数と Flame Chart 内の関連する行を確認できます。これを使えば、コーディングプラットフォーム (もちろんお好みのコーディングプラットフォームによります) で実際のコード行を表示することができます。

<!-- Once you have identified the relevant Function or Method you are interested in, `com.mysql.cj.protocol.a.NativePacketPayload.readBytes` in our example but yours may differ, so pick the top one **(1)**  and find it at the e bottom of the Flame Graph **(2)**. Click on it in the Flame Graph, it will show a pane as shown in the image below, where you can see the Thread information **(3)** by clicking on the blue *Show Thread Info* link. If you click on the *Copy Stack Trace* **(4)** button, you grab the actual stack trace that you can use in your coding platform to go to the actual lines of code used at this point (depending of course on your preferred Coding platform)

![stack trace](../../images/grab-stack-trace.png)

For more details on Profiling, check the the **Debug Problems workshop**, or  check the documents [here](https://docs.splunk.com/observability/en/apm/profiling/intro-profiling.html#introduction-to-alwayson-profiling-for-splunk-apm)> -->
