---
title: Tag Spotlight を使用した問題のトラブルシューティング
linkTitle: 5. Tag Spotlight を使用した問題のトラブルシューティング
weight: 5
time: 15 minutes
---

## APM データの探索

キャプチャした APM データの一部を探索して、アプリケーションのパフォーマンスを確認してみましょう。

**APM** に移動し、**Environment** ドロップダウンから自分の環境（例：`tagging-workshop-instancename`）を選択します。

サービス一覧に `creditprocessorservice` と `creditcheckservice` が表示されているはずです。

![APM Overview](../images/apm_overview.png)

右側の **Service Map** をクリックして、サービスマップを表示します。`creditcheckservice` が `creditprocessorservice` を呼び出しており、平均応答時間が少なくとも 3 秒であることがわかります。

![Service Map](../images/service_map.png)

次に、右側の **Traces** をクリックして、このアプリケーションでキャプチャされたトレースを確認します。一部のトレースは比較的高速（数ミリ秒程度）ですが、他のトレースは数秒かかることがわかります。

![Traces](../images/traces.png)

実行時間が長いトレースの 1 つをクリックします。この例では、トレースに 5 秒かかっており、ほとんどの時間が `creditprocessorservice` の一部である `/runCreditCheck` 操作の呼び出しに費やされていることがわかります。

![Long Running Trace](../images/long_running_trace.png)

しかし、なぜ一部のトレースは遅く、他のトレースは比較的速いのでしょうか？

トレースを閉じて Trace Analyzer に戻ります。**Errors only** を `on` に切り替えると、エラーが発生しているトレースもあることに気づくでしょう。

![Traces](../images/traces_with_errors.png)

エラートレースの 1 つを見ると、`creditprocessorservice` が `otherservice` という別のサービスを呼び出そうとしたときにエラーが発生していることがわかります。しかし、なぜ一部のリクエストは `otherservice` の呼び出しを引き起こし、他のリクエストはそうならないのでしょうか？

![Trace with Errors](../images/error_trace.png)

一部のリクエストが遅く、一部のリクエストでエラーが発生する理由を特定するために、トレースを 1 つずつ確認して、問題の背後にあるパターンを見つけ出すこともできます。

**Splunk Observability Cloud** には、問題の根本原因を見つけるためのより良い方法があります。次にこれを探索します。

## Tag Spotlight の使用

`credit.score.category` タグをインデックス化したので、これを **Tag Spotlight** と組み合わせてアプリケーションのトラブルシューティングに使用できます。

**APM** に移動し、右側の **Tag Spotlight** をクリックします。**Service** ドロップダウンから `creditcheckservice` サービスが選択されていることを確認してください（まだ選択されていない場合）。

**Tag Spotlight** を使用すると、`impossible` のスコア結果になるクレジットスコアリクエストの 100% でエラーが発生している一方で、他のすべてのクレジットスコアタイプのリクエストではエラーがまったく発生していないことがわかります。

**![Tag Spotlight with Errors](../images/tag_spotlight_errors.png)**

これが **Tag Spotlight** の威力です。これがなければパターンを見つけるのに時間がかかり、何百ものトレースを手作業で確認してパターンを特定する必要があり（それでも見つかる保証はありません）、非常に手間がかかります。

エラーを見てきましたが、レイテンシーはどうでしょうか？ **Requests & errors distribution** ドロップダウンをクリックし、**Latency distribution** に変更しましょう。

> IMPORTANT: **Cards display** の横にある設定アイコンをクリックして、P50 および P99 メトリクスを追加します。

ここでは、`poor` クレジットスコアのリクエストが遅く実行されており、P50、P90、P99 の時間がいずれも約 3 秒であることがわかります。これはユーザーが待つには長すぎる時間で、他のリクエストよりもはるかに遅くなっています。

また、`exceptional` クレジットスコアのリクエストの一部も遅く、P99 時間が約 5 秒となっていますが、P50 応答時間は比較的高速であることもわかります。

**![Tag Spotlight with Latency](../images/tag_spotlight_latency.png)**

## Dynamic Service Maps の使用

リクエストに関連付けられたクレジットスコアカテゴリーがパフォーマンスとエラー率に影響を与える可能性があることがわかったので、インデックス化されたタグを活用する別の機能である **Dynamic Service Maps** を探索しましょう。

Dynamic Service Maps を使用すると、特定のサービスをタグごとに分解できます。たとえば、**APM** をクリックしてから **Service Map** をクリックしてサービスマップを表示します。

`creditcheckservice` をクリックします。次に、右側のメニューで **Breakdown** と表示されているドロップダウンをクリックし、`credit.score.category` タグを選択します。

この時点で、サービスマップは動的に更新され、`creditcheckservice` にヒットするリクエストのパフォーマンスがクレジットスコアカテゴリー別に分解されて表示されます。

**![Service Map Breakdown](../images/service_map_breakdown.png)**

このビューから、`good` および `fair` クレジットスコアのパフォーマンスは優れている一方で、`poor` および `exceptional` スコアははるかに遅く、`impossible` スコアはエラーを引き起こしていることが明確になります。

## 調査結果

**Tag Spotlight** は、このサービスを所有するエンジニアがさらに調査すべきいくつかの興味深いパターンを明らかにしました。

* なぜすべての `impossible` クレジットスコアリクエストでエラーが発生するのか？
* なぜすべての `poor` クレジットスコアリクエストが遅いのか？
* なぜ一部の `exceptional` リクエストが遅いのか？

SRE として、このコンテキストをエンジニアリングチームに伝えることは、彼らの調査において非常に有用です。サービスが「時々遅い」とだけ伝えるよりも、はるかに迅速に問題を追跡できるようになるからです。

興味があれば、`creditprocessorservice` のソースコードを見てみてください。impossible、poor、exceptional のクレジットスコアを持つリクエストはそれぞれ異なる方法で処理されており、これが私たちが明らかにしたエラー率とレイテンシーの違いを引き起こしていることがわかります。

このアプリケーションで観察された動作は、サービスに渡されるさまざまな入力が異なるコードパスを引き起こし、その一部がパフォーマンスの低下やエラーを引き起こす、現代のクラウドネイティブアプリケーションでは典型的なものです。たとえば、実際のクレジットチェックサービスでは、低いクレジットスコアになるリクエストはリスクをさらに評価するために別のダウンストリームサービスに送信される場合があり、より高いスコアになるリクエストよりも実行が遅くなったり、エラー率が高くなったりすることがあります。
