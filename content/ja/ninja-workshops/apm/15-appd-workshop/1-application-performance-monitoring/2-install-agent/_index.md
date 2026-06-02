---
title: 2. Java エージェントのインストール
weight: 2
description: この演習では、サーバーに SSH 接続し、Java エージェントのインストールを進めます。
---

この演習では、次のアクションを実行します。

- Java エージェントのファイルを EC2 インスタンスにアップロードします
- ファイルを特定のディレクトリに解凍します
- Java エージェントの XML 設定ファイルを更新します（任意）
- Apache Tomcat の起動スクリプトを変更し、Java エージェントを追加します

## アプリケーション VM への Java エージェントのアップロード

この時点までに、本ワークショップで使用する EC2 インスタンスに関する情報を受け取っているはずです。インスタンスへの SSH 接続に必要な、EC2 インスタンスの IP アドレス、ユーザー名、パスワードが揃っていることを確認してください。

ローカルマシンでターミナルウィンドウを開き、Java エージェントのファイルをダウンロードしたディレクトリへ移動します。次のコマンドを使用してファイルを EC2 インスタンスにアップロードします。完了までしばらく時間がかかる場合があります。

- インスタンスの IP アドレスまたはパブリック DNS を更新してください。
- ファイル名はご自身のバージョンに合わせて更新してください。

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

Java エージェントのバンドルを新しいディレクトリに解凍します。

``` bash
cd /opt/appdynamics
mkdir javaagent
cp /home/splunk/AppServerAgent-*.zip /opt/appdynamics/javaagent
cd /opt/appdynamics/javaagent
unzip AppServerAgent-*.zip
```

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
Java エージェントは Controller の Getting Started Wizard を使用して事前設定済みです。AppDynamics Portal からエージェントをダウンロードする場合は、Java エージェントの XML 設定ファイルを手動で更新する必要があります。

Java エージェントの設定プロパティを設定する主な方法は 3 つあり、優先順位は次のとおりです。

1. システム環境変数。
2. コマンドラインで渡される JVM プロパティ。
3. ```controller-info.xml``` ファイル内のプロパティ。
{{% /notice %}}

## Tomcat サーバーへの Java エージェントの追加

まず、Tomcat サーバーが稼働していないことを確認します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

次に catalina スクリプトを変更し、Java エージェント用の環境変数を設定します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
nano catalina.sh
```

125 行目（冒頭のコメントの後）に次の行を追加し、ファイルを保存します。

``` bash
export CATALINA_OPTS="$CATALINA_OPTS -javaagent:/opt/appdynamics/javaagent/javaagent.jar"
```

サーバーを再起動します。

``` bash
./startup.sh
```

Tomcat サーバーが稼働していることを確認します。数分かかる場合があります。

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
