---
title: ゲームの起動をトラブルシュートする
linkTitle: 2 Troubleshoot Game Startup
weight: 2
time: 10 minutes
---

**Splunk Observability Cloud** を使って、ゲームの起動が遅かった原因を特定しましょう。

## Splunk Observability Cloud でアプリケーションを表示する

注意: アプリケーションが初めてデプロイされたとき、データが表示されるまで数分かかる場合があります。

**APM** -> **Overview** に移動し、**Environment** ドロップダウンを使って自分の環境（例: `profiling-workshop-name`）を選択します。

すべてが正しくデプロイされていれば、サービスのリストに `doorgame` が表示されているはずです。

![APM Overview](../images/apm_overview.png)

右側の **Service Map** をクリックしてサービスマップを表示します。サービスマップ上に `doorgame` アプリケーションが表示されているはずです。

![Service Map](../images/service_map.png)

時間の大半が MySQL データベースで費やされていることに注目してください。右側の **Database Query Performance** をクリックすると、より詳細な情報を取得できます。

![Database Query Performance](../images/db_query_performance.png)

このビューでは、最も時間がかかった SQL クエリが表示されます。**Compare to** ドロップダウンが `None` に設定されていることを確認します。これにより、現在のパフォーマンスにフォーカスできます。

特に1つのクエリに長い時間がかかっていることがわかります。

```text
select * from doorgamedb.users, doorgamedb.organizations
```

（このクエリに何か特異な点はないでしょうか？）

レイテンシーグラフのスパイクの1つをクリックして、さらにトラブルシュートしてみましょう。これにより、この遅いクエリを含むトレースの例のリストが表示されます。

![Traces with Slow Query](../images/traces_with_slow_query.png)

トレースの1つをクリックすると、詳細を確認できます。

![Trace with Slow Query](../images/trace_with_slow_query.png)

トレース内では、`DoorGame.startNew` オペレーションに 25.8 秒かかり、そのうち 17.6 秒が先ほど見つけた遅い SQL クエリに関連していることがわかります。

## ここまでで実施したこと

ここまでの内容をまとめます。

* アプリケーションをデプロイし、正常にアクセスできることを確認しました
* アプリケーションは **Splunk Observability Cloud** に正常にトレースを送信しています
* 起動時間が遅い問題のトラブルシュートを開始し、根本原因と思われる遅い SQL クエリを発見しました

さらにトラブルシュートするには、JVM 内部で何が起きているかについてのより深い診断データを、メモリ（JVM ヒープ）と CPU の両面から取得することが役立ちます。次のセクションでそれに取り組みます。
