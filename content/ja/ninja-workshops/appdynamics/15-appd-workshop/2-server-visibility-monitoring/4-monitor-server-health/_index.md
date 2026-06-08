---
title: サーバーヘルスの監視
time: 2 minutes
weight: 4
description: この演習では、サーバーヘルスを監視するためのいくつかのダッシュボードを確認し、サーバーとアプリケーションのコンテキスト間を移動します。
---

この演習では、以下のタスクを完了します

- Server Main ダッシュボードの確認
- Server Processes ダッシュボードの確認
- Server Volumes ダッシュボードの確認
- Server Network ダッシュボードの確認
- サーバーとアプリケーションのコンテキスト間の移動

## Server Main ダッシュボードの確認

Machine agent がインストールされたので、Server Visibility モジュールで利用可能な機能のいくつかを見てみましょう。**Application Dashboard** から **Servers** タブをクリックし、以下の手順に従ってサーバーメインダッシュボードにドリルインします。

1. 左メニューの **Servers** タブをクリックします。
2. サーバーの左側にある**チェックボックス**にチェックを入れます。
3. **View Details** をクリックします。

![Server Dashboard](images/svm-viewDetails.png)

サーバーダッシュボードを確認できます。このダッシュボードでは、以下のタスクを実行できます

選択した監視対象サーバーの主要パフォーマンスメトリクスのチャートを表示します。以下が含まれます  

- サーバーの可用性
- CPU、メモリ、およびネットワーク使用率
- サーバープロパティ
- ディスク、パーティション、およびボリュームのメトリクス
- CPU リソースとメモリを消費している上位 10 プロセス

Server Main ダッシュボードの詳細については、[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-dashboard)をご覧ください。

ダッシュボードの **Top Pane** を確認します。以下の情報が提供されます

- Host Id: Splunk AppDynamics Controller に固有のサーバー ID です
- Health: サーバーの全体的なヘルス状態を表示します
- Hierachy: サーバーをグループ化するための任意の階層です。詳細については、[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/machine-agent/configure-the-machine-agent/machine-agent-configuration-properties)のドキュメントを参照してください

1. ヘルスサーバーアイコンをクリックして **Violations * Anomalies** パネルを表示します。パネルを確認して潜在的な問題を特定します
2. **Current Health Rule Evaluation Status** をクリックして、このサーバーで現在アラートが発生している問題があるかどうかを確認します

![Server Health](images/server-health.png)
![Server violations](images/server-health-violations.png)

3. **CPU Usage too high** ルールをクリックします
4. **Edit Health Rule** をクリックします。これにより **Edit Health Rule** パネルが開きます

![Edit Health Rule](images/server-edit-hr.png)

このパネルでは、Health Rule を設定できます。別のラボで Health Rule の作成とカスタマイズについてより詳しく説明します。ここでは既存のルールを確認するだけにします

5. **Warning Criteria** をクリックします

![Edit Health Rule - Warning](images/server-warning.png)

この例では、CPU が 5% を超えた場合に警告基準が設定されていることがわかります。これが、Health Rule が正常な状態ではなく警告を表示している理由です。**Edit Health Rule** パネルからキャンセルして **Server Dashboard** に戻ります

## Server Processes ダッシュボードの確認

1. **Processes** タブをクリックします。
2. **View Options** をクリックして、異なるデータ列を選択します。表示可能な KPI を確認します

サーバープロセスダッシュボードを確認できます。このダッシュボードでは、以下のタスクを実行できます

- 選択した期間中にアクティブなすべてのプロセスを表示します。プロセスは ServerMonitoring.yml ファイルで指定されたクラスごとにグループ化されます。
- Command Line 列のプロセスエントリにカーソルを合わせると、そのプロセスを開始した完全なコマンドラインを表示できます。
- プロセスクラスを展開して、そのクラスに関連するプロセスを確認します。
- View Options を使用して、チャートに表示する列を設定します。
- 表示されるメトリクスの期間を変更します。
- 列をソートキーとしてチャートをソートします。スパークラインチャート（CPU Trend と Memory Trend）ではソートできません。
- CPU とメモリの使用傾向を一目で確認します。

Server Processes ダッシュボードの詳細については、[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-process-metrics)をご覧ください。

![Dashboard Processes](images/server-process-dashboard.png)

## Server Volumes ダッシュボードの確認

1. **Volumes** タブをクリックします。

サーバーボリュームダッシュボードを確認できます。このダッシュボードでは、以下のタスクを実行できます

- ボリュームのリスト、使用率、およびディスク、パーティション、またはボリュームで利用可能な合計ストレージ容量を確認します。
- ディスク使用量と I/O 使用率、レート、1 秒あたりの操作数、および待機時間を確認します。
- 収集および表示されるメトリクスの期間を変更します。
- チャート上の任意のポイントをクリックして、その時点のメトリクス値を確認します。

Server Volumes ダッシュボードの詳細については、[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-volumes-metrics)をご覧ください。

![Dashboard Example](images/server-volumes.png)

## Server Network ダッシュボードの確認

1. Network タブをクリックします。

**Server Network** ダッシュボードを確認できます。このダッシュボードでは、以下のタスクを実行できます

- 各ネットワークインターフェースの MAC、IPv4、および IPv6 アドレスを確認します。
- ネットワークインターフェースが有効かどうか、機能しているかどうか、イーサネットケーブルが接続された動作状態、全二重または半二重デュプレックスモードでの動作、最大転送単位（MTU）またはネットワークインターフェースが渡すことができる最大プロトコルデータユニットのサイズ（バイト単位）、イーサネット接続速度（Mbit/sec）を確認します。
- ネットワークスループット（kilobytes/sec）とパケットトラフィックを表示します。
- 表示されるメトリクスの期間を変更します。
- チャート上の任意のポイントにカーソルを合わせて、その時点のメトリクス値を確認します。

Server Network ダッシュボードの詳細については、[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-network-metrics)をご覧ください。

![Network Dashboard](images/server-network.png)
