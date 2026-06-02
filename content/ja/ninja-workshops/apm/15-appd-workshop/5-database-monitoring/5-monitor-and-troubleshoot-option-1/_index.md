---
title: Monitor and Troubleshoot - Part 1
time: 2 minutes
weight: 4
description: この演習では、データベースとサーバー全体のダッシュボードを確認し、メインのダッシュボードを確認し、データベースアクティビティウィンドウのレポートを確認します。
---

## Monitor and Troubleshoot - Part 1

この演習では、以下のタスクを実行します。

- Overall Database and Server Performance Dashboard を確認する
- Main Database Dashboard を確認する
- Database Activity Window のレポートを確認する

## Overall Database and Server Performance Dashboard を確認する

Overall Database and Server Performance Dashboard を使用すると、各データベースの健全性を一目で素早く確認できます。

1. Filters: ヘルス、負荷、データベース内の時間、またはタイプによってフィルタリングするオプションを探索できます。
2. Actions: このウィンドウのデータを .csv 形式のファイルにエクスポートします。
3. View Options: スパークチャートのオン/オフを切り替えます。
4. View: カードビューとリストビューを切り替えます。
5. Sort: 並べ替えオプションを表示します。
6. Supercar-MySQL: メインのデータベースダッシュボードにドリルダウンします。

![Overall Database and Server Performance Dashboard](images/04-db-collector.png)

## Main Database Dashboard を確認する

メインのデータベースダッシュボードでは、以下を含むデータベースの主要な情報を確認できます。

- データベースを実行しているサーバーの健全性。
- 指定された期間中のコールの総数。
- 任意の時点のコール数。
- 指定された期間中に SQL ステートメントの実行に費やされた合計時間。
- 上位 10 件のクエリ待機状態。
- 平均接続数。
- データベースのタイプまたはベンダー。
- ダッシュボードの機能を探索します。

1. ヘルスステータスの円をクリックして、サーバーの健全性の詳細を確認します。

- Green: サーバーは正常です。
- Yellow: 警告レベルの違反があるサーバー。
- Red: 重大レベルの違反があるサーバー。

1. データベースのタイプまたはベンダーは常にここに表示されます。
2. 指定された期間中に SQL ステートメントの実行に費やされた合計時間を確認します。
3. 指定された期間中の実行の総数を確認します。
4. チャートの時系列にカーソルを合わせると、記録されたメトリクスの詳細を確認できます。

データポイントの上部にあるオレンジ色の円をクリックすると、選択した時刻の 15 分前から 15 分後までのクエリ実行時間と待機状態を示す時間比較レポートが表示されます。

1. マウスの左ボタンを押したまま左から右にドラッグして、チャートで見られるスパイクをハイライトします。
2. 設定ボタンをクリックして、不要な待機状態を上位 10 件から除外します。
3. 各待機状態のラベルにカーソルを合わせると、より詳細な説明が表示されます。
4. 選択した期間中にクエリを実行している、アクティブな接続の平均数を確認します。

![Main Database Dashboard](images/04-db-overview.png)

選択した期間の DB サーバーの OS メトリクスを表示するには、以下を行います。

1. 右側のスクロールバーを使ってダッシュボードの一番下までスクロールします
2. CPU
3. Memory
4. Disk IO
5. Network IO

![OS Metrics](images/04-db-os-metrics.png)

## Database Activity Window のレポートを確認する

Database Visibility の Database Activity Window では、最大 9 種類の異なるレポートを利用できます。利用可能なレポートは、監視対象のデータベースプラットフォームによって異なります。この演習では、最も一般的な 3 つのレポートを確認します。

- Wait State Report
- Top Activity Report
- Query Wait State Report

## Wait State Report

このレポートは、データベース内の Wait Events (states) の時系列データを表示します。それぞれ異なる待機は色分けされ、Y 軸には秒単位の時間が表示されます。このレポートでは、データを表形式でも表示し、各 SQL ステートメントの各待機状態に費やされた時間をハイライト表示します。

最も時間を消費している待機状態は、パフォーマンスのボトルネックを示している可能性があります。たとえば、db file sequential reads は、インデックスのセグメントヘッダー競合やディスク競合によって発生する可能性があります。

![Wait State](images/04-db-waitstate.png)

## Top Activity Report

このレポートは、データベース内で時間を要している上位の SQL ステートメントを時系列ビューで表示します。このレポートでは、データを表形式でも表示し、上位 10 件の SQL ステートメントごとにデータベース内で費やされた時間をハイライト表示します。

このレポートを使用して、どの SQL ステートメントが最も多くのデータベース時間を使用しているかを確認します。これにより、特定の SQL ステートメントがシステム全体のパフォーマンスに与える影響を判断でき、データベースパフォーマンスへの影響が最も大きいステートメントにチューニング作業を集中させることができます。

![Top Activity Report](images/04-db-top-activity.png)

## Query Wait State Report

このレポートは、上位 (10、50、100、200) のクエリの待機時間を表示します。このレポートでは、データを表形式でも表示し、各クエリがさまざまな待機状態に費やしている時間をハイライト表示します。列を使って、異なる待機状態でクエリを並べ替えることができます。

Database Activity Window のレポートの詳細については、[こちら](https://help.splunk.com/en/appdynamics-on-premises/database-visibility/25.4.0/monitor-databases-and-database-servers/monitor-database-performance/database-activity-window/features-of-the-database-activity-windows) を参照してください。

![Query Wait State Report](images/04-db-query-waitstate.png)
