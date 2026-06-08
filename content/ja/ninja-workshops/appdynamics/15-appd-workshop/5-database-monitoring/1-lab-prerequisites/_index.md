---
title: ラボの前提条件
time: 3 minutes
weight: 1
description: この演習では、Controller にアクセスし、アプリケーションの負荷を確認します。
---

この演習では、以下のタスクを完了します

* Web ブラウザから AppDynamics Controller にアクセスします。
* アプリケーションへのトランザクション負荷を確認します。
* 必要に応じてアプリケーションとトランザクション負荷を再起動します。

## Controller へのログイン

Cisco の認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## アプリケーションへのトランザクション負荷の確認

アプリケーションフローマップを確認します

1. **last 1 hour** の時間枠を選択します。
2. フローマップに5つの異なる Tier が表示されていることを確認します。
3. 過去1時間にわたって一貫した負荷があったことを確認します。

![Verify Load 1](images/01-prereque-appload.png)

ビジネストランザクションのリストを確認します

4. 左メニューの **Business Transactions** オプションをクリックします。
5. 以下に示す11個のビジネストランザクションが表示されていることを確認します。
6. 過去1時間にいくつかのコール数があることを確認します。

**注意:** **Calls** 列が表示されない場合は、**View Options** ツールバーボタンをクリックしてその列を表示できます。

![Verify Business transactions](images/01-prereq-bts.png)

Node のエージェントステータスを確認します

7. 左メニューの **Tiers & Nodes** オプションをクリックします。
8. **Grid View** をクリックします。
9. 各 Node の **App Agent Status** が過去1時間で90%を超えていることを確認します。

![Verify Agents](images/01-prereq-tiersnodes.png)

## 必要に応じたアプリケーションと負荷生成の再起動

前の手順で実行したチェックのいずれかが確認できなかった場合は、**Application VM** に SSH で接続し、以下の手順に従ってアプリケーションとトランザクション負荷を再起動します。

以下のコマンドを使用して、実行中の Apache Tomcat インスタンスを停止します。
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

まだ実行中のアプリケーション JVM が残っている場合は、以下のコマンドを使用して残りの JVM を終了します。

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

Tomcat サーバーを再起動します

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./startup.sh
```

2分間待ってから、以下のコマンドを使用して Apache Tomcat がポート8080で実行されていることを確認します。

``` bash
sudo netstat -tulpn | grep LISTEN
```

以下の画像のような出力が表示され、ポート8080が Apache Tomcat によって使用されていることが確認できるはずです。

![Restart App 1](images/restart-app-and-load-01.png)

以下のコマンドを使用して、アプリケーションの負荷生成を開始します。

``` bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./start_load.sh
```

以下の画像のような出力が表示されるはずです。

![Restart App 3](images/restart-app-and-load-03.png)
