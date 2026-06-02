---
title: Database Collector の設定
time: 2 minutes
weight: 4
description: この演習では、コントローラーにアクセスし、Database Collector を設定し、Database Collector がデータを収集していることを確認します。
---

## Database Collector の設定

Database Agent Collector は、Database Agent 内で実行され、データベースインスタンスおよびデータベースサーバーに関するパフォーマンスメトリクスを収集するプロセスです。1 つの Collector は 1 つのデータベースインスタンスのメトリクスを収集します。1 つの Database Agent 内で複数の Collector を実行できます。Database Agent がコントローラーに接続されると、コントローラー上で 1 つ以上の Collector を設定できます。

この演習では、次のタスクを実行します。

- Web ブラウザから AppDynamics コントローラーにアクセスする
- コントローラーで Database Collector を設定する
- Database Collector がデータを収集していることを確認する

## コントローラーへのログイン

Cisco の認証情報を使用して、[AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## コントローラーでの Database Collector の設定

次の手順で、クエリリテラルの設定を変更し、Collector の設定画面に移動します。

1. 左側のメニューで **Databases** タブをクリックします。
2. 左下の **Configuration** タブをクリックします。
3. **Remove literals from the queries** のチェックボックスをオフにします。
4. **Collectors** オプションをクリックします。

![Configuration](images/05-db-configure-collector.png)

次の手順で、新しい Database Collector を設定します。

1. **Add** ボタンをクリックします。
2. データベースタイプとして **MySQL** を選択します。
3. データベースエージェントとして **DBMon-Lab-Agent** を選択し、次のパラメータを入力します。
4. Collector Name: **Supercar-MySQL-YOURINITIALS**
5. Hostname or IP Address: **localhost**
6. Listener Port: **3306**

![Configuration1](images/05-db-collector-config1.png)

1. Username: **root**
2. Password: **Welcome1!**

![Configuration2](images/05-db-username.png)

1. **Advanced Options** の下にある **Monitor Operating System** チェックボックスを選択します。
2. オペレーティングシステムとして **Linux** を選択し、次のパラメータを入力します。
3. SSH Port: **22**
4. Username: **splunk**
5. Password: **インストラクターから提供された、EC2 インスタンスへ SSH 接続するためのパスワード**
6. **OK** をクリックして Collector を保存します。

![Advance Options](images/05-db-advance-options.png)

## Database Collector がデータを収集していることの確認

Collector が実行されデータが送信されるまで 10 分間待機し、次の手順で Database Collector がデータベースに接続してデータベースメトリクスを収集していることを確認します。

1. 左側のメニューで **Databases** タブをクリックします
2. 前のセクションで作成した Collector を検索します: **Supercar-MySQL-YOURINITIALS**
3. ステータスが緑色であり、エラーが表示されていないことを確認します。
4. Supercar-MySQL のリンクをクリックして、データベースの詳細を表示します。

_注: Collector を設定してから Top 10 SQL Wait States や Queries タブの各クエリが表示されるまでに、最大 18 分かかる場合があります。_

![Application](images/04-db-db-controller.png)

![Application](images/04-db-db-dashboard.png)

Database Collector の設定について詳しくは、[こちら](https://docs.appdynamics.com/appd/24.x/latest/en/database-visibility/add-database-collectors) を参照してください
