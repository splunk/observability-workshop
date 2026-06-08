---
title: Monitor and Troubleshoot - Part 1
time: 2 minutes
weight: 4
description: この演習では、データベースとサーバーの全体ダッシュボード、メインダッシュボード、およびデータベースアクティビティウィンドウのレポートを確認します。
---

## Monitor and Troubleshoot - Part 1

この演習では、以下のタスクを実行します

- Overall Database and Server Performance Dashboard の確認
- Main Database Dashboard の確認
- Database Activity Window のレポートの確認

## Overall Database and Server Performance Dashboard の確認

Overall Database and Server Performance Dashboard では、各データベースの健全性を一目で素早く確認できます。

1. Filters: 健全性、負荷、データベース内の時間、またはタイプでフィルタリングするオプションを探索できます。
2. Actions: このウィンドウのデータを .csv 形式のファイルでエクスポートします。
3. View Options: スパークチャートのオン/オフを切り替えます。
4. View: カードビューとリストビューを切り替えます。
5. Sort: ソートオプションを表示します。
6. Supercar-MySQL: メインデータベースダッシュボードにドリルインします。

![Overall Database and Server Performance Dashboard](images/04-db-collector.png)

## Main Database Dashboard の確認

メインデータベースダッシュボードでは、以下を含むデータベースの主要なインサイトが表示されます

- データベースを実行しているサーバーの健全性
- 指定された期間中の合計コール数
- 任意の時点でのコール数
- 指定された期間中の SQL ステートメント実行に費やされた合計時間
- 上位10件のクエリ待機状態
- 平均接続数
- データベースのタイプまたはベンダー
- ダッシュボードの機能を探索

1. ヘルスステータスの円をクリックして、サーバーの健全性の詳細を確認します

- 緑: サーバーは健全です。
- 黄: 警告レベルの違反があるサーバーです。
- 赤: クリティカルレベルの違反があるサーバーです。

2. データベースのタイプまたはベンダーは常にここに表示されます。
3. 指定された期間中の SQL ステートメント実行に費やされた合計時間を確認します。
4. 指定された期間中の合計実行回数を確認します。
5. チャート上の時系列にカーソルを合わせて、記録されたメトリクスの詳細を確認します。

データポイントの上部にあるオレンジの円をクリックすると、時間比較レポートが表示されます。このレポートでは、選択した時間の前後15分間のクエリ実行時間と待機状態が表示されます。

6. マウスの左ボタンをクリックしたまま、左から右にドラッグして、チャートに表示されるスパイクをハイライトします。
7. 設定ボタンをクリックして、不要な待機状態を上位10件から除外します。
8. 各待機状態のラベルにカーソルを合わせて、より詳細な説明を確認します。
9. 選択した期間中にアクティブにクエリを実行しているアクティブ接続の平均数を確認します。

![Main Database Dashboard](images/04-db-overview.png)

選択した期間のDBサーバーのOSメトリクスを表示するには

1. 右側のスクロールバーを使用してダッシュボードの一番下までスクロールします
2. CPU
3. Memory
4. Disk IO
5. Network IO

![OS Metrics](images/04-db-os-metrics.png)

## Database Activity Window のレポートの確認

Database Activity Window の Database Visibility では、最大9種類のレポートが利用可能です。利用可能なレポートは、監視対象のデータベースプラットフォームによって異なります。この演習では、最も一般的な3つのレポートを確認します。

- Wait State Report
- Top Activity Report
- Query Wait State Report

## Wait State Report

このレポートは、データベース内の Wait Events（状態）に関する時系列データを表示します。各待機状態は色分けされ、Y軸は秒単位の時間を表示します。このレポートはテーブル形式でもデータを表示し、各 SQL ステートメントの各待機状態で費やされた時間をハイライトします。

最も多くの時間を消費している待機状態は、パフォーマンスのボトルネックを示している可能性があります。例えば、db file sequential reads は、インデックスのセグメントヘッダー競合やディスク競合が原因である可能性があります。

![Wait State](images/04-db-waitstate.png)

## Top Activity Report

このレポートは、データベース内の SQL ステートメントの上位時間を時系列ビューで表示します。このレポートはテーブル形式でもデータを表示し、上位10件の SQL ステートメントそれぞれについてデータベース内で費やされた時間をハイライトします。

このレポートを使用して、どの SQL ステートメントが最も多くのデータベース時間を使用しているかを確認します。これにより、特定の SQL ステートメントがシステム全体のパフォーマンスに与える影響を判断でき、データベースパフォーマンスに最も影響を与えるステートメントにチューニングの取り組みを集中させることができます。

![Top Activity Report](images/04-db-top-activity.png)

## Query Wait State Report

このレポートは、上位（10、50、100、200）クエリの待機時間を表示します。このレポートはテーブル形式でもデータを表示し、各クエリが異なる待機状態で費やしている時間をハイライトします。列を使用して、異なる待機状態でクエリをソートできます。

Database Activity Window のレポートについての詳細は[こちら](https://help.splunk.com/en/appdynamics-on-premises/database-visibility/25.4.0/monitor-databases-and-database-servers/monitor-database-performance/database-activity-window/features-of-the-database-activity-windows)をご覧ください。

![Query Wait State Report](images/04-db-query-waitstate.png)
