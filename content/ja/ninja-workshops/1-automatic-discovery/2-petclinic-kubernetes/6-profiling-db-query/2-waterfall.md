---
title: Trace Waterfall内のAlways-On Profiling
linkTitle: 2. Trace Waterfall
weight: 2
---

APM Waterfall ビューでオリジナルの Trace & Span **(1)**（または類似のもの）を選択し、右側のペイン (pane) から**Memory Stack Traces (2)**を選択してください：

![profiling from span](../../images/flamechart-in-waterfall.png)

ペイン (pane) に Memory Stack Trace Flame Graph **(3)**が表示されます。スクロール (scroll) するか、ペイン (pane) の右側をドラッグ (drag) して拡大できます。

AlwaysOn Profiling は、アプリケーション (application) のコード (code) のスナップショット (snapshot)、つまりスタックトレース (stack trace) を常に取得しています。何千ものスタックトレース (stack trace) を読まなければならないことを想像してみてください！それは現実的ではありません。これを支援するために、AlwaysOn Profiling はプロファイリング (profiling) データ (data) を集約して要約し、**Flame Graph**と呼ばれるビュー (view) で Call Stacks を探索する便利な方法を提供します。これは、アプリケーション (application) からキャプチャ (capture) されたすべてのスタックトレース (stack trace) の要約を表します。Flame Graph を使用して、パフォーマンス (performance) の問題を引き起こしている可能性のあるコード (code) の行を発見し、コード (code) に加えた変更が意図した効果を持っているかどうかを確認できます。

Always-on Profiling をさらに詳しく調べるには、**Memory Stack Traces**の下の Profiling Pane で上の画像で参照されている Span **(3)**を選択してください。これにより、Always-on Profiling のメイン (main) 画面が開き、Memory ビュー (view) があらかじめ選択されています：

![Profiling main](../../images/profiling-memory.png)

- Time フィルタ (filter) は、選択したスパン (span) の時間枠に設定されます **(1)**
- Java Memory Metric Charts **(2)**では、`Heap Memoryのモニター (monitor)`、`Memory Allocation Rate`や`Garbage Collecting` Metrics などの`Application Activity`を確認できます。
- スパン (span) **(3)**に関連するメトリクス (metrics) と Stack Traces のみにフォーカス/表示する機能。これにより、必要に応じて Java アプリケーション (application) で実行されているバックグラウンド (background) アクティビティ (activity) をフィルタ (filter) で除外できます。
- 識別された Java Function calls **(4)**により、その関数から呼び出されたメソッド (method) にドリルダウン (drill down) できます。
- プロファイル (profile) されたサービス (service) のスタックトレース (stack trace) に基づく階層の視覚化を持つ Flame Graph **(5)**。
- サービス (service) が複数のバージョン (version) を起動する場合に備えて、Service instance **(6)**を選択する機能。

さらなる調査のために、UI ではスタックトレース (stack trace) をクリックして、呼び出された関数と、フレームチャート (flame chart) から関連する行を確認できます。これを使用して、コーディング (coding) プラットフォーム (platform) で実際のコード (code) の行を表示できます（もちろん、お好みのコーディング (coding) プラットフォーム (platform) によって異なります）。

<!-- Once you have identified the relevant Function or Method you are interested in, `com.mysql.cj.protocol.a.NativePacketPayload.readBytes` in our example but yours may differ, so pick the top one **(1)**  and find it at the e bottom of the Flame Graph **(2)**. Click on it in the Flame Graph, it will show a pane as shown in the image below, where you can see the Thread information **(3)** by clicking on the blue *Show Thread Info* link. If you click on the *Copy Stack Trace* **(4)** button, you grab the actual stack trace that you can use in your coding platform to go to the actual lines of code used at this point (depending of course on your preferred Coding platform)

![stack trace](../../images/grab-stack-trace.png)

For more details on Profiling, check the the **Debug Problems workshop**, or  check the documents [here](https://docs.splunk.com/observability/en/apm/profiling/intro-profiling.html#introduction-to-alwayson-profiling-for-splunk-apm)> -->
