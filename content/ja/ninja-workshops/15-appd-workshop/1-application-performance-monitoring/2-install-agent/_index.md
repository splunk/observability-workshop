---
title: 2. Java Agent のインストール
weight: 2
description: この演習では、サーバーに SSH 接続し、Java エージェントをインストールします。
---

この演習では、以下のアクションを実行します：

- JavaエージェントファイルをEC2インスタンスにアップロードする
- ファイルを特定のディレクトリに解凍する
- JavaエージェントのXML設定ファイルを更新する（オプション）
- Apache Tomcatの起動スクリプトを変更してJavaエージェントを追加する

## Application VM への Java Agent のアップロード

この時点で、このワークショップで使用するEC2インスタンスに関する情報を受け取っているはずです。EC2インスタンスのIPアドレス、インスタンスにSSH接続するために必要なユーザー名とパスワードを確認してください。

ローカルマシンでターミナルウィンドウを開き、Javaエージェントファイルがダウンロードされたディレクトリに移動します。以下のコマンドを使用してファイルをEC2インスタンスにアップロードします。これには時間がかかる場合があります。

- インスタンスのIPアドレスまたはパブリックDNSを更新してください。
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

## Java Agent の解凍

インストラクターから割り当てられたインスタンスとパスワードを使用してEC2インスタンスにSSH接続します。

``` bash
ssh -P 2222 splunk@i-0b6e3c9790292be66.splunk.show
```

Javaエージェントバンドルを新しいディレクトリに解凍します。

``` bash
cd /opt/appdynamics
mkdir javaagent
cp /home/splunk/AppServerAgent-*.zip /opt/appdynamics/javaagent
cd /opt/appdynamics/javaagent
unzip AppServerAgent-*.zip
```

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
ControllerのGetting Started Wizardを使用してJavaエージェントを事前設定しました。AppDynamics Portalからエージェントをダウンロードした場合は、JavaエージェントのXML設定ファイルを手動で更新する必要があります。

Javaエージェントの設定プロパティを設定するには、主に3つの方法があります。これらは以下の順序で優先されます：

1. システム環境変数
2. コマンドラインで渡されるJVMプロパティ
3. ```controller-info.xml``` ファイル内のプロパティ
{{% /notice %}}

## Tomcat Server への Java Agent の追加

まず、Tomcatサーバーが実行されていないことを確認します

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

次に、catalinaスクリプトを変更してJavaエージェントの環境変数を設定します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
nano catalina.sh
```

125行目（最初のコメントの後）に以下の行を追加してファイルを保存します

``` bash
export CATALINA_OPTS="$CATALINA_OPTS -javaagent:/opt/appdynamics/javaagent/javaagent.jar"
```

サーバーを再起動します

``` bash
./startup.sh
```

Tomcatサーバーが実行されていることを確認します。これには数分かかる場合があります

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
