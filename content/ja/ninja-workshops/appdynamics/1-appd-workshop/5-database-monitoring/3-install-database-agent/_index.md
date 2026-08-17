---
title: Database Agent のインストール
time: 2 minutes
weight: 3
description: この演習では、Database Visibility エージェントをアップロードし、ダウンロードしたファイルを解凍して、Database Visibility エージェントを起動します。
---

AppDynamics Database Agentは、データベースインスタンスとデータベースサーバーのパフォーマンスメトリクスを収集するスタンドアロンのJavaプログラムです。Database Agentは、Java 1.8以上が動作する任意のマシンにデプロイできます。そのマシンは、AppDynamics Controllerと監視対象のデータベースインスタンスへのネットワークアクセスが必要です。

16 GBのメモリを搭載した標準的なマシンで実行されるDatabase Agentは、約25個のデータベースを監視できます。より大きなマシンでは、Database Agentは最大200個のデータベースを監視できます。

この演習では、以下のタスクを実行します

- Database VisibilityエージェントファイルをApplication VMにアップロードする
- ファイルシステムの特定のディレクトリにファイルを解凍する
- Database Visibilityエージェントを起動する

## Application VM への Database Agent のアップロード

この時点で、このワークショップで使用するEC2インスタンスに関する情報を受け取っているはずです。EC2インスタンスのIPアドレス、SSH接続に必要なユーザー名とパスワードを確認してください。

ローカルマシンでターミナルウィンドウを開き、Database Agentファイルがダウンロードされたディレクトリに移動します。以下のコマンドを使用して、ファイルをEC2インスタンスにアップロードします。これには時間がかかる場合があります。Windows OSを使用している場合は、WinSCPなどのプログラムを使用する必要があるかもしれません。

- IPアドレスまたはパブリックDNSをインスタンスに合わせて更新してください。
- ファイル名を正確なバージョンに合わせて更新してください。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
cd ~/Downloads
scp -P 2222 db-agent-*.zip splunk@i-0267b13f78f891b64.splunk.show:/home/splunk
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
splunk@i-0267b13f78f891b64.splunk.show's password:
db-agent-25.7.0.5137.zip                                                                                                                               100%   70MB   5.6MB/s   00:12
```

{{% /tab %}}
{{< /tabs >}}

## Database Agent のインストール

Database Agentのzipファイルを解凍するディレクトリ構造を作成します。

```bash
cd /opt/appdynamics
mkdir dbagent
```

以下のコマンドを使用して、Database Agentのzipファイルをディレクトリにコピーし、ファイルを解凍します。Database Agentファイルの名前は、以下の例とは若干異なる場合があります。

```bash
cp ~/db-agent-*.zip /opt/appdynamics/dbagent/
cd /opt/appdynamics/dbagent
unzip db-agent-*.zip
```

## Database Visibility エージェントの起動

以下のコマンドを使用して、Database Agentを起動し、起動したことを確認します。

**DB エージェント名にイニシャルを追加してください**。これは次のセクションで使用します。例：DBMon-Lab-Agent-IO

```bash
cd /opt/appdynamics/dbagent
nohup java -Dappdynamics.agent.maxMetrics=300000 -Ddbagent.name=DBMon-Lab-Agent-YOURINITIALS -jar db-agent.jar &
ps -ef | grep db-agent
```

以下の画像のような出力が表示されます。

![Output](images/04-dbagent-install.png)
