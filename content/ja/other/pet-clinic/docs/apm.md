---
title: Install OpenTelemetry Java Agent
linkTitle: 2. OpenTelemetry Java Agent
weight: 2
---

## 1. Spring PetClinic アプリケーションを動かす

APMをセットアップするためにまず必要なのは...そう、アプリケーションです！この演習では、Spring PetClinicアプリケーションを使用します。これはSpringフレームワーク（Spring Boot）で作られた、非常に人気のあるサンプルJavaアプリケーションです。

まずはPetClinicリポジトリをクローンし、そして、アプリケーションをコンパイル、ビルド、パッケージ、テストしていきます。

```bash
git clone https://github.com/spring-projects/spring-petclinic
```

`spring-petclinic` ディレクトリに移動します:

```bash
cd spring-petclinic
```

PetClinic が使用する MySQL データベースを起動します:

```bash
docker run -d -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 docker.io/mysql:5.7.8
```

そして、Splunk版のOpenTelemetry Java APMエージェントをダウンロードしておきましょう。

```bash
curl -L https://github.com/signalfx/splunk-otel-java/releases/latest/download/splunk-otel-javaagent.jar \
-o splunk-otel-javaagent.jar
```

次に、mavenコマンドを実行してPetClinicをコンパイル/ビルド/パッケージ化します:

```bash
./mvnw package -Dmaven.test.skip=true
```

{{% notice title="情報" style="info" %}}
実際にアプリをコンパイルする前に、mavenが多くの依存ライブラリをダウンロードするため、初回実行時には数分かかるでしょう。2回目以降の実行はもっと短くなります。
{{% /notice %}}

そして、以下のコマンドでアプリケーションを実行することができます:

```bash
java -javaagent:./splunk-otel-javaagent.jar \
-Dotel.service.name=$(hostname)-petclinic.service \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


アプリケーションが動作しているかどうかは、`http://<VM_IP_ADDRESS>:8080` にアクセスして確認することができます。次に、トラフィックを生成し、クリックしまくり、エラーを生成し、ペットを追加するなどしてください。その後、Splunk APM UIからExploreを開き、、アプリケーションのコンポーネントやトレースなどを調べることができます。

検証が完了したら、ターミナルで **`Ctrl-c`** を押すと、アプリケーションを停止することができます。


## 2. プロファイリングとJVMメトリクスを有効にする

CPU とメモリのプロファイリングを有効にするには `splunk.profiler.enabled=true` を、メモリやGC等のJVMメトリクスを有効にする `splunk.metrics.enabled=true` をアプリケーションの起動時に渡します。アプリケーションが停止していることを確認し、メトリクスとプロファイリングを有効にするために以下のコマンドを実行します。

```bash
java -javaagent:./splunk-otel-javaagent.jar \
-Dotel.service.name=$(hostname)-petclinic.service \
-Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


トラフィックを発生させるために、`http://<VM_IP_ADDRESS>:8080` を開いてアプリケーションにアクセスしてみましょう。クリックしまくり、エラーを発生させ、ペットを追加する、などなど。その後、Splunk APM UIにアクセスして、アプリケーションのコンポーネント、Traces、Profiling、Database Query Performance, Endpoint Performansや、DashboardからJVMメトリクスを調べることができます。

検証が完了したら、ターミナルで **`Ctrl-c`** を押すと、アプリケーションを停止することができます。


## 3. スパンにリソース属性を追加する

リソース属性は、報告されたすべてのスパンに追加することができます。例えば、 `version=0.314` のように。また、リソース属性のカンマ区切りリストも定義することができます。

新しいリソース属性を使用して、PetClinicを再び起動してみましょう。実行コマンドにリソース属性を追加すると、コレクタをインストールしたときに定義されたものが上書きされることに注意してください。そのため、新しいリソース属性と一緒に `deployment.environment` リソース属性も指定する必要があります。以下では `deployment.environment=$(hostname)-petclinic` と `version=0.314` を指定していることがわかると思います。


```bash
java -javaagent:./splunk-otel-javaagent.jar \
-Dotel.service.name=$(hostname).service \
-Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-Dotel.resource.attributes=deployment.environment=$(hostname)-petclinic,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


アプリケーションに戻り、さらにトラフィックを発生させます。そして Splunk APM UI に戻って、最近のトレースをドリルダウンし、スパンの新しい属性 `version` を見ることができます。

次のセクションではカスタム計装を追加して、OpenTelemetryでは何ができるのか、さらに見ていきます。
