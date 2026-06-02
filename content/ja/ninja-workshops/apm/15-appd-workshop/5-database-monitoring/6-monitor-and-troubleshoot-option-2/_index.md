---
title: Monitor and Troubleshoot - Part 2
weight: 5
description: この演習では、Queries ダッシュボードを確認し、コストの高いクエリの詳細を確認し、コストの高いクエリのトラブルシューティングを行います。
---

## Queries ダッシュボードを確認する

Queries 画面には、データベースで最も時間を消費している SQL ステートメントとストアドプロシージャが表示されます。クエリの重み付けを SQL 待機時間などの他のメトリクスと比較することで、チューニングが必要な SQL を特定できます。

1. **Queries** タブ: queries 画面を表示します。
2. **Top Queries** ドロップダウン: 上位 5、10、100、200 件のクエリを表示します。
3. **Filter by Wait States**: 待機状態を選択して Query リストをフィルタリングできます。
4. **Group Similar**: 同じ構文のクエリをグループ化します。
5. 最大の **Weight (%)** を使用しているクエリをクリックします。
6. **View Query Details**: クエリの詳細を掘り下げます。

![Queries Dashboard](images/04-db-queries-overview.png)

## コストの高いクエリの詳細を確認する

Database Queries 画面でデータベース内で最も多くの時間を費やしているステートメントを特定したら、それらの SQL ステートメントのチューニングに役立つ詳細をさらに掘り下げることができます。データベースインスタンスの Query Details 画面には、Database Queries 画面で選択したクエリの詳細が表示されます。

1. **Resource consumption over time**: クエリがリソースを使用してデータベース内で費やした時間、実行回数、消費した CPU 時間を表示します。
2. **Wait states**: 選択した SQL ステートメントのデータベース処理にかかる時間に寄与するアクティビティです。最も時間を消費している待機状態は、パフォーマンスのボトルネックを示している可能性があります。
3. **Components Executing Similar Queries**: このクエリと類似したクエリを実行する Node を表示します。
4. **Business Transactions Executing Similar Queries**: このクエリと類似したクエリを実行する Java ビジネストランザクションを表示します。

![Expensive Query Details](images/04-db-queries-details.png)

1. 右側の外側のスクロールバーを使用して下にスクロールします。
2. **Clients**: 選択した SQL ステートメントを実行したマシンと、各マシンがステートメントの実行に要した合計時間に対する割合を表示します。
3. **Sessions**: 各データベースインスタンス使用のセッションです。
4. **Query Active in Database**: この SQL によってアクセスされたスキーマを表示します。
5. **Users**: このクエリを実行したユーザーを表示します。
6. **Query Hashcode**: クエリの一意の ID を表示します。これにより、データベースサーバーがキャッシュ内でこの SQL ステートメントをより迅速に検索できます。
7. **Query**: 選択した SQL ステートメントの構文全体を表示します。Query カードの右上にある鉛筆アイコンをクリックして、識別しやすいようにクエリ名を編集できます。
8. **Execution Plan**: クエリ実行計画ウィンドウを表示します。

![Expensive Query Details2](images/04-db-queries-details2.png)

## コストの高いクエリのトラブルシューティング

Database Query Execution Plan 画面は、クエリにとって最も効率的な実行計画を判断するのに役立ちます。問題のある可能性があるクエリを発見したら、EXPLAIN PLAN ステートメントを実行して、データベースが作成した実行計画を確認できます。

クエリの実行計画では、クエリがインデックスの使用を最適化し、効率的に実行されているかどうかが明らかになります。この情報は、実行が遅いクエリのトラブルシューティングに役立ちます。

1. **Execution Plan** タブをクリックします。
2. **Type** 列の結合タイプが各テーブルで ALL になっていることに注目してください。
3. 結合タイプの 1 つにマウスオーバーして、結合タイプの説明を確認します。
4. **Extras** 列のエントリを調べます。
5. 各エントリにマウスオーバーして、エントリの説明を確認します。

![Troubleshoot Expensive Query](images/04-db-execution-plan.png)

次に、Object Browser を使用してテーブルのインデックスを調査します。

1. **Object Browser** オプションをクリックして、テーブルのスキーマの詳細を表示します。
2. **Database** オプションをクリックします。
3. **supercars** スキーマをクリックして、テーブルのリストを展開します。
4. **CARS** テーブルをクリックして、テーブルの詳細を確認します。
5. CAR_ID 列が主キーとして定義されていることがわかります。

![Troubleshoot Expensive Query](images/04-db-object-browser.png)

1. 外側のスクロールバーを使用してページを下にスクロールします。
2. テーブルに定義された主キーインデックスに注目してください。

![Troubleshoot Car Index](images/04-db-cars-index.png)

1. **MANUFACTURER** テーブルをクリックして、その詳細を表示します。
2. **MANUFACTURER_ID** 列が主キーとして定義されていないことに注目してください。
3. ページを下にスクロールすると、テーブルにインデックスが定義されていないことがわかります。

![Troubleshoot Expensive Query](images/04-db-man-table.png)

テーブルに対するクエリのパフォーマンスを向上させるためには、MANUFACTURER_ID 列にインデックスを作成する必要があります。別のクエリを分析した場合、根本的な問題は異なるかもしれませんが、このラボで示される最も一般的な問題は、クエリが MANUFACTURER テーブルとの結合を実行しているか、そのテーブルを直接クエリしていることに起因します。
