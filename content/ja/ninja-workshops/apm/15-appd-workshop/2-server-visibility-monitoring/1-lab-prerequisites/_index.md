---
title: ラボの前提条件
time: 2 minutes
weight: 1
description: この演習では、Splunk AppDynamics コントローラーへのアクセス、アプリケーションへのトランザクション負荷の確認、必要に応じてアプリケーションとトランザクション負荷の再起動を行います。
draft: true
---

## コントローラーへのログイン

Cisco の認証情報を使用して、[AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## アプリケーションへのトランザクション負荷を確認する

アプリケーションのフローマップを確認します。

1. 過去 1 時間の時間枠を選択します。
2. フローマップ上で 5 つの異なる Tier が表示されていることを確認します。
3. 過去 1 時間の間に一貫した負荷があることを確認します。

![Verify App Load](images/verify-app-load-01.png)

ビジネストランザクションの一覧を確認します。

1. 左側のメニューから Business Transactions オプションをクリックします。
2. 以下に示す 11 件のビジネストランザクションが表示されていることを確認します。
3. 過去 1 時間の間に何らかの数の呼び出しがあったことを確認します。

注: Calls 列が表示されていない場合は、View Options ツールバーボタンをクリックして該当の列を表示できます。

![Verify App Load](images/verify-app-load-02.png)

ノードのエージェントステータスを確認します。

1. 左側のメニューから Tiers & Nodes オプションをクリックします。
2. Grid View をクリックします。
3. 過去 1 時間の間、各ノードの App Agent Status が 90% を超えていることを確認します。

![Verify App Load](images/verify-app-load-03.png)

## 必要に応じてアプリケーションとトランザクション負荷を再起動する

前のステップで実行したチェックのいずれかが確認できなかった場合は、Application VM に SSH 接続し、以下の手順に従ってアプリケーションとトランザクション負荷を再起動します。インスタンスへの SSH 接続に必要な EC2 インスタンスの IP アドレス、ユーザー名、パスワードが手元にあることを確認してください。ローカルマシンでターミナルを開き、以下を入力します。

``` bash
ssh -P 2222 [username]@http://[ec2-ip-address]
```

パスワードの入力を求められます。

実行中の Apache Tomcat インスタンスを停止するには、以下のコマンドを使用します。

```bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

以下のコマンドを使用して、まだ実行中のアプリケーション JVM が残っていないか確認します。

```bash
ps -ef | grep Supercar-Trader
```

実行中のアプリケーション JVM が残っている場合は、以下のコマンドを使用して残りの JVM を終了させます。

```bash
sudo pkill -f Supercar-Trader
```

アプリケーションの負荷生成を停止するには、以下のコマンドを使用します。

```bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./stop_load.sh
```

以下の画像のような出力が表示されるはずです。

![Restart App And Load](images/restart-app-and-load-02.png)

次に、以下のコマンドを使用して Apache Tomcat を起動します。

```bash
cd /usr/local/apache/apache-tomcat-9/bin
./startup.sh
```

2 分間待ってから、以下のコマンドを使用して Apache Tomcat がポート 8080 で動作していることを確認します。

```bash
sudo netstat -tulpn | grep LISTEN
```

以下の画像のような出力が表示され、ポート 8080 が Apache Tomcat によって使用されていることが示されるはずです。

![Restart App](images/restart-app-and-load-01.png)

アプリケーションの負荷生成を開始するには、以下のコマンドを使用します。

```bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./start_load.sh
```

以下の画像のような出力が表示されるはずです。

![Restart App And Load](images/restart-app-and-load-03.png)
