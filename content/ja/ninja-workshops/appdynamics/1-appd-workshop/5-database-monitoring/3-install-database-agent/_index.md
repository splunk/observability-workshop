---
title: Database Agentのインストール
time: 2 minutes
weight: 3
description: この演習では、Database Visibilityエージェントをアップロードし、ダウンロードしたファイルを解凍して、Database Visibilityエージェントを起動します。
---

AppDynamics Database Agentは、データベースインスタンスとデータベースサーバーのパフォーマンスメトリクスを収集するスタンドアロンのJavaプログラムです。Java 1.8以上が動作する任意のマシンにDatabase Agentをデプロイできます。マシンはAppDynamics Controllerとモニタリング対象のデータベースインスタンスにネットワークアクセスできる必要があります。

16GBのメモリを搭載した一般的なマシンで動作するDatabase Agentは、約25のデータベースをモニタリングできます。より大きなマシンでは、最大200のデータベースをモニタリングできます。

この演習では、以下のタスクを実行します

- Database VisibilityエージェントファイルをアプリケーションVMにアップロードする
- ファイルシステム上の特定のディレクトリにファイルを解凍する
- Database Visibilityエージェントを起動する

## Database AgentをアプリケーションVMにアップロード

この時点で、このワークショップで使用するEC2インスタンスに関する情報を受け取っているはずです。EC2インスタンスのIPアドレス、インスタンスにSSH接続するために必要なユーザー名とパスワードを確認してください。

ローカルマシンでターミナルウィンドウを開き、Database AgentファイルがダウンロードされたディレクトリI移動します。以下のコマンドを使用して、ファイルをEC2インスタンスにアップロードします。完了までに時間がかかる場合があります。Windows OSの場合は、WinSCPなどのプログラムを使用する必要があるかもしれません。

- インスタンスのIPアドレスまたはパブリックDNSを更新します
- ファイル名を正確なバージョンに合わせて更新します

{{< tabs >}}
{{% tab title="コマンド" %}}

``` bash
cd ~/Downloads
scp -P 2222 db-agent-*.zip splunk@i-0267b13f78f891b64.splunk.show:/home/splunk
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
splunk@i-0267b13f78f891b64.splunk.show's password:
db-agent-25.7.0.5137.zip                                                                                                                               100%   70MB   5.6MB/s   00:12
```

{{% /tab %}}
{{< /tabs >}}

## Database Agentのインストール

Database Agentのzipファイルを解凍するディレクトリ構造を作成します。

```bash
cd /opt/appdynamics
mkdir dbagent
```

以下のコマンドを使用して、Database Agentのzipファイルをディレクトリにコピーし、ファイルを解凍します。Database Agentファイルの名前は、以下の例と若干異なる場合があります。

```bash
cp ~/db-agent-*.zip /opt/appdynamics/dbagent/
cd /opt/appdynamics/dbagent
unzip db-agent-*.zip
```

## Database Visibilityエージェントの起動

以下のコマンドを使用して、Database Agentを起動し、起動したことを確認します。

**DBエージェント名にイニシャルを追加してください**。これは次のセクションで使用します。例: DBMon-Lab-Agent-IO

```bash
cd /opt/appdynamics/dbagent
nohup java -Dappdynamics.agent.maxMetrics=300000 -Ddbagent.name=DBMon-Lab-Agent-YOURINITIALS -jar db-agent.jar &
ps -ef | grep db-agent
```

以下の画像のような出力が表示されます。

![Output](images/04-dbagent-install.png)
