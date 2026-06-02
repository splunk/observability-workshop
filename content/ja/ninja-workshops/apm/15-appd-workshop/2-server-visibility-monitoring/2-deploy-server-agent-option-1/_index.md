---
title: Server Agent のデプロイ - Option 1
time: 2 minutes
weight: 2
description: ご利用の AppDynamics Controller のバージョンによっては、Option 1 で示すように Controller から Server Visibility エージェントをダウンロードできる場合とできない場合があります。
draft: true
---

{{% notice title="前提条件" style="primary"  icon="lightbulb" %}}
これは Application Performance Monitoring ラボの続きです。アプリケーションが起動しており、過去 1 時間にわたって負荷がかかっていることを確認してください。必要に応じて generate-application-load セクションに戻り、ロードジェネレーターを再起動してください。
{{% /notice %}}

以下の手順を Select the agent type for download セクションまで進めてください。Servers タイルが表示されない場合は、Deploy Server Agent - Option 2 のアプローチを使用する必要があります。

Option 1 を使用する利点は、エージェントが Controller に接続するように事前構成されている点です。一方 Option 2 を使用する場合は、Controller に接続するためにエージェントの構成を編集する必要があります。

## Controller へのログイン

[AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) に Cisco の資格情報でログインします。

## Getting Started Wizard への移動

1. 画面左上の Home タブを選択します。
2. Getting Started タブを選択します。
3. Getting Started Wizard をクリックします。

![Download Wizard](images/download-wizard-01.png)

## ダウンロードするエージェントタイプの選択

1. Servers ボタンをクリックします。

![Servers](images/download-wizard-02.png)

## Server Agent のダウンロード

1. Platform Bundle は Linux と 64-bit のままにしておきます。
2. Controller connection はデフォルトのままにしておきます。
3. Click Here to Download をクリックします。

![Download](images/download-wizard-03.png)

Server Visibility Agent ファイルをローカルのワークステーションに保存します。

ブラウザは、以下の画像のように（OS によって異なります）、エージェントファイルをローカルファイルシステムに保存するよう促します。

![Save Download](images/download-wizard-04.png)

## Server Agent をアプリケーション VM にアップロード

Server エージェントファイルをアップロードするプロセスは、ワークステーションのオペレーティングシステムによって異なります。OS が MAC/Linux の場合は SCP を、Windows の場合は WinSCP を使用して Server エージェントの ZIP ファイルをコピーしてください。

## Server Agent のインストール

Server エージェントの zip ファイルを解凍するディレクトリ構造を作成します。

```bash
cd /opt/appdynamics
mkdir machineagent
```

以下のコマンドを使用して、Server Visibility エージェントの zip ファイルをディレクトリにコピーし、ファイルを解凍します。Server Visibility エージェントファイルの名前は、以下の例と若干異なる場合があります。（zip ファイルを /tmp ディレクトリにアップロードしたことを前提としています）

```bash
cp /tmp/machineagent-bundle-64bit-linux-20.4.0.2571.zip /opt/appdynamics/machineagent/
cd /opt/appdynamics/machineagent
unzip machineagent-bundle-64bit-linux-20.4.0.2571.zip
```

## Server Visibility エージェントの起動

以下のコマンドを使用して Server Visibility エージェントを起動し、起動したことを確認します。

```bash
cd /opt/appdynamics/machineagent/bin
nohup ./machine-agent &
ps -ef | grep machine
```

以下の画像のような出力が表示されるはずです。

![Install](images/svm-install-01.png)
