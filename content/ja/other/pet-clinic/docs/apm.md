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
-Dotel.service.name=$(hostname).service \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


アプリケーションが動作しているかどうかは、`http://<VM_IP_ADDRESS>:8080` にアクセスして確認することができます。
次に、トラフィックを生成し、クリックしまくり、エラーを生成し、ペットを追加するなどしてください。その後、Splunk APM UIからExploreを開き、アプリケーションのコンポーネントやトレースなどを調べることができます。


## 2. いくつかのオプションを追加する

CPUとメモリのプロファイリングを有効にするには `splunk.profiler.enabled=true` と `splunk.profiler.memory.enabled=true` 、
メモリやGC等のJVMメトリクスを有効にする `splunk.metrics.enabled=true` をアプリケーションの起動時に渡します。

また、例えば `version=0.314` のように、リソース属性を報告されたすべてのスパンに追加することができます。。
リソース属性のカンマ区切りリストで定義していきます。
新しいリソース属性を使用して、PetClinicを再び起動してみましょう。
以下では `deployment.environment=$(hostname).service` と同時に `version=0.314` を指定しています。。

アプリケーションが停止していることを確認し（ターミナルで **`Ctrl-c`** を押すと、停止することができます）、これらのオプションを有効にして、再びアプリケーションを動かしてみましょう。

```bash
java -javaagent:./splunk-otel-javaagent.jar \
-Dotel.service.name=$(hostname).service \
-Dotel.resource.attributes=deployment.environment=$(hostname),version=0.314 \
-Dsplunk.profiler.enabled=true \
-Dsplunk.profiler.memory.enabled=true \
-Dsplunk.metrics.enabled=true \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


トラフィックを発生させるために、`http://<VM_IP_ADDRESS>:8080` を開いてアプリケーションにアクセスしてみましょう。
クリックしまくり、エラーを発生させ、ペットを追加する、などなど。
その後、Splunk APM UIにアクセスして、アプリケーションのコンポーネント、Traces、Profiling、Database Query Performance, Endpoint Performansや、DashboardからJVMメトリクスを調べることができます。

スパンの新しい属性 `version` はトレースをドリルダウンするとを見ることができます。さらに、サービスマップでも Breakdown の機能で分析したり、Tag Spotlightを開くと `version` 毎のパフォーマンス分析が使えます。


{{% notice title="Troubleshooting MetricSetsを追加する" style="info" %}}
サービスマップやTab Spotlightで、 `version` などのカスタム属性で分析できるようにするためには、Troubleshooting MetricSetsの設定をあらかじめ追加する必要があります。 
左メニューの **Settings → APM MetricSets** で、設定を管理することができます。 もしお使いのアカウントで分析できなければ、設定を追加してみましょう。
{{% /notice %}}


次のセクションではカスタム計装を追加して、OpenTelemetryでは何ができるのか、さらに見ていきます。
