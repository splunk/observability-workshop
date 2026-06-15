---
title: Tag Spotlight を使用した問題のトラブルシューティング
linkTitle: 5. Tag Spotlight を使用した問題のトラブルシューティング
weight: 5
time: 15 minutes
---

## APM データの探索

キャプチャした APM データを探索して、アプリケーションのパフォーマンスを確認しましょう。

**APM** に移動し、**Environment** ドロップダウンを使用して環境を選択します（例: `tagging-workshop-instancename`）。

サービスの一覧に `creditprocessorservice` と `creditcheckservice` が表示されるはずです:

![APM Overview](../images/apm_overview.png)

右側の **Service Map** をクリックしてサービスマップを表示します。`creditcheckservice` が `creditprocessorservice` を呼び出しており、平均応答時間が少なくとも 3 秒であることがわかります:

![Service Map](../images/service_map.png)

次に、右側の **Traces** をクリックして、このアプリケーションでキャプチャされたトレースを確認します。一部のトレースは比較的高速（数ミリ秒程度）に実行される一方、数秒かかるものもあることがわかります。

![Traces](../images/traces.png)

実行時間の長いトレースの 1 つをクリックします。この例では、トレースに 5 秒かかっており、ほとんどの時間が `creditprocessorservice` の一部である `/runCreditCheck` オペレーションの呼び出しに費やされていることがわかります:

![Long Running Trace](../images/long_running_trace.png)

しかし、なぜ一部のトレースは遅く、他のトレースは比較的速いのでしょうか？

トレースを閉じて Trace Analyzer に戻ります。**Errors only** を `on` に切り替えると、一部のトレースにエラーがあることにも気づくでしょう:

![Traces](../images/traces_with_errors.png)

エラーのあるトレースの 1 つを見ると、`creditprocessorservice` が `otherservice` という名前の別のサービスを呼び出そうとした時にエラーが発生していることがわかります。しかし、なぜ一部のリクエストは `otherservice` への呼び出しが発生し、他のリクエストでは発生しないのでしょうか？

![Trace with Errors](../images/error_trace.png)

一部のリクエストがなぜ遅いのか、また一部のリクエストがなぜエラーになるのかを特定するには、トレースを 1 つずつ確認して問題の背後にあるパターンを見つけることもできます。

**Splunk Observability Cloud** は、問題の根本原因を見つけるためのより良い方法を提供します。次にこれを探索しましょう。

## Tag Spotlight の使用

`credit.score.category` タグをインデックス化したので、**Tag Spotlight** を使用してアプリケーションのトラブルシューティングを行うことができます。

**APM** に移動し、右側の **Tag Spotlight** をクリックします。**Service** ドロップダウンから `creditcheckservice` サービスが選択されていることを確認します（まだ選択されていない場合）。

**Tag Spotlight** を使用すると、`impossible` のスコアとなるクレジットスコアリクエストの 100% がエラーになっている一方で、他のすべてのクレジットスコアタイプのリクエストにはエラーがまったくないことがわかります！

**![Tag Spotlight with Errors](../images/tag_spotlight_errors.png)**

これは **Tag Spotlight** の威力を示しています！この機能がなければ、このパターンを見つけるのは非常に時間がかかるでしょう。何百ものトレースを手動で確認してパターンを特定する必要があり（それでも見つけられる保証はありません）。

エラーについて確認しましたが、レイテンシーはどうでしょうか？**Requests & errors distribution** ドロップダウンをクリックして **Latency distribution** に変更しましょう。

> IMPORTANT: **Cards display** の横にある設定アイコンをクリックして、P50 と P99 のメトリクスを追加してください。

ここでは、`poor` クレジットスコアのリクエストが遅く実行されており、P50、P90、P99 の時間が約 3 秒であることがわかります。これはユーザーが待つには長すぎる時間であり、他のリクエストよりもはるかに遅いです。

また、`exceptional` クレジットスコアのリクエストの一部も遅く実行されており、P99 の時間が約 5 秒であることがわかりますが、P50 の応答時間は比較的速いです。

**![Tag Spotlight with Latency](../images/tag_spotlight_latency.png)**

## Dynamic Service Maps の使用

リクエストに関連付けられたクレジットスコアカテゴリがパフォーマンスとエラー率に影響を与える可能性があることがわかったので、インデックス化されたタグを活用する別の機能、**Dynamic Service Maps** を探索しましょう。

Dynamic Service Maps を使用すると、特定のサービスをタグごとに分解できます。例えば、**APM** をクリックし、**Service Map** をクリックしてサービスマップを表示しましょう。

`creditcheckservice` をクリックします。次に、右側のメニューで **Breakdown** と表示されているドロップダウンをクリックし、`credit.score.category` タグを選択します。

この時点で、サービスマップが動的に更新され、クレジットスコアカテゴリ別に分解された `creditcheckservice` へのリクエストのパフォーマンスを確認できます:

**![Service Map Breakdown](../images/service_map_breakdown.png)**

このビューにより、`good` と `fair` のクレジットスコアのパフォーマンスは優れている一方、`poor` と `exceptional` のスコアははるかに遅く、`impossible` のスコアはエラーになることが明確にわかります。

## 調査結果

**Tag Spotlight** により、このサービスを担当するエンジニアがさらに調査すべきいくつかの興味深いパターンが明らかになりました:

* なぜすべての `impossible` クレジットスコアリクエストがエラーになるのか？
* なぜすべての `poor` クレジットスコアリクエストが遅いのか？
* なぜ一部の `exceptional` リクエストが遅いのか？

SRE として、このコンテキストをエンジニアリングチームに渡すことは、調査に非常に役立ちます。単にサービスが「時々遅い」と伝えるよりも、はるかに迅速に問題を追跡できるようになるためです。

興味がある場合は、`creditprocessorservice` のソースコードを確認してみてください。impossible、poor、exceptional のクレジットスコアのリクエストは異なる方法で処理されているため、発見したエラー率とレイテンシーの違いが生じていることがわかります。

アプリケーションで観察した動作は、現代のクラウドネイティブアプリケーションの典型的なものです。サービスに渡される異なる入力が異なるコードパスにつながり、一部のパスではパフォーマンスが低下したりエラーが発生したりします。例えば、実際のクレジットチェックサービスでは、低いクレジットスコアとなるリクエストはリスクをさらに評価するために別の下流サービスに送信される場合があり、高いスコアのリクエストよりも遅くなったり、エラー率が高くなったりする可能性があります。
