---
title: BRUM ラボ前提条件
time: 2 minutes
weight: 1
description: この演習では、Controller にアクセスし、アプリケーションの負荷を確認します。
---

この演習では、以下のタスクを完了します。

* Web ブラウザから AppDynamics Controller にアクセスします。
* アプリケーションへのトランザクション負荷を確認します。
* 必要に応じてアプリケーションとトランザクション負荷を再起動します。

## Controller へのログイン

Cisco の認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## アプリケーションへのトランザクション負荷の確認

アプリケーションのフローマップを確認します。

1. **last 1 hour** の時間範囲を選択します。
2. フローマップ上に 5 つの異なる Tier が表示されていることを確認します。
3. 過去 1 時間にわたって安定した負荷があったことを確認します。

![Verify Load 1](images/01-prereque-appload.png)

ビジネストランザクションのリストを確認します。

1. 左側のメニューから **Business Transactions** オプションをクリックします。
2. 以下に示す 11 個のビジネストランザクションが表示されていることを確認します。
3. 過去 1 時間にいくつかの呼び出しが行われていることを確認します。

**Note:** **Calls** カラムが表示されていない場合は、**View Options** ツールバーボタンをクリックしてそのカラムを表示できます。

![Verify Business transactions](images/01-prereq-bts.png)

Node のエージェントステータスを確認します。

1. 左側のメニューから **Tiers & Nodes** オプションをクリックします。
2. **Grid View** をクリックします。
3. 各 Node の **App Agent Status** が過去 1 時間において 90% 以上であることを確認します。

![Verify Agents](images/01-prereq-tiersnodes.png)

## 必要に応じてアプリケーションと負荷生成を再起動する

前のステップで実行した確認のいずれかが検証できなかった場合は、**Application VM** に SSH 接続し、以下の手順に従ってアプリケーションとトランザクション負荷を再起動します。

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

まだ実行中のアプリケーション JVM が残っている場合は、以下のコマンドを使用して残りの JVM を強制終了します。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo pkill -f Supercar-Trader
```

{{% /tab %}}
{{< /tabs >}}

以下のコマンドを使用して、アプリケーションの負荷生成を停止します。すべてのプロセスが停止するまで待ちます。

``` bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./stop_load.sh
```

Tomcat サーバーを再起動します。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./startup.sh
```

2 分間待ってから、以下のコマンドを使用して Apache Tomcat がポート 8080 で実行されていることを確認します。

``` bash
sudo netstat -tulpn | grep LISTEN
```

以下の画像のような出力が表示され、ポート 8080 が Apache Tomcat によって使用されていることが確認できます。

![Restart App 1](images/restart-app-and-load-01.png)

以下のコマンドを使用して、アプリケーションの負荷生成を開始します。

``` bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./start_load.sh
```

以下の画像のような出力が表示されます。

![Restart App 3](images/restart-app-and-load-03.png)
