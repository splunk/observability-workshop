---
title: アプリケーション起動の遅延を修正する
linkTitle: 4 アプリケーション起動の遅延を修正する
weight: 4
time: 10 minutes
---

このセクションでは、**Splunk Observability Cloud** のプロファイリングデータから学んだことを活用して、アプリケーション起動時に発生した遅延を解決します。

### ソースコードの確認

対応するソースファイル（`~/workshop/profiling/doorgame/src/main/java/com/splunk/profiling/workshop/UserData.java`）をもう一度開き、以下のコードに注目してください。

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

データベースエンジニアに相談したところ、実行されている SQL クエリにデカルト結合が含まれていることがわかりました。

````
select * FROM DoorGameDB.Users, DoorGameDB.Organizations
````

デカルト結合は非常に遅いことで知られており、一般的に使用すべきではありません。

さらに調査を進めると、ユーザーテーブルには 10,000 行、組織テーブルには 1,000 行あることがわかりました。これら2つのテーブルでデカルト結合を実行すると、10,000 x 1,000 行、つまり 10,000,000 行が返されることになります！

さらに、ユーザーテーブルの各レコードが各組織に対して繰り返されるため、クエリは重複したユーザーデータを返すことになります。

したがって、コードがこのクエリを実行すると、10,000,000 個のユーザーオブジェクトを HashMap にロードしようとします。これが実行に非常に時間がかかり、大量のヒープメモリを消費する理由です。

### バグを修正しましょう

このコードを最初に書いたエンジニアに相談したところ、Organizations テーブルとの結合は意図しないものだったことが判明しました。

そのため、ユーザーを HashMap にロードする際に、クエリからこのテーブルを削除するだけで済みます。

対応するソースファイル（`./doorgame/src/main/java/com/splunk/profiling/workshop/UserData.java`）をもう一度開き、以下のコード行を変更します。

``` java
    static final String SELECT_QUERY = "select * FROM DoorGameDB.Users, DoorGameDB.Organizations";
```

以下のように変更します。

``` java
    static final String SELECT_QUERY = "select * FROM DoorGameDB.Users";
```

これにより、メソッドの実行速度が大幅に向上し、正しい数のユーザー（10,000,000 ではなく 10,000）を HashMap にロードするため、メモリ使用量も削減されます。

### アプリケーションの再ビルドと再デプロイ

以下のコマンドを使用して、Door Game アプリケーションを再ビルドおよび再デプロイし、変更をテストしましょう。

``` bash
cd ~/workshop/profiling
./5-redeploy-doorgame.sh
```

アプリケーションの再デプロイが正常に完了したら、The Door Game に再度アクセスして修正が適用されていることを確認します。
`http://<your IP address>:81`

`Let's Play` をクリックすると、以前よりも早くゲームに移動できるはずです（パフォーマンスにはまだ改善の余地がありますが）。

![Choose Door](../images/door_game_choose_door.png)

ゲームをさらに数回開始してから、**Splunk Observability Cloud** に戻り、`GET new-game` オペレーションのレイテンシーが減少したことを確認しましょう。

## 達成したこと

* SQL クエリが遅かった原因を発見しました。
* 修正を適用し、アプリケーションを再ビルドして再デプロイしました。
* アプリケーションがより速く新しいゲームを開始できるようになったことを確認しました。

次のセクションでは、引き続きゲームをプレイし、残りのパフォーマンスの問題を見つけて修正していきます。
