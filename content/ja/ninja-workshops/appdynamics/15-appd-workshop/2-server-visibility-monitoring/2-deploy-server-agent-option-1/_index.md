---
title: Deploy Server Agent - Option 1
time: 2 minutes
weight: 2
description: 使用している AppDynamics Controller のバージョンによって、Option 1 で示すように Controller から Server Visibility エージェントをダウンロードできる場合とできない場合があります。
draft: true
---

{{% notice title="前提条件" style="primary"  icon="lightbulb" %}}
これは Application Performance Monitoring ラボの続きです。アプリケーションが実行中で、過去1時間にわたって負荷がかかっていることを確認してください。必要に応じて、generate-application-load セクションに戻ってロードジェネレーターを再起動してください。
{{% /notice %}}

以下の手順に従って「Select the agent type for download」セクションまで進んでください。Servers タイルが表示されない場合は、Deploy Server Agent - Option 2 のアプローチを使用する必要があります。

Option 1 を使用する利点は、エージェントがコントローラーに接続するように事前設定されることです。一方、Option 2 を使用する場合は、エージェントの設定を編集してコントローラーに接続する必要があります。

## Controller にログイン

Cisco の認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## Getting Started Wizard に移動

1. 画面左上の Home タブを選択します。
2. Getting Started タブを選択します。
3. Getting Started Wizard をクリックします。

![Download Wizard](images/download-wizard-01.png)

## ダウンロードするエージェントタイプを選択

1. Servers ボタンをクリックします。

![Servers](images/download-wizard-02.png)

## Server Agent をダウンロード

1. Platform Bundle は Linux および 64-bit のままにします。
2. Controller 接続のデフォルト値をそのまま使用します。
3. Click Here to Download をクリックします。

![Download](images/download-wizard-03.png)

Server Visibility Agent ファイルをローカルワークステーションに保存します。

ブラウザーがエージェントファイルをローカルファイルシステムに保存するよう求めるプロンプトが表示されます。以下の画像のようになります（OS によって異なります）。

![Save Download](images/download-wizard-04.png)

## Server Agent をアプリケーション VM にアップロード

Server エージェントファイルのアップロード方法は、ワークステーションのオペレーティングシステムによって異なります。OS が MAC/Linux の場合は SCP を使用し、OS が Windows の場合は WinSCP を使用して、Server エージェントの ZIP ファイルをコピーしてください。

## Server Agent をインストール

Server エージェントの zip ファイルを解凍するディレクトリ構造を作成します。

```bash
cd /opt/appdynamics
mkdir machineagent
```

以下のコマンドを使用して、Server Visibility エージェントの zip ファイルをディレクトリにコピーし、解凍します。Server Visibility エージェントファイルの名前は、以下の例と若干異なる場合があります。（zip ファイルを /tmp ディレクトリにアップロードしたことを前提としています）

```bash
cp /tmp/machineagent-bundle-64bit-linux-20.4.0.2571.zip /opt/appdynamics/machineagent/
cd /opt/appdynamics/machineagent
unzip machineagent-bundle-64bit-linux-20.4.0.2571.zip
```

## Server Visibility エージェントを起動

以下のコマンドを使用して、Server Visibility エージェントを起動し、起動したことを確認します。

```bash
cd /opt/appdynamics/machineagent/bin
nohup ./machine-agent &
ps -ef | grep machine
```

以下の画像のような出力が表示されるはずです。

![Install](images/svm-install-01.png)
