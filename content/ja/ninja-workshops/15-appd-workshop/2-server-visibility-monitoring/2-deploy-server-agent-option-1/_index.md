---
title: Server Agent のデプロイ - オプション 1
time: 2 minutes
weight: 2
description: 使用している AppDynamics Controller のバージョンによっては、オプション1で示すように Controller から Server Visibility エージェントをダウンロードできる場合とできない場合があります。
draft: true
---

{{% notice title="前提条件" style="primary"  icon="lightbulb" %}}
このラボは Application Performance Monitoring ラボの続きです。アプリケーションが実行中であり、過去1時間にわたって負荷がかかっていることを確認してください。必要に応じて、generate-application-load セクションに戻ってロードジェネレーターを再起動してください。
{{% /notice %}}

以下のステップに従って Select the agent type for download セクションまで進み、**Servers** タイルが表示されない場合は、Deploy Server Agent - Option 2 のアプローチを使用する必要があります。

オプション1を使用する利点は、エージェントが Controller に接続するように事前設定されていることです。一方、オプション2を使用する場合は、エージェントの設定を編集して Controller に接続する必要があります。

## Controller へのログイン

Cisco の認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインしてください。

## Getting Started Wizard への移動

1. 画面左上の **Home** タブを選択します。
2. **Getting Started** タブを選択します。
3. **Getting Started Wizard** をクリックします。

![Download Wizard](images/download-wizard-01.png)

## ダウンロードするエージェントタイプの選択

1. **Servers** ボタンをクリックします。

![Servers](images/download-wizard-02.png)

## Server Agent のダウンロード

1. Platform Bundle は Linux と 64-bit のままにします。
2. Controller 接続のデフォルトを受け入れます。
3. **Click Here to Download** をクリックします。

![Download](images/download-wizard-03.png)

Server Visibility Agent ファイルをローカルワークステーションに保存します。

ブラウザがエージェントファイルをローカルファイルシステムに保存するようプロンプトを表示します。以下の画像のような表示になります（OSによって異なります）。

![Save Download](images/download-wizard-04.png)

## Application VM への Server Agent のアップロード

Server Agent ファイルのアップロードプロセスは、ワークステーションのオペレーティングシステムによって異なります。OS が MAC/Linux の場合は SCP を使用し、OS が Windows の場合は WinSCP を使用して Server Agent の ZIP ファイルをコピーしてください。

## Server Agent のインストール

Server Agent の zip ファイルを解凍するディレクトリ構造を作成します。

```bash
cd /opt/appdynamics
mkdir machineagent
```

以下のコマンドを使用して、Server Visibility Agent の zip ファイルをディレクトリにコピーし、ファイルを解凍します。Server Visibility Agent ファイルの名前は、以下の例とは若干異なる場合があります（zip ファイルを /tmp ディレクトリにアップロードしたことを前提としています）。

```bash
cp /tmp/machineagent-bundle-64bit-linux-20.4.0.2571.zip /opt/appdynamics/machineagent/
cd /opt/appdynamics/machineagent
unzip machineagent-bundle-64bit-linux-20.4.0.2571.zip
```

## Server Visibility Agent の起動

以下のコマンドを使用して、Server Visibility Agent を起動し、起動したことを確認します。

```bash
cd /opt/appdynamics/machineagent/bin
nohup ./machine-agent &
ps -ef | grep machine
```

以下の画像のような出力が表示されるはずです。

![Install](images/svm-install-01.png)
