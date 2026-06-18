---
title: アプリケーション起動の遅延を修正する
linkTitle: 4 アプリケーション起動の遅延を修正する
weight: 4
time: 10 minutes
---

このセクションでは、**Splunk Observability Cloud** のプロファイリングデータから学んだことを活用して、アプリケーション起動時に発生した遅延を解決します。

### ソースコードの調査

対応するソースファイル（`~/workshop/profiling/doorgame/src/main/java/com/splunk/profiling/workshop/UserData.java`）を再度開き、以下のコードに注目してください

````
public class UserData {

    static final String DB_URL = "jdbc:mysql://mysql/DoorGameDB";
    static final String USER = "root";
    static final String PASS = System.getenv("MYSQL_ROOT_PASSWORD");
    static final String SELECT_QUERY = "select * FROM DoorGameDB.Users, DoorGameDB.Organizations";

    HashMap<String, User> users;

    public UserData() {
        users = new HashMap<String, User>();
    }

    public void loadUserData() {

        // Load user data from the database and store it in a map
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try{
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            stmt = conn.createStatement();
            rs = stmt.executeQuery(SELECT_QUERY);
            while (rs.next()) {
                User user = new User(rs.getString("UserId"), rs.getString("FirstName"), rs.getString("LastName"));
                users.put(rs.getString("UserId"), user);
            }
````

データベースエンジニアに確認したところ、実行されている SQL クエリにデカルト結合が含まれていることが判明しました

````
select * FROM DoorGameDB.Users, DoorGameDB.Organizations
````

デカルト結合は非常に遅いことで知られており、一般的に使用すべきではありません。

さらに調査を進めると、ユーザーテーブルには 10,000 行、組織テーブルには 1,000 行あることがわかりました。これら2つのテーブルでデカルト結合を実行すると、10,000 x 1,000 行、つまり 10,000,000 行が返されることになります！

さらに、ユーザーテーブルの各レコードが各組織に対して繰り返されるため、クエリは重複したユーザーデータを返すことになります。

したがって、コードがこのクエリを実行すると、10,000,000 個のユーザーオブジェクトを HashMap にロードしようとするため、実行に非常に時間がかかり、大量のヒープメモリを消費する理由が説明できます。

### バグを修正する

このコードを最初に書いたエンジニアに相談したところ、Organizations テーブルとの結合は意図しないものであったことが判明しました。

したがって、ユーザーを HashMap にロードする際に、クエリからこのテーブルを削除するだけで済みます。

対応するソースファイル（`./doorgame/src/main/java/com/splunk/profiling/workshop/UserData.java`）を再度開き、以下のコード行を変更してください

``` java
    static final String SELECT_QUERY = "select * FROM DoorGameDB.Users, DoorGameDB.Organizations";
```

以下のように変更します

``` java
    static final String SELECT_QUERY = "select * FROM DoorGameDB.Users";
```

これにより、メソッドの実行が大幅に高速化され、正しい数のユーザーが HashMap にロードされるため（10,000,000 ではなく 10,000）、使用メモリも削減されます。

### アプリケーションの再ビルドと再デプロイ

以下のコマンドを使用して Door Game アプリケーションを再ビルドおよび再デプロイし、変更をテストしましょう

``` bash
cd ~/workshop/profiling
./5-redeploy-doorgame.sh
```

アプリケーションが正常に再デプロイされたら、修正が適用されていることを確認するために再度 The Door Game にアクセスしてください
`http://<your IP address>:81`

`Let's Play` をクリックすると、以前よりも速くゲームに移動できるはずです（まだパフォーマンスの改善の余地はありますが）

![Choose Door](../images/door_game_choose_door.png)

さらに数回ゲームを開始してから、**Splunk Observability Cloud** に戻り、`GET new-game` オペレーションのレイテンシーが減少していることを確認してください。

## 何を達成しましたか？

* SQL クエリが遅い理由を発見しました。
* 修正を適用し、アプリケーションを再ビルドして再デプロイしました。
* アプリケーションが新しいゲームをより速く開始できることを確認しました。

次のセクションでは、引き続きゲームをプレイし、見つかった残りのパフォーマンスの問題を修正します。
