---
title: ゲーム起動のトラブルシューティング
linkTitle: 2 ゲーム起動のトラブルシューティング
weight: 2
time: 10 minutes
---

**Splunk Observability Cloud** を使用して、ゲームの起動が遅かった原因を特定しましょう。

## Splunk Observability Cloud でアプリケーションを確認する

注意: アプリケーションを初めてデプロイした場合、データが表示されるまで数分かかることがあります。

**APM** -> **Overview** に移動し、**Environment** ドロップダウンを使用してご自身の環境を選択します（例: `profiling-workshop-name`）。

すべてが正しくデプロイされていれば、サービスの一覧に `doorgame` が表示されているはずです:

![APM Overview](../images/apm_overview.png)

右側の **Service Map** をクリックして、サービスマップを表示します。サービスマップ上に `doorgame` アプリケーションが表示されるはずです:

![Service Map](../images/service_map.png)

時間の大部分が MySQL データベースで費やされていることに注目してください。右側の **Database Query Performance** をクリックすると、より詳細な情報を確認できます。

![Database Query Performance](../images/db_query_performance.png)

このビューでは、最も時間がかかった SQL クエリが表示されます。現在のパフォーマンスに集中するために、**Compare to** ドロップダウンが `None` に設定されていることを確認してください。

特に時間がかかっているクエリが1つあることがわかります:

````
select * from doorgamedb.users, doorgamedb.organizations
````

（このクエリに何か異常な点に気づきましたか？）

レイテンシーグラフのスパイクの1つをクリックして、さらにトラブルシューティングを進めましょう。これにより、この遅いクエリを含むトレースの例が一覧表示されます:

![Traces with Slow Query](../images/traces_with_slow_query.png)

トレースの1つをクリックして詳細を確認します:

![Trace with Slow Query](../images/trace_with_slow_query.png)

トレースでは、`DoorGame.startNew` オペレーションに 25.8 秒かかり、そのうち 17.6 秒が先ほど見つけた遅い SQL クエリに関連していることがわかります。

## 何を達成しましたか？

ここまでの内容を振り返りましょう:

* アプリケーションをデプロイし、正常にアクセスできることを確認しました。
* アプリケーションが **Splunk Observability Cloud** にトレースを正常に送信していることを確認しました。
* アプリケーションの起動が遅い原因のトラブルシューティングを開始し、根本原因と思われる遅い SQL クエリを発見しました。

さらにトラブルシューティングを進めるには、JVM 内部で何が起きているかを、メモリ（JVM ヒープ）と CPU の両方の観点から示す、より深い診断データを取得することが役立ちます。次のセクションでこれに取り組みます。
