---
title: ラボの前提条件
time: 3 minutes
weight: 1
description: この演習では、Controller へアクセスし、アプリケーションの負荷を確認します。
---

この演習では、以下のタスクを実施します。

* Web ブラウザから AppDynamics Controller にアクセスします。
* アプリケーションへのトランザクション負荷を確認します。
* 必要に応じて、アプリケーションとトランザクション負荷を再起動します。

## Controller へのログイン

[AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) に Cisco の資格情報でログインします。

## アプリケーションへのトランザクション負荷を確認する

アプリケーションのフローマップを確認します。

1. 時間範囲として **last 1 hour** を選択します。
2. フローマップ上で 5 つの異なる Tier が表示されていることを確認します。
3. 過去 1 時間にわたり一貫した負荷がかかっていることを確認します。

![Verify Load 1](images/01-prereque-appload.png)

ビジネストランザクションの一覧を確認します。

1. 左側のメニューの **Business Transactions** オプションをクリックします。
2. 以下に示す 11 個のビジネストランザクションが表示されていることを確認します。
3. 過去 1 時間に何らかの数の呼び出しがあることを確認します。

**Note:** **Calls** 列が表示されていない場合は、**View Options** ツールバーボタンをクリックして列を表示できます。

![Verify Business transactions](images/01-prereq-bts.png)

Node のエージェントステータスを確認します。

1. 左側のメニューの **Tiers & Nodes** オプションをクリックします。
2. **Grid View** をクリックします。
3. 過去 1 時間における各 Node の **App Agent Status** が 90% を超えていることを確認します。

![Verify Agents](images/01-prereq-tiersnodes.png)

## 必要に応じてアプリケーションと負荷生成を再起動する

前述のステップで実施したチェックのいずれかが確認できない場合は、**Application VM** に SSH 接続し、以下の手順に従ってアプリケーションとトランザクション負荷を再起動します。

実行中の Apache Tomcat インスタンスを停止するには、以下のコマンドを使用します。
{{< tabs >}}
{{% tab title="Command" %}}

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

{{% /tab %}}
{{< /tabs >}}

以下のコマンドを使用して、まだ実行中のアプリケーション JVM が残っていないか確認します。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
ps -ef | grep Supercar-Trader
```

{{% /tab %}}
{{< /tabs >}}

実行中のアプリケーション JVM が残っている場合は、以下のコマンドで残っている JVM を停止します。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo pkill -f Supercar-Trader
```

{{% /tab %}}
{{< /tabs >}}

以下のコマンドを使用して、アプリケーションの負荷生成を停止します。すべてのプロセスが停止するまで待機します。

``` bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./stop_load.sh
```

Tomcat サーバーを再起動します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./startup.sh
```

2 分間待機してから、以下のコマンドを使用して Apache Tomcat がポート 8080 で実行中であることを確認します。

``` bash
sudo netstat -tulpn | grep LISTEN
```

以下の画像のように、ポート 8080 が Apache Tomcat により使用されていることを示す出力が表示されるはずです。

![Restart App 1](images/restart-app-and-load-01.png)

以下のコマンドを使用して、アプリケーションの負荷生成を開始します。

``` bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./start_load.sh
```

以下の画像のような出力が表示されるはずです。

![Restart App 3](images/restart-app-and-load-03.png)
