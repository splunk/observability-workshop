---
title: AlwaysOn Profiling の有効化
linkTitle: 3 AlwaysOn Profiling の有効化
weight: 3
time: 20 minutes
---

メモリプロファイラと CPU プロファイラを有効にし、動作を確認し、Splunk Observability Cloud で結果を使用してアプリケーションの起動が遅い原因を特定する方法を学びましょう。

### アプリケーション設定の更新

両方のプロファイラを有効にするために、Splunk OpenTelemetry Java エージェントに追加の設定引数を渡す必要があります。設定の詳細は[こちらに記載されています](https://docs.splunk.com/observability/en/gdi/get-data-in/application/java/instrumentation/instrument-java-application.html#activate-alwayson-profiling)が、現時点では以下の設定のみが必要です

````
SPLUNK_PROFILER_ENABLED="true"
SPLUNK_PROFILER_MEMORY_ENABLED="true"
````

アプリケーションは Kubernetes にデプロイされているため、Kubernetes マニフェストファイルを更新してこれらの環境変数を設定できます。`doorgame/doorgame.yaml` ファイルを編集用に開き、以下の環境変数の値が "true" に設定されていることを確認してください

```` yaml
- name: SPLUNK_PROFILER_ENABLED
  value: "true"
- name: SPLUNK_PROFILER_MEMORY_ENABLED
  value: "true"
````

次に、以下のコマンドを実行して Door Game アプリケーションを再デプロイしましょう

``` bash
cd ~/workshop/profiling
kubectl apply -f doorgame/doorgame.yaml
```

数秒後、更新されたアプリケーション設定で新しい Pod がデプロイされます。

### 動作確認

プロファイラが有効になっていることを確認するために、以下のコマンドでアプリケーションログを確認しましょう

```` bash
kubectl logs -l app=doorgame --tail=100 | grep JfrActivator
````

アプリケーションログの出力に、プロファイラがアクティブであることを示す行が表示されるはずです

```` log
[otel.javaagent 2024-02-05 19:01:12:416 +0000] [main] INFO com.splunk.opentelemetry.profiler.JfrActivator - Profiler is active.```
````

これにより、プロファイラが有効になり、Kubernetes クラスターにデプロイされた OpenTelemetry コレクターにデータを送信していることが確認できます。コレクターはプロファイリングデータを Splunk Observability Cloud に転送します。

### APM でのプロファイリング

`http://<your IP address>:81` にアクセスし、The Door Game を数回プレイしてください。

次に Splunk Observability Cloud に戻り、**APM** -> **Trace analyzer** をクリックします。

`doorgame` サービスと `GET new-game` オペレーションに関連するトレースでフィルタリングします（ゲームの起動シーケンスのトラブルシューティングを行っているため）

![New Game Traces](../images/new_game_traces.png)

これらのトレースの1つを選択すると、以下の画面が表示されます

![Trace with Call Stacks](../images/trace_with_call_stacks.png)

スパンに「Call Stacks」が含まれていることがわかります。これは、先ほど CPU プロファイリングとメモリプロファイリングを有効にした結果です。

`doorgame: SELECT doorgamedb` という名前のスパンをクリックし、右側の CPU stack traces をクリックします

![Trace with CPU Call Stacks](../images/trace_with_cpu_call_stacks.png)

プロファイラによってキャプチャされた CPU コールスタックが表示されます。

CPU スタックトレースをより詳細に確認するために、AlwaysOn Profiler を開きましょう。`View in AlwaysOn Profiler` の横にある `Span` リンクをクリックします

![Flamegraph and table](../images/flamegraph_and_table.png)

AlwaysOn Profiler にはテーブルと[フレームグラフ](https://www.brendangregg.com/flamegraphs.html)の両方が含まれています。以下の操作を行って、このビューを探索してみてください

* テーブルのアイテムをクリックして、フレームグラフの変化を確認する
* スタックフレームをクリックしてズームイン、親フレームをクリックしてズームアウトして、フレームグラフをナビゲートする
* `splunk` や `jetty` などの検索語を追加して、一致するスタックフレームをハイライトする

`DoorGame.startNew` メソッドから始まるスタックトレースを詳しく見てみましょう（これがリクエストの最も遅い部分であることは既にわかっています）

````
com.splunk.profiling.workshop.DoorGame.startNew(DoorGame.java:24)
com.splunk.profiling.workshop.UserData.loadUserData(UserData.java:33)
com.mysql.cj.jdbc.StatementImpl.executeQuery(StatementImpl.java:1168)
com.mysql.cj.NativeSession.execSQL(NativeSession.java:655)
com.mysql.cj.protocol.a.NativeProtocol.sendQueryString(NativeProtocol.java:998)
com.mysql.cj.protocol.a.NativeProtocol.sendQueryPacket(NativeProtocol.java:1065)
com.mysql.cj.protocol.a.NativeProtocol.readAllResults(NativeProtocol.java:1715)
com.mysql.cj.protocol.a.NativeProtocol.read(NativeProtocol.java:1661)
com.mysql.cj.protocol.a.TextResultsetReader.read(TextResultsetReader.java:48)
com.mysql.cj.protocol.a.TextResultsetReader.read(TextResultsetReader.java:87)
com.mysql.cj.protocol.a.NativeProtocol.read(NativeProtocol.java:1648)
com.mysql.cj.protocol.a.ResultsetRowReader.read(ResultsetRowReader.java:42)
com.mysql.cj.protocol.a.ResultsetRowReader.read(ResultsetRowReader.java:75)
com.mysql.cj.protocol.a.MultiPacketReader.readMessage(MultiPacketReader.java:44)
com.mysql.cj.protocol.a.MultiPacketReader.readMessage(MultiPacketReader.java:66)
com.mysql.cj.protocol.a.TimeTrackingPacketReader.readMessage(TimeTrackingPacketReader.java:41)
com.mysql.cj.protocol.a.TimeTrackingPacketReader.readMessage(TimeTrackingPacketReader.java:62)
com.mysql.cj.protocol.a.SimplePacketReader.readMessage(SimplePacketReader.java:45)
com.mysql.cj.protocol.a.SimplePacketReader.readMessage(SimplePacketReader.java:102)
com.mysql.cj.protocol.a.SimplePacketReader.readMessageLocal(SimplePacketReader.java:137)
com.mysql.cj.protocol.FullReadInputStream.readFully(FullReadInputStream.java:64)
java.io.FilterInputStream.read(Unknown Source:0)
sun.security.ssl.SSLSocketImpl$AppInputStream.read(Unknown Source:0)
sun.security.ssl.SSLSocketImpl.readApplicationRecord(Unknown Source:0)
sun.security.ssl.SSLSocketInputRecord.bytesInCompletePacket(Unknown Source:0)
sun.security.ssl.SSLSocketInputRecord.readHeader(Unknown Source:0)
sun.security.ssl.SSLSocketInputRecord.read(Unknown Source:0)
java.net.SocketInputStream.read(Unknown Source:0)
java.net.SocketInputStream.read(Unknown Source:0)
java.lang.ThreadLocal.get(Unknown Source:0)
````

スタックトレースは以下のように解釈できます

* 新しい Door Game を開始する際に、ユーザーデータを読み込む呼び出しが行われます。
* これにより、ユーザーデータを読み込むための SQL クエリが実行されます（先ほど確認した遅い SQL クエリに関連しています）。
* その後、データベースからデータを読み取る呼び出しが確認できます。

では、これは何を意味するのでしょうか？アプリケーションの起動が遅いのは、ユーザーデータの読み込みに時間を費やしているためです。実際、プロファイラはこれが発生するコードの正確な行を教えてくれています

````
com.splunk.profiling.workshop.UserData.loadUserData(UserData.java:33)
````

対応するソースファイル（`./doorgame/src/main/java/com/splunk/profiling/workshop/UserData.java`）を開いて、このコードをより詳しく見てみましょう

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

ここでアプリケーションのロジックが動作しているのがわかります。データベースへの接続を確立し、先ほど確認した SQL クエリを実行します

````
select * FROM DoorGameDB.Users, DoorGameDB.Organizations
````

その後、各結果をループ処理し、各ユーザーを `User` オブジェクトのコレクションである `HashMap` オブジェクトに読み込みます。

ゲームの起動シーケンスが遅い理由はよく理解できましたが、どのように修正すればよいでしょうか？

さらなる手がかりを得るために、AlwaysOn Profiling のもう一つの部分であるメモリプロファイリングを見てみましょう。AlwaysOn Profiling の `Memory` タブをクリックします

![Memory Profiling](../images/memory_profiling.png)

このビューの上部では、アプリケーションが使用しているヒープメモリの量、ヒープメモリの割り当てレート、およびガベージコレクションのアクティビティを確認できます。

アプリケーションが最大 1 GB のヒープサイズのうち約 400 MB を使用していることがわかります。このような単純なアプリケーションとしては過剰に思えます。また、ガベージコレクションが発生し、アプリケーションが一時停止したことも確認できます（Door Game をプレイしたいユーザーにとっては迷惑だったでしょう）。

画面の下部では、Java アプリケーションコードのどのメソッドが最も多くのヒープメモリ使用量に関連しているかを確認できます。リストの最初のアイテムをクリックして、`java.util.Arrays.copyOf` メソッドに関連する Memory Allocation Stack Traces を表示します

![Memory Allocation Stack Traces](../images/memory_allocation_stack_traces.png)

プロファイラの助けにより、`loadUserData` メソッドが過剰な CPU 時間を消費するだけでなく、ユーザーデータを `HashMap` コレクションオブジェクトに格納する際に過剰なメモリも消費していることがわかります。

## 何を達成しましたか？

ここまでで多くのことを学びました！

* Splunk OpenTelemetry Java インストルメンテーションエージェントでプロファイラを有効にする方法を学びました。
* エージェントの出力でプロファイラが有効であることを確認する方法を学びました。
* APM でのプロファイリング関連のワークフローをいくつか探索しました
  * トラブルシューティングビューから AlwaysOn Profiling に移動する方法
  * ナビゲーションとフィルタリングを通じてフレームグラフとメソッド呼び出し時間テーブルを探索する方法
  * スパンにサンプリングされたコールスタックが関連付けられていることを識別する方法
  * ヒープ使用率とガベージコレクションアクティビティを探索する方法
  * 特定のメソッドのメモリ割り当てスタックトレースを表示する方法

次のセクションでは、遅い起動パフォーマンスを解決するためにアプリケーションに修正を適用します。
