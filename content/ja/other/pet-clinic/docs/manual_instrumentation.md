---
title: Manual Instrumentation
linkTitle: 3. Manual Instrumentation
weight: 3
---

## 1. 依存ライブラリを追加する

前のセクション足したような、プロセス全体に渡る属性は便利なのですが、ときにはさらに、リクエストの内容に応じた状況を知りたくなるかもしれません。心配ありません、OpenTelemetryのAPIを通じてそれらを計装し、データを送り、Splunk Observabilityで分析できるようになります。

最初に、JavaアプリケーションがOpenTelemetryのAPIを使えるように、ライブラリの依存を追加していきます。もちろん、vimなどのお好みのエディタをお使い頂いても大丈夫です！

```bash
nano pom.xml
```

そして、`<dependencies>` セクションの中（33行目）に↓をたしてください:


```
        <dependency>
            <groupId>io.opentelemetry</groupId>
            <artifactId>opentelemetry-api</artifactId>
        </dependency>
```

念の為、コンパイルできるか確かめてみましょう:

```
./mvnw package -Dmaven.test.skip=true
```

{{% notice title="Tips: nanoの使い方と壊れたファイルの直し方" style="info" %}}
nanoはLinux環境でよく使われる、シンプルなエディタの一つです。

* `ctrl-_` のあとに数字を入力すると、指定した行数にジャンプします。
* `ctrl-O` のあとに `Enter` で、ファイルを保存します。
* `ctrl-X` で、nanoを終了します。

もしファイルをどうしようもなく壊してしまって元に戻したい場合は、gitを使って次のようにするとよいでしょう。

```bash
git checkout pom.xml
```

{{% /notice %}}

これで、JavaのアプリケーションでOpenTelemetryのAPIが使う準備ができました。

## 2. Javaのコードにマニュアル計装を追加する

では、アプリケーションコードをちょっと変更して、リクエストのコンテキストのデータをスパン属性に追加してみましょう。

ここではPetClinicアプリケーションの中で `Find Owners` が使われたときに、どのような検索文字列が指定されたのかを調査できるようにしていきます。検索条件によってパフォーマンスが劣化してしまうケース、よくありませんか？そんなときは `OwnerController` に計装を追加していきましょう！

```bash
nano src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java
```

このコードを **変更するのは2箇所** です。

まず、`import jakarta.validation.Valid;` の下、37行目付近に↓を足します:

```java
import io.opentelemetry.api.trace.Span;
```

次に、 `// find owners by last name` のコメントがある箇所（おそらく95行目付近にあります）の下に、次のコードを足していきましょう:

```java
                Span span = Span.current();
                span.setAttribute("lastName", owner.getLastName());
```


このコードで、Last Nameとして指定された検索条件が、スパン属性 `lastName` としてSplunk Observabilityに伝えるようになりました。

アプリケーションをコンパイルし直して...

```bash
./mvnw spring-javaformat:apply package -Dmaven.test.skip=true
```


アプリケーションを起動します。せっかくなので、バージョンを一つあげて `version=0.315` としましょう。

```bash
java -javaagent:./splunk-otel-javaagent.jar \
-Dotel.service.name=$(hostname).service \
-Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-Dotel.resource.attributes=deployment.environment=$(hostname)-petclinic,version=0.315 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


`http://<VM_IP_ADDRESS>:8080` にアクセスして、オーナー検索をいくつか試してましょう。そしてSplunk APM UIからExploreを開き、アプリケーションのトレースを見ていきます。

検証が完了したら、ターミナルで **`Ctrl-c`** を押すと、アプリケーションを停止することができます。

次のセクションでは、RUMを使ってブラウザ上のパフォーマンスデータを収集してみましょう。
