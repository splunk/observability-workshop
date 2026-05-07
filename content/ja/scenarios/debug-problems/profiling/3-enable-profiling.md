---
title: AlwaysOn Profiling を有効にする
linkTitle: 3 AlwaysOn Profiling を有効にする
weight: 3
time: 20 minutes
---

メモリと CPU のプロファイラーを有効にし、その動作を確認し、Splunk Observability Cloud でアプリケーションの起動が遅い原因を特定する方法を学びましょう。

### アプリケーション設定の更新

両方のプロファイラーを有効にするために、Splunk OpenTelemetry Java エージェントに追加の設定引数を渡す必要があります。設定の詳細は[こちらのドキュメント](https://docs.splunk.com/observability/en/gdi/get-data-in/application/java/instrumentation/instrument-java-application.html#activate-alwayson-profiling)に記載されていますが、現時点では以下の設定のみ必要です。

````
SPLUNK_PROFILER_ENABLED="true"
SPLUNK_PROFILER_MEMORY_ENABLED="true"
````

アプリケーションは Kubernetes にデプロイされているため、Kubernetes マニフェストファイルを更新してこれらの環境変数を設定できます。`doorgame/doorgame.yaml` ファイルを開き、以下の環境変数の値が "true" に設定されていることを確認してください。

```` yaml
- name: SPLUNK_PROFILER_ENABLED
  value: "true"
- name: SPLUNK_PROFILER_MEMORY_ENABLED
  value: "true"
````

次に、以下のコマンドを実行して Door Game アプリケーションを再デプロイしましょう。

``` bash
cd ~/workshop/profiling
kubectl apply -f doorgame/doorgame.yaml
```

数秒後、更新されたアプリケーション設定で新しい Pod がデプロイされます。

### 動作確認

プロファイラーが有効になっていることを確認するために、以下のコマンドでアプリケーションログを確認しましょう。

```` bash
kubectl logs -l app=doorgame --tail=100 | grep JfrActivator
````

アプリケーションログの出力に、プロファイラーがアクティブであることを示す行が表示されるはずです。

```` log
[otel.javaagent 2024-02-05 19:01:12:416 +0000] [main] INFO com.splunk.opentelemetry.profiler.JfrActivator - Profiler is active.```
````

これにより、プロファイラーが有効になり、Kubernetes クラスターにデプロイされた OpenTelemetry Collector にデータを送信していることが確認できます。OpenTelemetry Collector はプロファイリングデータを Splunk Observability Cloud に転送します。

### APM でのプロファイリング

`http://<your IP address>:81` にアクセスして、The Door Game をさらに数回プレイしてください。

次に、Splunk Observability Cloud に戻り、**APM** → **Trace analyzer** をクリックします。

`doorgame` サービスと `GET new-game` オペレーション（ゲームの起動シーケンスをトラブルシューティングしているため）を含むトレースでフィルタリングします。

![New Game Traces](../images/new_game_traces.png)

これらのトレースの1つを選択すると、以下の画面が表示されます。

![Trace with Call Stacks](../images/trace_with_call_stacks.png)

スパンに「Call Stacks」が含まれていることがわかります。これは、先ほど CPU とメモリのプロファイリングを有効にした結果です。

`doorgame: SELECT doorgamedb` という名前のスパンをクリックし、右側の CPU stack traces をクリックします。

![Trace with CPU Call Stacks](../images/trace_with_cpu_call_stacks.png)

プロファイラーによってキャプチャされた CPU コールスタックが表示されます。

AlwaysOn Profiler を開いて、CPU スタックトレースをより詳細に確認しましょう。`View in AlwaysOn Profiler` の横にある `Span` リンクをクリックします。

![Flamegraph and table](../images/flamegraph_and_table.png)

AlwaysOn Profiler にはテーブルと[フレームグラフ](https://www.brendangregg.com/flamegraphs.html)の両方が含まれています。以下の操作を試して、このビューを探索してみてください。

* テーブルの項目をクリックして、フレームグラフの変化を確認する
* スタックフレームをクリックしてズームイン、親フレームをクリックしてズームアウトしてフレームグラフを操作する
* `splunk` や `jetty` などの検索キーワードを入力して、一致するスタックフレームをハイライト表示する

`DoorGame.startNew` メソッドから始めて、スタックトレースを詳しく見てみましょう（リクエストの最も遅い部分であることはすでにわかっています）。

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

スタックトレースは以下のように解釈できます。

* 新しい Door Game を開始する際に、ユーザーデータをロードする呼び出しが行われます。
* その結果、ユーザーデータをロードするための SQL クエリが実行されます（これは先ほど確認した遅い SQL クエリに関連しています）。
* そして、データベースからデータを読み込む呼び出しが確認できます。

では、これは何を意味するのでしょうか？アプリケーションの起動が遅いのは、ユーザーデータのロードに時間を費やしているためです。実際、プロファイラーはこれが発生する正確なコード行を教えてくれています。

````
com.splunk.profiling.workshop.UserData.loadUserData(UserData.java:33)
````

対応するソースファイル（`./doorgame/src/main/java/com/splunk/profiling/workshop/UserData.java`）を開いて、このコードをより詳細に確認しましょう。

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

ここでアプリケーションロジックの動作を確認できます。データベースへの接続を確立し、先ほど確認した SQL クエリを実行します。

````
select * FROM DoorGameDB.Users, DoorGameDB.Organizations
````

次に、各結果をループし、各ユーザーを `User` オブジェクトのコレクションである `HashMap` オブジェクトにロードします。

ゲームの起動シーケンスが遅い理由は十分に理解できましたが、どのように修正すればよいのでしょうか？

さらなる手がかりを得るために、AlwaysOn Profiling のもう1つの機能であるメモリプロファイリングを確認しましょう。AlwaysOn Profiling の `Memory` タブをクリックしてください。

![Memory Profiling](../images/memory_profiling.png)

このビューの上部では、アプリケーションが使用しているヒープメモリの量、ヒープメモリのアロケーション速度、およびガベージコレクションのアクティビティを確認できます。

アプリケーションが最大 1 GB のヒープサイズのうち約 400 MB を使用していることがわかります。このような単純なアプリケーションにしては過剰に見えます。また、ガベージコレクションが発生し、アプリケーションが一時停止したことも確認できます（Door Game をプレイしたい人はイライラしたことでしょう）。

画面の下部では、Java アプリケーションコード内のどのメソッドが最も多くのヒープメモリ使用量に関連しているかを確認できます。リストの最初の項目をクリックして、`java.util.Arrays.copyOf` メソッドに関連するメモリアロケーションスタックトレースを表示します。

![Memory Allocation Stack Traces](../images/memory_allocation_stack_traces.png)

プロファイラーの助けにより、`loadUserData` メソッドが過剰な CPU 時間を消費するだけでなく、ユーザーデータを `HashMap` コレクションオブジェクトに格納する際に過剰なメモリも消費していることがわかります。

## 達成したこと

ここまで多くのことを達成しました！

* Splunk OpenTelemetry Java インストルメンテーションエージェントでプロファイラーを有効にする方法を学びました。
* エージェントの出力でプロファイラーが有効になっていることを確認する方法を学びました。
* APM でのプロファイリング関連のワークフローをいくつか探索しました。
  * トラブルシューティングビューから AlwaysOn Profiling に移動する方法
  * ナビゲーションとフィルタリングを使用してフレームグラフとメソッド呼び出し時間テーブルを探索する方法
  * スパンにサンプリングされたコールスタックが関連付けられているかを識別する方法
  * ヒープ使用率とガベージコレクションのアクティビティを探索する方法
  * 特定のメソッドのメモリアロケーションスタックトレースを表示する方法

次のセクションでは、アプリケーションの起動パフォーマンスの遅延を解決するための修正を適用します。
