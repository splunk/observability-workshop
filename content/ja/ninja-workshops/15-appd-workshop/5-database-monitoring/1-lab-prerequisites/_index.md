---
title: ラボの前提条件
time: 3 minutes
weight: 1
description: この演習では、Controller にアクセスしてアプリケーションの負荷を確認します。
---

この演習では、以下のタスクを完了します

* WebブラウザからAppDynamics Controllerにアクセスする
* アプリケーションへのトランザクション負荷を確認する
* 必要に応じてアプリケーションとトランザクション負荷を再起動する

## Controller へのログイン

Ciscoの認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## アプリケーションへのトランザクション負荷の確認

アプリケーションフローマップを確認します

1. **last 1 hour** の時間枠を選択します。
2. フローマップに5つの異なるティアが表示されていることを確認します。
3. 過去1時間にわたって一貫した負荷があったことを確認します。

![Verify Load 1](images/01-prereque-appload.png)

ビジネストランザクションのリストを確認します

1. 左メニューの **Business Transactions** オプションをクリックします。
2. 以下に示す11個のビジネストランザクションが表示されていることを確認します。
3. 過去1時間にいくらかの呼び出し回数があることを確認します。

**注意:** **Calls** 列が表示されていない場合は、**View Options** ツールバーボタンをクリックしてその列を表示できます。

![Verify Business transactions](images/01-prereq-bts.png)

ノードのエージェントステータスを確認します

1. 左メニューの **Tiers & Nodes** オプションをクリックします。
2. **Grid View** をクリックします。
3. 過去1時間の各ノードの **App Agent Status** が90%を超えていることを確認します。

![Verify Agents](images/01-prereq-tiersnodes.png)

## 必要に応じてアプリケーションと負荷生成を再起動

前のステップで行った確認のいずれかが検証できなかった場合は、**Application VM** にSSH接続し、以下の手順に従ってアプリケーションとトランザクション負荷を再起動します。

以下のコマンドを使用して、実行中のApache Tomcatインスタンスを停止します。
{{< tabs >}}
{{% tab title="Command" %}}

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

{{% /tab %}}
{{< /tabs >}}

以下のコマンドを使用して、まだ実行中のアプリケーションJVMがないか確認します。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
ps -ef | grep Supercar-Trader
```

{{% /tab %}}
{{< /tabs >}}

まだ実行中のアプリケーションJVMがある場合は、以下のコマンドを使用して残りのJVMを停止します。

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

Tomcatサーバーを再起動します

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./startup.sh
```

2分間待ってから、以下のコマンドを使用してApache Tomcatがポート8080で実行されていることを確認します。

``` bash
sudo netstat -tulpn | grep LISTEN
```

以下の画像のような出力が表示され、ポート8080がApache Tomcatによって使用されていることが確認できます。

![Restart App 1](images/restart-app-and-load-01.png)

以下のコマンドを使用して、アプリケーションの負荷生成を開始します。

``` bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./start_load.sh
```

以下の画像のような出力が表示されます。

![Restart App 3](images/restart-app-and-load-03.png)
