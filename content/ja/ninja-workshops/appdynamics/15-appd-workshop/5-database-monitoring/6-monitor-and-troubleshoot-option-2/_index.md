---
title: Monitor and Troubleshoot - Part 2
weight: 5
description: この演習では、クエリダッシュボードの確認、高負荷クエリの詳細の確認、および高負荷クエリのトラブルシューティングを行います。
---

## クエリダッシュボードの確認

Queries ウィンドウには、データベースで最も多くの時間を消費している SQL 文とストアドプロシージャが表示されます。クエリの重みを SQL 待機時間などの他のメトリクスと比較して、チューニングが必要な SQL を特定できます。

1. **Queries** タブ: クエリウィンドウを表示します。
2. **Top Queries** ドロップダウン: 上位 5、10、100、または 200 のクエリを表示します。
3. **Filter by Wait States**: 待機状態を選択してクエリリストをフィルタリングできます。
4. **Group Similar**: 同じ構文を持つクエリをグループ化します。
5. 最大の **Weight (%)** を使用しているクエリをクリックします。
6. **View Query Details**: クエリの詳細にドリルダウンします。

![Queries Dashboard](images/04-db-queries-overview.png)

## 高負荷クエリの詳細の確認

Database Queries ウィンドウでデータベースで最も多くの時間を費やしている文を特定したら、それらの SQL 文のチューニングに役立つ詳細情報をさらに深く掘り下げることができます。データベースインスタンスの Query Details ウィンドウには、Database Queries ウィンドウで選択したクエリの詳細が表示されます。

1. **Resource consumption over time**: クエリがリソースを使用してデータベースで費やした時間、実行回数、消費された CPU 時間が表示されます。
2. **Wait states**: 選択した SQL 文をデータベースが処理するのにかかる時間に寄与するアクティビティです。最も多くの時間を消費している待機状態は、パフォーマンスのボトルネックを示している可能性があります。
3. **Components Executing Similar Queries**: このクエリと類似したクエリを実行するノードを表示します。
4. **Business Transactions Executing Similar Queries**: このクエリと類似したクエリを実行する Java ビジネストランザクションを表示します。

![Expensive Query Details](images/04-db-queries-details.png)

1. 右側の外側のスクロールバーを使用して下にスクロールします。
2. **Clients**: 選択した SQL 文を実行したマシンと、各マシンが実行した文の合計時間に対する割合を表示します。
3. **Sessions**: 各データベースインスタンスの使用セッションです。
4. **Query Active in Database**: この SQL がアクセスしたスキーマを表示します。
5. **Users**: このクエリを実行したユーザーを表示します。
6. **Query Hashcode**: データベースサーバーがキャッシュ内のこの SQL 文をより迅速に見つけるためのクエリの一意の ID を表示します。
7. **Query**: 選択した SQL 文の完全な構文を表示します。Query カードの右上隅にある鉛筆アイコンをクリックして、識別しやすいようにクエリ名を編集できます。
8. **Execution Plan**: クエリ実行プランウィンドウを表示します。

![Expensive Query Details2](images/04-db-queries-details2.png)

## 高負荷クエリのトラブルシューティング

Database Query Execution Plan ウィンドウは、クエリの最も効率的な実行プランを決定するのに役立ちます。問題のある可能性のあるクエリを発見したら、EXPLAIN PLAN 文を実行して、データベースが作成した実行プランを確認できます。

クエリの実行プランは、クエリがインデックスの使用を最適化し、効率的に実行されているかどうかを明らかにします。この情報は、実行速度が遅いクエリのトラブルシューティングに役立ちます。

1. **Execution Plan** タブをクリックします。
2. **Type** 列の結合タイプが各テーブルで ALL になっていることを確認します。
3. 結合タイプの 1 つにカーソルを合わせて、結合タイプの説明を確認します。
4. **Extras** 列のエントリを確認します。
5. 各エントリにカーソルを合わせて、エントリの説明を確認します。

![Troubleshoot Expensive Query](images/04-db-execution-plan.png)

次に、Object Browser を使用してテーブルのインデックスを調査しましょう。

5. **Object Browser** オプションをクリックして、テーブルのスキーマの詳細を表示します。
6. **Database** オプションをクリックします。
7. **supercars** スキーマをクリックして、テーブルのリストを展開します。
8. **CARS** テーブルをクリックして、テーブルの詳細を確認します。
9. CAR_ID 列がプライマリキーとして定義されていることが確認できます。

![Troubleshoot Expensive Query](images/04-db-object-browser.png)

10. 外側のスクロールバーを使用してページを下にスクロールします。
11. テーブルに定義されたプライマリキーインデックスを確認します。

![Troubleshoot Car Index](images/04-db-cars-index.png)

12. **MANUFACTURER** テーブルをクリックして、その詳細を表示します。
13. **MANUFACTURER_ID** 列がプライマリキーとして定義されていないことを確認します。
14. ページを下にスクロールして、テーブルにインデックスが定義されていないことを確認します。

![Troubleshoot Expensive Query](images/04-db-man-table.png)

MANUFACTURER_ID 列には、テーブルに対するクエリのパフォーマンスを向上させるためにインデックスを作成する必要があります。別のクエリを分析した場合、根本的な問題は異なる可能性がありますが、このラボで示される最も一般的な問題は、クエリが MANUFACTURER テーブルとの結合を実行しているか、そのテーブルを直接クエリしていることが原因です。
