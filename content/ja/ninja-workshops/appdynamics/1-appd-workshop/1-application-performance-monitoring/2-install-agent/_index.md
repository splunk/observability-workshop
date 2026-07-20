---
title: 2. Java Agentのインストール
weight: 2
description: この演習では、サーバーにSSH接続し、Java agentをインストールします。
---

この演習では、以下の作業を行います。

- Java agentファイルをEC2インスタンスにアップロードする
- ファイルを特定のディレクトリに解凍する
- Java agentのXML設定ファイルを更新する（オプション）
- Apache Tomcatの起動スクリプトを変更してJava agentを追加する

## Java AgentをアプリケーションVMにアップロード

この時点で、このワークショップで使用するEC2インスタンスの情報を受け取っているはずです。EC2インスタンスのIPアドレス、インスタンスにSSH接続するために必要なユーザー名とパスワードを確認してください。

ローカルマシンでターミナルウィンドウを開き、Java agentファイルをダウンロードしたディレクトリに移動します。以下のコマンドを使用して、ファイルをEC2インスタンスにアップロードします。完了までに時間がかかる場合があります。

- インスタンスのIPアドレスまたはパブリックDNSを更新します
- ファイル名を正確なバージョンに合わせて更新します

{{< tabs >}}
{{% tab title="コマンド" %}}

``` bash
cd ~/Downloads
scp -P 2222 AppServerAgent-22.4.0.33722.zip splunk@i-0b6e3c9790292be66.splunk.show:/home/splunk
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
(splunk@44.247.206.254) Password:
AppServerAgent-22.4.0.33722.zip                                                                    100%   22MB 255.5KB/s   01:26
```

{{% /tab %}}
{{< /tabs >}}

## Java Agentの解凍

インストラクターから割り当てられたインスタンスとパスワードを使用して、EC2インスタンスにSSH接続します。

``` bash
ssh -P 2222 splunk@i-0b6e3c9790292be66.splunk.show
```

Java agentバンドルを新しいディレクトリに解凍します。

``` bash
cd /opt/appdynamics
mkdir javaagent
cp /home/splunk/AppServerAgent-*.zip /opt/appdynamics/javaagent
cd /opt/appdynamics/javaagent
unzip AppServerAgent-*.zip
```

{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}
ControllerのGetting Started Wizardを使用してJava agentを事前設定しています。AppDynamics PortalからAgentをダウンロードした場合は、Java agentのXML設定ファイルを手動で更新する必要があります。

Java agentの設定プロパティを設定するには、主に3つの方法があります。以下の順序で優先されます。

1. システム環境変数
2. コマンドラインで渡されるJVMプロパティ
3. ```controller-info.xml``` ファイル内のプロパティ
{{% /notice %}}

## Java AgentをTomcatサーバーに追加

まず、Tomcatサーバーが実行されていないことを確認します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

次に、catalinaスクリプトを変更して、Java agentの環境変数を設定します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
nano catalina.sh
```

125行目（初期コメントの後）に以下の行を追加し、ファイルを保存します。

``` bash
export CATALINA_OPTS="$CATALINA_OPTS -javaagent:/opt/appdynamics/javaagent/javaagent.jar"
```

サーバーを再起動します。

``` bash
./startup.sh
```

Tomcatサーバーが実行されていることを確認します。数分かかる場合があります。

{{< tabs >}}
{{% tab title="コマンド" %}}

``` bash
curl localhost:8080
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Apache Tomcat/9.0.50</title>
        <link href="favicon.ico" rel="icon" type="image/x-icon" />
        <link href="tomcat.css" rel="stylesheet" type="text/css" />
    </head>

    <body>
        <div id="wrapper"
....
```

{{% /tab %}}
{{< /tabs >}}
