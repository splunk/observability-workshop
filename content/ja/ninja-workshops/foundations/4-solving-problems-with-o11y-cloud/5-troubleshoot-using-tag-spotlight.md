---
title: Tag Spotlightを使用した問題のトラブルシューティング
linkTitle: 5. Tag Spotlightを使用した問題のトラブルシューティング
weight: 5
time: 15 minutes
---

## APMデータの探索

キャプチャしたAPMデータを探索して、アプリケーションのパフォーマンスを確認しましょう。

**APM** に移動し、 **Environment** ドロップダウンから自分の環境（例: `tagging-workshop-instancename`）を選択します。

サービスのリストに `creditprocessorservice` と `creditcheckservice` が表示されます。

![APM Overview](../images/apm_overview.png)

右側の **Service Map** をクリックしてサービスマップを表示します。`creditcheckservice` が `creditprocessorservice` を呼び出しており、平均応答時間が少なくとも3秒であることがわかります。

![Service Map](../images/service_map.png)

次に、右側の **Traces** をクリックして、このアプリケーションでキャプチャされたトレースを確認します。一部のトレースは比較的高速（数ミリ秒程度）ですが、数秒かかるものもあることがわかります。

![Traces](../images/traces.png)

実行時間が長いトレースの1つをクリックします。この例では、トレースに5秒かかっており、ほとんどの時間が `creditprocessorservice` の一部である `/runCreditCheck` オペレーションの呼び出しに費やされていることがわかります。

![Long Running Trace](../images/long_running_trace.png)

しかし、なぜ一部のトレースは遅く、他のトレースは比較的速いのでしょうか？

トレースを閉じてTrace Analyzerに戻ります。 **Errors only** を `on` に切り替えると、一部のトレースにエラーがあることもわかります。

![Traces](../images/traces_with_errors.png)

エラーのあるトレースの1つを見ると、`creditprocessorservice` が `otherservice` という別のサービスを呼び出そうとしたときにエラーが発生していることがわかります。しかし、なぜ一部のリクエストは `otherservice` への呼び出しが発生し、他のリクエストでは発生しないのでしょうか？

![Trace with Errors](../images/error_trace.png)

一部のリクエストがなぜ遅いのか、またなぜ一部のリクエストがエラーになるのかを特定するには、トレースを1つずつ確認して問題のパターンを見つける方法があります。

**Splunk Observability Cloud** には、問題の根本原因を見つけるためのより良い方法があります。次にそれを見ていきましょう。

## Tag Spotlightの使用

`credit.score.category` タグをインデックス化したので、 **Tag Spotlight** を使用してアプリケーションのトラブルシューティングを行うことができます。

**APM** に移動し、右側の **Tag Spotlight** をクリックします。 **Service** ドロップダウンから `creditcheckservice` サービスが選択されていることを確認します（まだ選択されていない場合）。

**Tag Spotlight** を使用すると、スコアが `impossible` となるクレジットスコアリクエストの100%がエラーになっている一方、他のすべてのクレジットスコアタイプのリクエストにはエラーがまったくないことがわかります。

**![Tag Spotlight with Errors](../images/tag_spotlight_errors.png)**

これが **Tag Spotlight** の威力です！このパターンを見つけるのは、Tag Spotlightなしでは時間がかかります。何百ものトレースを手動で確認してパターンを特定する必要があり、それでも見つけられる保証はありません。

エラーについて確認しましたが、レイテンシーはどうでしょうか？ **Requests & errors distribution** ドロップダウンをクリックして **Latency distribution** に変更しましょう。

> IMPORTANT: **Cards display** の横にある設定アイコンをクリックして、P50とP99のメトリクスを追加します。

ここでは、`poor` クレジットスコアのリクエストが遅く実行されており、P50、P90、P99の時間が約3秒であることがわかります。これはユーザーが待つには長すぎる時間であり、他のリクエストよりもはるかに遅いです。

また、`exceptional` クレジットスコアのリクエストの一部も遅く実行されており、P99の時間が約5秒ですが、P50の応答時間は比較的速いことがわかります。

**![Tag Spotlight with Latency](../images/tag_spotlight_latency.png)**

## Dynamic Service Mapsの使用

リクエストに関連するクレジットスコアカテゴリがパフォーマンスとエラー率に影響を与えることがわかったので、インデックス化されたタグを活用するもう1つの機能、 **Dynamic Service Maps** を探索しましょう。

Dynamic Service Mapsでは、タグによって特定のサービスを分解できます。例えば、 **APM** をクリックし、次に **Service Map** をクリックしてサービスマップを表示します。

`creditcheckservice` をクリックします。次に、右側のメニューで **Breakdown** と表示されているドロップダウンをクリックし、`credit.score.category` タグを選択します。

この時点で、サービスマップが動的に更新され、`creditcheckservice` に到達するリクエストのパフォーマンスがクレジットスコアカテゴリ別に分解されて表示されます。

**![Service Map Breakdown](../images/service_map_breakdown.png)**

このビューにより、`good` と `fair` のクレジットスコアのパフォーマンスは優れている一方、`poor` と `exceptional` のスコアははるかに遅く、`impossible` のスコアはエラーになることが明確にわかります。

## 調査結果

**Tag Spotlight** により、このサービスを所有するエンジニアがさらに調査すべきいくつかの興味深いパターンが明らかになりました。

* なぜすべての `impossible` クレジットスコアリクエストがエラーになるのか？
* なぜすべての `poor` クレジットスコアリクエストが遅く実行されるのか？
* なぜ一部の `exceptional` リクエストが遅く実行されるのか？

SREとして、このコンテキストをエンジニアリングチームに渡すことは、調査に非常に役立ちます。単にサービスが「時々遅い」と伝えるよりも、はるかに迅速に問題を追跡できるようになります。

興味がある場合は、`creditprocessorservice` のソースコードを確認してください。impossible、poor、exceptionalのクレジットスコアを持つリクエストは異なる方法で処理されているため、発見したエラー率とレイテンシーの違いが生じていることがわかります。

アプリケーションで確認した動作は、最新のクラウドネイティブアプリケーションに典型的なものです。サービスに渡される異なる入力が異なるコードパスにつながり、一部はパフォーマンスの低下やエラーを引き起こします。例えば、実際のクレジットチェックサービスでは、低いクレジットスコアのリクエストはリスクをさらに評価するために別の下流サービスに送信される場合があり、高いスコアのリクエストよりも遅くなったり、エラー率が高くなったりする可能性があります。
