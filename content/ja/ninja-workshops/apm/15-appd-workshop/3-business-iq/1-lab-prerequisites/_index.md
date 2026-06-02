---
title: ラボの前提条件
time: 3 minutes
weight: 1
description: この演習では、Controllerにアクセスしてアプリケーションの負荷を確認します。
---

この演習では、次のタスクを実施します。

* Webブラウザから AppDynamics Controller にアクセスします。
* アプリケーションへのトランザクション負荷を確認します。
* 必要に応じてアプリケーションとトランザクション負荷を再起動します。

## Controllerへのログイン

[AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) に Cisco の認証情報でログインします。

## アプリケーションへのトランザクション負荷の確認

アプリケーションのフローマップを確認します。

1. **last 1 hour** の時間枠を選択します。
2. フローマップ上に 5 つの異なる Tier が表示されていることを確認します。
3. 過去 1 時間にわたって一貫した負荷が発生していることを確認します。

![Verify Load 1](images/01-prereque-appload.png)

ビジネストランザクションの一覧を確認します。

1. 左側のメニューから **Business Transactions** オプションをクリックします。
2. 以下に示す 11 個のビジネストランザクションが表示されていることを確認します。
3. 過去 1 時間に何らかのコール数が記録されていることを確認します。

**Note:** **Calls** 列が表示されていない場合は、**View Options** ツールバーボタンをクリックすると列を表示できます。

![Verify Business transactions](images/01-prereq-bts.png)

Node のエージェントステータスを確認します。

1. 左側のメニューから **Tiers & Nodes** オプションをクリックします。
2. **Grid View** をクリックします。
3. 過去 1 時間において、各 Node の **App Agent Status** が 90% を超えていることを確認します。

![Verify Agents](images/01-prereq-tiersnodes.png)

## 必要に応じたアプリケーションと負荷生成の再起動

前のステップでいずれかの確認項目が満たせなかった場合は、**Application VM** に SSH 接続し、次の手順に従ってアプリケーションとトランザクション負荷を再起動します。

実行中の Apache Tomcat インスタンスを停止するには、次のコマンドを使用します。
{{< tabs >}}
{{% tab title="Command" %}}

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

{{% /tab %}}
{{< /tabs >}}

実行中のアプリケーション JVM が残っているかを確認するには、以下のコマンドを使用します。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
ps -ef | grep Supercar-Trader
```

{{% /tab %}}
{{< /tabs >}}

実行中のアプリケーション JVM が残っていた場合は、以下のコマンドで残っている JVM を強制終了します。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo pkill -f Supercar-Trader
```

{{% /tab %}}
{{< /tabs >}}

アプリケーションの負荷生成を停止するには、以下のコマンドを使用します。すべてのプロセスが停止するまで待機してください。

``` bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./stop_load.sh
```

Tomcat サーバーを再起動します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./startup.sh
```

2 分間待ってから、以下のコマンドで Apache Tomcat がポート 8080 で稼働していることを確認します。

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

アプリケーションの負荷生成を開始するには、以下のコマンドを使用します。

``` bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./start_load.sh
```

以下の画像のような出力が表示されるはずです。

![Restart App 3](images/restart-app-and-load-03.png)
