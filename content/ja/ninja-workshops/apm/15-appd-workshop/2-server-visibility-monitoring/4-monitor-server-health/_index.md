---
title: サーバーヘルスの監視
time: 2 minutes
weight: 4
description: この演習では、サーバーのヘルスを監視するためのいくつかのダッシュボードを確認し、サーバーとアプリケーションのコンテキスト間を移動します。
---

この演習では、以下のタスクを完了します。

- Server Main ダッシュボードの確認
- Server Processes ダッシュボードの確認
- Server Volumes ダッシュボードの確認
- Server Network ダッシュボードの確認
- サーバーとアプリケーションのコンテキスト間の移動

## Server Main ダッシュボードの確認

Machine agent をインストールしたので、Server Visibility モジュールで利用可能ないくつかの機能を見ていきましょう。**Application Dashboard** から **Servers** タブをクリックし、以下の手順でサーバーのメインダッシュボードへドリルダウンします。

1. 左メニューの **Servers** タブをクリックします。
2. サーバーの左側の **checkbox** をオンにします。
3. **View Details** をクリックします。

![Server Dashboard](images/svm-viewDetails.png)

これでサーバーダッシュボードを確認できます。このダッシュボードでは、以下のタスクを実行できます。

選択した監視対象サーバーの主要なパフォーマンスメトリクスのチャートを確認できます。含まれる項目は以下のとおりです。

- サーバーの可用性
- CPU、メモリ、ネットワーク使用率
- サーバーのプロパティ
- ディスク、パーティション、ボリュームのメトリクス
- CPU リソースとメモリを最も消費している上位 10 のプロセス

Server Main ダッシュボードの詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-dashboard)を参照してください。

ダッシュボードの **Top Pane** を確認すると、以下の情報が表示されます。

- Host Id: Splunk AppDynamics Controller 内でサーバーを一意に識別する ID です
- Health: サーバーの全体的なヘルス状態を表示します。
- Hierachy: サーバーをグループ化するための任意の階層構造です。詳細についてはドキュメント[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/machine-agent/configure-the-machine-agent/machine-agent-configuration-properties)を参照してください

1. ヘルスサーバーアイコンをクリックすると、**Violations * Anomalies** パネルが表示されます。パネルを確認して潜在的な問題を特定します
2. **Current Health Rule Evaluation Status** をクリックして、このサーバーで現在アラートが発生している問題があるかどうかを確認します

![Server Health](images/server-health.png)
![Server violations](images/server-health-violations.png)

1. **CPU Usage too high** ルールをクリックします
2. **Edit Health Rule** をクリックします。**Edit Health Rule** パネルが開きます

![Edit Health Rule](images/server-edit-hr.png)

このパネルでは Health Rule を設定できます。Health Rule の作成とカスタマイズの詳細については別のラボで扱います。ここでは既存のルールを確認するだけです

1. **Warning Criteria** をクリックします

![Edit Health Rule - Warning](images/server-warning.png)

この例では、CPU が 5% を超えると警告基準が設定されていることがわかります。これが Health Rule が healthy 状態ではなく warning を表示している理由です。**Edit Health Rule** パネルをキャンセルして **Server Dashboard** に戻ります

## Server Processes ダッシュボードの確認

1. **Processes** タブをクリックします。
2. **View Options** をクリックして、異なるデータ列を選択します。表示可能な KPI を確認します

これで Server Processes ダッシュボードを確認できます。このダッシュボードでは、以下のタスクを実行できます。

- 選択した期間中にアクティブだったすべてのプロセスを表示します。プロセスは ServerMonitoring.yml ファイルで指定されたクラスごとにグループ化されます。
- Command Line 列のプロセスエントリにマウスオーバーすることで、このプロセスを開始した完全なコマンドラインを表示します。
- プロセスクラスを展開して、そのクラスに関連付けられたプロセスを表示します。
- View Options を使用して、チャートに表示する列を構成します。
- 表示されるメトリクスの期間を変更します。
- 列をソートキーとしてチャートをソートします。スパークラインチャート（CPU Trend と Memory Trend）はソートできません。
- CPU とメモリの使用傾向を一目で確認します。

Server Processes ダッシュボードの詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-process-metrics)を参照してください。

![Dashboard Processes](images/server-process-dashboard.png)

## Server Volumes ダッシュボードの確認

1. **Volumes** タブをクリックします。

これで Server Volumes ダッシュボードを確認できます。このダッシュボードでは、以下のタスクを実行できます。

- ボリュームのリスト、使用率、ディスク・パーティション・ボリュームで利用可能な合計ストレージスペースを確認します。
- ディスク使用量と I/O 使用率、レート、1 秒あたりの操作数、待機時間を確認します。
- 収集および表示されるメトリクスの期間を変更します。
- チャート上の任意のポイントをクリックして、その時点のメトリクス値を確認します。

Server Volumes ダッシュボードの詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-volumes-metrics)を参照してください。

![Dashboard Example](images/server-volumes.png)

## Server Network ダッシュボードの確認

1. Network タブをクリックします。

これで **Server Network** ダッシュボードを確認できます。このダッシュボードでは、以下のタスクを実行できます。

- 各ネットワークインターフェイスの MAC、IPv4、IPv6 アドレスを確認します。
- ネットワークインターフェイスが有効かつ機能しているか、その動作状態（イーサネットケーブルが接続されているか、全二重または半二重モードで動作しているか）、最大転送単位（MTU）またはネットワークインターフェイスが転送できる最大プロトコルデータユニットのサイズ（バイト単位）、イーサネット接続の速度（Mbit/sec）を確認します。
- ネットワークスループット（kilobytes/sec）とパケットトラフィックを表示します。
- 表示されるメトリクスの期間を変更します。
- チャート上の任意のポイントにマウスオーバーして、その時点のメトリクス値を確認します。

Server Network ダッシュボードの詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-network-metrics)を参照してください。

![Network Dashboard](images/server-network.png)
