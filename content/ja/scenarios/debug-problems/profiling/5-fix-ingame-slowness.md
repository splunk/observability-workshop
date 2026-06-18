---
title: ゲーム中の遅延を修正する
linkTitle: 5 ゲーム中の遅延を修正する
weight: 5
time: 10 minutes
---

ゲーム起動時の遅延が解決されたので、Door Game を数ラウンドプレイして、ゲームの残りの部分も高速に動作することを確認しましょう。

ゲームをプレイしていて、他に遅延に気づきませんか？**Splunk Observability** Cloud のデータを確認して、体感している内容を数値で把握しましょう。

### Splunk Observability Cloud でゲームのパフォーマンスを確認する

APM に移動し、画面右側の Traces をクリックします。トレースを Duration の降順でソートします

![Slow Traces](../images/slow_trace.png)

`GET /game/:uid/picked/:picked/outcome` オペレーションを持つトレースのいくつかが、5秒強の Duration を持っていることがわかります。これが、アプリをプレイしているときにまだ遅延を感じる理由です（遅延はもはやゲーム起動オペレーション `GET /new-game` ではなく、実際にゲームをプレイしている際に使用される別のオペレーションで発生していることに注意してください）。

遅いトレースの1つをクリックして詳しく見てみましょう。プロファイリングはまだ有効になっているため、このトレースの一部としてコールスタックがキャプチャされています。ウォーターフォールビューで子スパンをクリックし、次に CPU Stack Traces をクリックします

![View Stack on Span](../images/view_stack_on_span.png)

コールスタックの下部で、スレッドがスリープ状態であったことがわかります

``` log
com.splunk.profiling.workshop.ServiceMain$$Lambda$.handle(Unknown Source:0)
com.splunk.profiling.workshop.ServiceMain.lambda$main$(ServiceMain.java:34)
com.splunk.profiling.workshop.DoorGame.getOutcome(DoorGame.java:41)
com.splunk.profiling.workshop.DoorChecker.isWinner(DoorChecker.java:14)
com.splunk.profiling.workshop.DoorChecker.checkDoorTwo(DoorChecker.java:30)
com.splunk.profiling.workshop.DoorChecker.precheck(DoorChecker.java:36)
com.splunk.profiling.workshop.Util.sleep(Util.java:9)
java.util.concurrent.TimeUnit.sleep(Unknown Source:0)
java.lang.Thread.sleep(Unknown Source:0)
java.lang.Thread.sleep(Native Method:0)
```

コールスタックはストーリーを語ってくれます -- 下から上に読むことで、サービスコード内部で何が起きているかを説明できます。ソースコードに馴染みのない開発者であっても、このコールスタックを見て次のようなナラティブを構築できるはずです
> ゲームの結果を取得しています。DoorChecker を利用して何かが勝者かどうかを確認していますが、ドア2のチェックがなぜか precheck() を発行し、何らかの理由で長時間スリープしています。

このワークショップのアプリケーションは意図的にシンプルに作られています -- 実際のサービスでは、データベース呼び出し中やトレースされていない外部サービスへの呼び出し中にスレッドがサンプリングされることがあるかもしれません。また、遅いスパンが複雑なビジネスプロセスを実行している可能性もあり、その場合はスタックトレース同士がまったく関連していないこともあります。

メソッドやプロセスの実行時間が長いほど、その実行中にコールスタックがサンプリングされる可能性が高くなります。

### バグを修正しましょう

プロファイリングツールを使用することで、`DoorChecker.checkDoorTwo()` 内部から `DoorChecker.precheck()` メソッドを呼び出す際にアプリケーションが遅くなっていることを特定できました。エディタで `doorgame/src/main/java/com/splunk/profiling/workshop/DoorChecker.java` ソースファイルを開きましょう。

ファイルをざっと見ると、各ドアをチェックするメソッドがあり、すべてが `precheck()` を呼び出していることがわかります。実際のサービスでは、見えない/考慮されていない副作用がある可能性があるため、単純に `precheck()` の呼び出しを削除することには抵抗があるかもしれません。

29行目に以下のコードがあります

``` java
    private boolean checkDoorTwo(GameInfo gameInfo) {
        precheck(2);
        return gameInfo.isWinner(2);
    }

    private void precheck(int doorNum) {
        long extra = (int)Math.pow(70, doorNum);
        sleep(300 + extra);
    }
```

開発者の視点で見ると、ドア番号はゼロベースであるため、最初のドアは0、2番目は1、3番目は2です（これは慣例的なものです）。`extra` の値は追加のスリープ時間として使用され、`70^doorNum`（`Math.pow` はべき乗計算を行います）で計算されます。これは奇妙です。なぜなら、以下のようになるからです

* door 0 => 70^0 => 1ms
* door 1 => 70^1 => 70ms
* door 2 => 70^2 => 4900ms

遅延バグの根本原因を見つけました！これは、最初の2つのドアがそれほど遅くなかった理由も説明しています。

プロダクトマネージャーとチームリーダーと簡単に相談し、`precheck()` メソッドは残す必要があるが、追加のパディングは不要であることに合意しました。`extra` 変数を削除して、`precheck` を以下のように変更しましょう

```java
    private void precheck(int doorNum) {
        sleep(300);
    }
```

これですべてのドアが一貫した動作になります。作業を保存し、以下のコマンドを使用してアプリケーションを再ビルドおよび再デプロイします

``` bash
cd workshop/profiling
./5-redeploy-doorgame.sh
```

アプリケーションが正常に再デプロイされたら、再度 The Door Game にアクセスして修正が適用されていることを確認します
`http://<your IP address>:81`

## 何を達成しましたか？

* ゲームプレイに影響を与えるアプリケーションの別のパフォーマンス問題を発見しました。
* トレースに含まれる CPU コールスタックを使用して、アプリケーションの動作を理解しました。
* コールスタックがストーリーを語り、疑わしいコード行を指し示してくれることを学びました。
* 遅いコードを特定し、より高速になるように修正しました。
