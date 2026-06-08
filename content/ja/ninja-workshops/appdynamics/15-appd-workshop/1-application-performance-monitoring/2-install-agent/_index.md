---
title: 2. Java エージェントのインストール
weight: 2
description: この演習では、サーバーに SSH 接続し、Java エージェントをインストールします。
---

この演習では、以下の作業を行います

- Java エージェントファイルを EC2 インスタンスにアップロードする
- ファイルを特定のディレクトリに解凍する
- Java エージェントの XML 設定ファイルを更新する（オプション）
- Apache Tomcat の起動スクリプトを変更して Java エージェントを追加する

## Java エージェントをアプリケーション VM にアップロードする

この時点で、このワークショップで使用する EC2 インスタンスに関する情報を受け取っているはずです。EC2 インスタンスの IP アドレス、インスタンスに SSH 接続するために必要なユーザー名とパスワードを確認してください。

ローカルマシンでターミナルウィンドウを開き、Java エージェントファイルをダウンロードしたディレクトリに移動します。以下のコマンドを使用して、ファイルを EC2 インスタンスにアップロードします。完了するまでに時間がかかる場合があります。

- インスタンスの IP アドレスまたはパブリック DNS を更新してください。
- ファイル名を正確なバージョンに合わせて更新してください。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
cd ~/Downloads
scp -P 2222 AppServerAgent-22.4.0.33722.zip splunk@i-0b6e3c9790292be66.splunk.show:/home/splunk
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
(splunk@44.247.206.254) Password:
AppServerAgent-22.4.0.33722.zip                                                                    100%   22MB 255.5KB/s   01:26
```

{{% /tab %}}
{{< /tabs >}}

## Java エージェントの解凍

インストラクターから割り当てられたインスタンスとパスワードを使用して、EC2 インスタンスに SSH 接続します。

``` bash
ssh -P 2222 splunk@i-0b6e3c9790292be66.splunk.show
```

Java エージェントバンドルを新しいディレクトリに解凍します。

``` bash
cd /opt/appdynamics
mkdir javaagent
cp /home/splunk/AppServerAgent-*.zip /opt/appdynamics/javaagent
cd /opt/appdynamics/javaagent
unzip AppServerAgent-*.zip
```

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
Controller の Getting Started Wizard を使用して Java エージェントを事前設定しています。AppDynamics Portal からエージェントをダウンロードした場合は、Java エージェントの XML 設定ファイルを手動で更新する必要があります。

Java エージェントの設定プロパティを設定するには、主に 3 つの方法があります。優先順位は以下の順序になります

1. システム環境変数。
2. コマンドラインで渡される JVM プロパティ。
3. ```controller-info.xml``` ファイル内のプロパティ。
{{% /notice %}}

## Tomcat サーバーに Java エージェントを追加する

まず、Tomcat サーバーが実行されていないことを確認します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

次に、catalina スクリプトを変更して、Java エージェントの環境変数を設定します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
nano catalina.sh
```

125 行目（初期コメントの後）に以下の行を追加し、ファイルを保存します。

``` bash
export CATALINA_OPTS="$CATALINA_OPTS -javaagent:/opt/appdynamics/javaagent/javaagent.jar"
```

サーバーを再起動します。

``` bash
./startup.sh
```

Tomcat サーバーが実行されていることを確認します。これには数分かかる場合があります。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
curl localhost:8080
```

{{% /tab %}}
{{% tab title="Example Output" %}}

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
