---
title: サーバーの正常性をモニタリングする
time: 2 minutes
weight: 4
description: この演習では、サーバーの正常性をモニタリングするためのダッシュボードを確認し、サーバーとアプリケーションのコンテキスト間を移動します。
---

この演習では、以下のタスクを完了します。

- Server Mainダッシュボードを確認する
- Server Processesダッシュボードを確認する
- Server Volumesダッシュボードを確認する
- Server Networkダッシュボードを確認する
- サーバーとアプリケーションのコンテキスト間を移動する

## Server Mainダッシュボードを確認する

Machine agentがインストールされたので、Server Visibilityモジュールで利用可能な機能を確認しましょう。 **Application Dashboard** から **Servers** タブをクリックし、以下の手順でサーバーのメインダッシュボードにドリルインします。

1. 左メニューの **Servers** タブをクリックします。
2. サーバーの左側にある **チェックボックス** をオンにします。
3. **View Details** をクリックします。

![Server Dashboard](images/svm-viewDetails.png)

サーバーダッシュボードを確認できます。このダッシュボードでは以下のタスクを実行できます。

選択したモニタリング対象サーバーの主要なパフォーマンスメトリクスのチャートを表示します。以下が含まれます。  

- サーバーの可用性
- CPU、メモリ、およびネットワーク使用率
- サーバープロパティ
- ディスク、パーティション、およびボリュームのメトリクス
- CPUリソースとメモリを消費する上位10プロセス

Server Mainダッシュボードの詳細は[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-dashboard)を参照してください。

ダッシュボードの **Top Pane** を確認します。以下の情報が表示されます。

- Host Id: Splunk AppDynamics Controllerに固有のサーバーIDです
- Health: サーバーの全体的な正常性を表示します
- Hierachy: サーバーをグループ化するための任意の階層です。詳細はドキュメントの[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/machine-agent/configure-the-machine-agent/machine-agent-configuration-properties)を参照してください

1. サーバーのヘルスアイコンをクリックして **Violations * Anomalies** パネルを表示します。パネルを確認して潜在的な問題を特定します
2. **Current Health Rule Evaluation Status** をクリックして、このサーバーで現在アラートが発生している問題がないか確認します

![Server Health](images/server-health.png)
![Server violations](images/server-health-violations.png)

1. **CPU Usage too high** ルールをクリックします
2. **Edit Health Rule** をクリックします。 **Edit Health Rule** パネルが開きます

![Edit Health Rule](images/server-edit-hr.png)

このパネルでは正常性ルールを設定できます。正常性ルールの作成とカスタマイズの詳細については、別のラボで説明します。ここでは既存のルールを確認するだけにします。

1. **Warning Criteria** をクリックします

![Edit Health Rule - Warning](images/server-warning.png)

この例では、CPUが5%を超えた場合に警告条件が設定されていることがわかります。これが正常性ルールが正常状態ではなく警告を表示している理由です。 **Edit Health Rule** パネルをキャンセルして **Server Dashboard** に戻ります。

## Server Processesダッシュボードを確認する

1. **Processes** タブをクリックします。
2. **View Options** をクリックして、異なるデータ列を選択します。表示可能なKPIを確認します。

サーバープロセスダッシュボードを確認できます。このダッシュボードでは以下のタスクを実行できます。

- 選択した期間中にアクティブなすべてのプロセスを表示します。プロセスはServerMonitoring.ymlファイルで指定されたクラスごとにグループ化されます。
- Command Line列のプロセスエントリにカーソルを合わせると、そのプロセスを開始した完全なコマンドラインを表示できます。
- プロセスクラスを展開して、そのクラスに関連するプロセスを表示します。
- View Optionsを使用して、チャートに表示する列を設定します。
- 表示するメトリクスの期間を変更します。
- 列をソートキーとしてチャートをソートします。スパークラインチャート（CPU TrendとMemory Trend）ではソートできません。
- CPUとメモリの使用傾向を一目で確認します。

Server Processesダッシュボードの詳細は[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-process-metrics)を参照してください。

![Dashboard Processes](images/server-process-dashboard.png)

## Server Volumesダッシュボードを確認する

1. **Volumes** タブをクリックします。

サーバーボリュームダッシュボードを確認できます。このダッシュボードでは以下のタスクを実行できます。

- ボリュームのリスト、使用率、およびディスク、パーティション、またはボリュームで利用可能な合計ストレージ容量を表示します。
- ディスク使用量とI/O使用率、レート、1秒あたりの操作数、および待機時間を表示します。
- 収集および表示するメトリクスの期間を変更します。
- チャート上の任意のポイントをクリックして、その時点のメトリクス値を表示します。

Server Volumesダッシュボードの詳細は[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-volumes-metrics)を参照してください。

![Dashboard Example](images/server-volumes.png)

## Server Networkダッシュボードを確認する

1. **Network** タブをクリックします。

**Server Network** ダッシュボードを確認できます。このダッシュボードでは以下のタスクを実行できます。

- 各ネットワークインターフェースのMAC、IPv4、およびIPv6アドレスを表示します。
- ネットワークインターフェースが有効で機能しているかどうか、動作状態、イーサネットケーブルが接続されているか、全二重または半二重モードで動作しているか、最大転送単位（MTU）またはネットワークインターフェースが通過できる最大プロトコルデータユニットのサイズ（バイト単位）、イーサネット接続速度（Mbit/sec）を表示します。
- ネットワークスループット（kilobytes/sec）およびパケットトラフィックを表示します。
- 表示するメトリクスの期間を変更します。
- チャート上の任意のポイントにカーソルを合わせて、その時点のメトリクス値を表示します。

Server Networkダッシュボードの詳細は[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/server-network-metrics)を参照してください。

![Network Dashboard](images/server-network.png)
