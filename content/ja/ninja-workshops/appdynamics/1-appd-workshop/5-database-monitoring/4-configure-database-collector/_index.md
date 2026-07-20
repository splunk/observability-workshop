---
title: Database Collectorの設定
time: 2 minutes
weight: 4
description: この演習では、コントローラーにアクセスし、Database Collectorを設定し、Database Collectorがデータを収集していることを確認します。
---

## Database Collectorの設定

Database Agent Collectorは、Database Agent内で実行され、データベースインスタンスとデータベースサーバーのパフォーマンスメトリクスを収集するプロセスです。1つのCollectorが1つのデータベースインスタンスのメトリクスを収集します。1つのDatabase Agentで複数のCollectorを実行できます。Database AgentがControllerに接続されると、Controller内で1つ以上のCollectorを設定できます。

この演習では、以下のタスクを実行します

- WebブラウザからAppDynamics Controllerにアクセスする
- ControllerでDatabase Collectorを設定する
- Database Collectorがデータを収集していることを確認する

## Controllerへのログイン

Ciscoの認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## ControllerでDatabase Collectorを設定する

以下の手順に従って、クエリリテラルの設定を変更し、Collector設定に移動します。

1. 左メニューの **Databases** タブをクリックします。
2. 左下の **Configuration** タブをクリックします。
3. **Remove literals from the queries** のチェックボックスをオフにします。
4. **Collectors** オプションをクリックします。

![Configuration](images/05-db-configure-collector.png)

以下の手順に従って、新しいDatabase Collectorを設定します。

1. **Add** ボタンをクリックします。
2. データベースタイプとして **MySQL** を選択します。
3. Database Agentとして **DBMon-Lab-Agent** を選択し、以下のパラメータを入力します。
4. Collector Name: **Supercar-MySQL-YOURINITIALS**
5. Hostname or IP Address: **localhost**
6. Listener Port: **3306**

![Configuration1](images/05-db-collector-config1.png)

1. Username: **root**
2. Password: **Welcome1!**

![Configuration2](images/05-db-username.png)

1. **Advanced Options** の下にある **Monitor Operating System** チェックボックスを選択します。
2. オペレーティングシステムとして **Linux** を選択し、以下のパラメータを入力します。
3. SSH Port: **22**
4. Username: **splunk**
5. Password: **インストラクターから提供されたEC2インスタンスへのSSHパスワード**
6. **OK** をクリックしてCollectorを保存します。

![Advance Options](images/05-db-advance-options.png)

## Database Collectorがデータを収集していることを確認する

Collectorが実行されデータを送信するまで10分間待ってから、以下の手順に従ってDatabase Collectorがデータベースに接続し、データベースメトリクスを収集していることを確認します。

1. 左メニューの **Databases** タブをクリックします
2. 前のセクションで作成したCollectorを検索します: **Supercar-MySQL-YOURINITIALS**
3. ステータスが緑色で、エラーが表示されていないことを確認します。
4. Supercar-MySQLリンクをクリックしてデータベースにドリルインします。

_注意: Collectorを設定してからTop 10 SQL Wait StatesやQueriesタブのクエリが表示されるまで、最大18分かかる場合があります。_

![Application](images/04-db-db-controller.png)

![Application](images/04-db-db-dashboard.png)

Database Collectorの設定について詳しくは[こちら](https://docs.appdynamics.com/appd/24.x/latest/en/database-visibility/add-database-collectors)を参照してください。
