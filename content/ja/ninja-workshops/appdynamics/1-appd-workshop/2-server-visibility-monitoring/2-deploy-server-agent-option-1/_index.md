---
title: Deploy Server Agent - Option 1
time: 2 minutes
weight: 2
description: 使用しているAppDynamics Controllerのバージョンによっては、Option 1で示すようにControllerからServer Visibilityエージェントをダウンロードできない場合があります。
draft: true
---

{{% notice title="前提条件" style="primary"  icon="lightbulb" %}}
このラボはApplication Performance Monitoringラボの続きです。アプリケーションが実行中で、過去1時間の負荷があることを確認してください。必要に応じて、generate-application-loadセクションに戻り、ロードジェネレーターを再起動してください。
{{% /notice %}}

以下の手順に従い、Select the agent type for downloadセクションまで進みます。Serversタイルが表示されない場合は、Deploy Server Agent - Option 2の方法を使用する必要があります。

Option 1を使用する利点は、エージェントがControllerに接続するための設定が事前に構成されることです。Option 2を使用する場合は、エージェントの設定を編集してControllerに接続する必要があります。

## Controllerへのログイン

Ciscoの認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## Getting Started Wizardへの移動

1. 画面左上の **Home** タブを選択します。
2. **Getting Started** タブを選択します。
3. **Getting Started Wizard** をクリックします。

![Download Wizard](images/download-wizard-01.png)

## ダウンロードするエージェントタイプの選択

1. **Servers** ボタンをクリックします。

![Servers](images/download-wizard-02.png)

## Server Agentのダウンロード

1. Platform Bundleは **Linux** および **64-bit** のままにします。
2. Controller接続のデフォルト値を受け入れます。
3. **Click Here to Download** をクリックします。

![Download](images/download-wizard-03.png)

Server Visibilityエージェントファイルをローカルワークステーションに保存します。

ブラウザがエージェントファイルをローカルファイルシステムに保存するよう促します。以下の画像のように表示されます（OSによって異なります）。

![Save Download](images/download-wizard-04.png)

## Server AgentをアプリケーションVMにアップロード

Serverエージェントファイルのアップロード手順は、ワークステーションのオペレーティングシステムによって異なります。MAC/Linuxの場合はSCPを使用し、Windowsの場合はWinSCPを使用して、ServerエージェントのZIPファイルをコピーします。

## Server Agentのインストール

Serverエージェントのzipファイルを解凍するディレクトリ構造を作成します。

```bash
cd /opt/appdynamics
mkdir machineagent
```

以下のコマンドを使用して、Server Visibilityエージェントのzipファイルをディレクトリにコピーし、解凍します。Server Visibilityエージェントのファイル名は以下の例と若干異なる場合があります（zipファイルを/tmpディレクトリにアップロードした前提です）。

```bash
cp /tmp/machineagent-bundle-64bit-linux-20.4.0.2571.zip /opt/appdynamics/machineagent/
cd /opt/appdynamics/machineagent
unzip machineagent-bundle-64bit-linux-20.4.0.2571.zip
```

## Server Visibilityエージェントの起動

以下のコマンドを使用して、Server Visibilityエージェントを起動し、正常に起動したことを確認します。

```bash
cd /opt/appdynamics/machineagent/bin
nohup ./machine-agent &
ps -ef | grep machine
```

以下の画像のような出力が表示されます。

![Install](images/svm-install-01.png)
