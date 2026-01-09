---
title: Tag Spotlight を使用して問題をトラブルシューティングする
linkTitle: 5. Tag Spotlight を使用して問題をトラブルシューティングする
weight: 5
time: 15 minutes
---

## APM データを確認する

キャプチャした APM データの一部を確認して、アプリケーションのパフォーマンスを見てみましょう。

**APM** に移動し、**Environment** ドロップダウンを使用して環境を選択します（例：`tagging-workshop-instancename`）。

サービスのリストに `creditprocessorservice` と `creditcheckservice` が表示されているはずです：

![APM Overview](../images/apm_overview.png)

右側の **Service Map** をクリックしてサービスマップを表示します。`creditcheckservice` が `creditprocessorservice` を呼び出しており、平均応答時間が少なくとも3秒であることがわかります：

![Service Map](../images/service_map.png)

次に、右側の **Traces** をクリックして、このアプリケーションでキャプチャされたトレースを確認します。一部のトレースは比較的高速（数ミリ秒程度）に実行される一方、他のトレースは数秒かかることがわかります。

![Traces](../images/traces.png)

実行時間の長いトレースの1つをクリックします。この例では、トレースに5秒かかり、ほとんどの時間が `creditprocessorservice` の一部である `/runCreditCheck` 操作の呼び出しに費やされていることがわかります：

![Long Running Trace](../images/long_running_trace.png)

しかし、なぜ一部のトレースは遅く、他のトレースは比較的速いのでしょうか？

トレースを閉じて Trace Analyzer に戻ります。**Errors only** を `on` に切り替えると、一部のトレースにエラーがあることにも気づくでしょう：

![Traces](../images/traces_with_errors.png)

エラートレースの1つを見ると、`creditprocessorservice` が `otherservice` という別のサービスを呼び出そうとしたときにエラーが発生していることがわかります。しかし、なぜ一部のリクエストは `otherservice` への呼び出しを行い、他のリクエストは行わないのでしょうか？

![Trace with Errors](../images/error_trace.png)

一部のリクエストがなぜ遅く実行され、一部のリクエストがなぜエラーになるのかを特定するために、
トレースを1つずつ確認して問題の背後にあるパターンを見つけようとすることもできます。

**Splunk Observability Cloud** は、問題の根本原因を見つけるためのより良い方法を提供します。次にこれを確認しましょう。 

## Tag Spotlight を使用する

`credit.score.category` タグをインデックスしたので、**Tag Spotlight** と一緒に使用してアプリケーションをトラブルシューティングできます。

**APM** に移動し、右側の **Tag Spotlight** をクリックします。**Service** ドロップダウンから `creditcheckservice` サービスが選択されていることを確認します（まだ選択されていない場合）。

**Tag Spotlight** を使用すると、`impossible` のスコアになるクレジットスコアリクエストの100%にエラーがあることがわかります。一方、他のすべてのクレジットスコアタイプのリクエストにはまったくエラーがありません！

**![Tag Spotlight with Errors](../images/tag_spotlight_errors.png)**

これは **Tag Spotlight** の威力を示しています！この機能がなければ、このパターンを見つけるのは時間がかかります。数百のトレースを手動で確認してパターンを特定する必要があり（それでも見つかる保証はありません）。

エラーを確認しましたが、レイテンシはどうでしょうか？**Requests & errors distribution** ドロップダウンをクリックして **Latency distribution** に変更しましょう。

> 重要：**Cards display** の横にある設定アイコンをクリックして、P50 と P99 のメトリクスを追加します。

ここでは、`poor` クレジットスコアのリクエストが遅く実行されていることがわかります。P50、P90、P99 の時間は約3秒で、これはユーザーが待つには長すぎ、他のリクエストよりもはるかに遅いです。

また、`exceptional` クレジットスコアの一部のリクエストも遅く実行されていることがわかります。P99 の時間は約5秒ですが、P50 の応答時間は比較的速いです。

**![Tag Spotlight with Latency](../images/tag_spotlight_latency.png)**

## Dynamic Service Maps を使用する

リクエストに関連付けられたクレジットスコアカテゴリがパフォーマンスとエラー率に影響を与える可能性があることがわかったので、インデックスされたタグを活用する別の機能を確認しましょう：**Dynamic Service Maps** です。

Dynamic Service Maps を使用すると、特定のサービスをタグ別に分解できます。例えば、**APM** をクリックし、次に **Service Map** をクリックしてサービスマップを表示しましょう。

`creditcheckservice` をクリックします。次に、右側のメニューで **Breakdown** というドロップダウンをクリックし、`credit.score.category` タグを選択します。

この時点で、サービスマップは動的に更新され、`creditcheckservice` に到達するリクエストのパフォーマンスがクレジットスコアカテゴリ別に分解されて表示されます：

**![Service Map Breakdown](../images/service_map_breakdown.png)**

このビューにより、`good` と `fair` のクレジットスコアのパフォーマンスは優れている一方、`poor` と `exceptional` のスコアははるかに遅く、`impossible` のスコアはエラーになることが明確にわかります。

## 発見事項

**Tag Spotlight** により、このサービスを担当するエンジニアがさらに調査すべきいくつかの興味深いパターンが明らかになりました：

* なぜすべての `impossible` クレジットスコアリクエストがエラーになるのか？
* なぜすべての `poor` クレジットスコアリクエストが遅く実行されるのか？
* なぜ一部の `exceptional` リクエストが遅く実行されるのか？

SRE として、このコンテキストをエンジニアリングチームに伝えることは、彼らの調査に非常に役立ちます。サービスが「時々遅い」と単に伝えるよりも、はるかに迅速に問題を追跡できるからです。

興味があれば、`creditprocessorservice` のソースコードを確認してください。impossible、poor、exceptional のクレジットスコアを持つリクエストは異なる方法で処理されており、そのため我々が発見したエラー率とレイテンシの違いが生じていることがわかります。

アプリケーションで見られた動作は、モダンなクラウドネイティブアプリケーションでは一般的なものです。サービスに渡される異なる入力が異なるコードパスにつながり、その一部がパフォーマンスの低下やエラーを引き起こします。例えば、実際のクレジットチェックサービスでは、低いクレジットスコアになるリクエストは、リスクをさらに評価するために別のダウンストリームサービスに送信される場合があり、高いスコアになるリクエストよりも遅く実行されたり、より高いエラー率に遭遇したりする可能性があります。
