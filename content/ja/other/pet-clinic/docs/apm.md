---
title: OpenTelemetry Javaエージェントをインストールする
linkTitle: 2. Javaエージェント
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

PetClinicが使用するMySQLデータベースを起動します:

```bash
docker run -d -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 docker.io/biarms/mysql:5.7
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
-Dserver.port=8083 \
-Dotel.service.name=$(hostname).service \
-Dotel.resource.attributes=deployment.environment=$(hostname),version=0.314 \
-Dsplunk.profiler.enabled=true \
-Dsplunk.profiler.memory.enabled=true \
-Dsplunk.metrics.enabled=true \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


アプリケーションが動作しているかどうかは、`http://<VM_IP_ADDRESS>:8083` にアクセスして確認することができます。
次に、トラフィックを生成し、クリックしまくり、エラーを生成し、ペットを追加するなどしてください。

* `-Dotel.service.name=$(hostname).service` では、アプリケーションの名前を定義しています。サービスマップ上のアプリケーションの名前等に反映されます。
* `-Dotel.resource.attributes=deployment.environment=$(hostname),version=0.314` では、Environmentと、versionを定義しています。
    - `deployment.environment=$(hostname)` は、Splunk APM UIの上部「Environment」に反映されます。
    - `version=0.314` はここでは、アプリケーションのバージョンを示しています。トレースをドリルダウンしたり、サービスマップのBreakdownの機能で分析したり、Tag Spotlightを開くと `version` 毎のパフォーマンス分析が使えます。
* `-Dsplunk.profiler.enabled=true` および `splunk.profiler.memory.enabled=true` では、CPUとメモリのプロファイリングを有効にしています。Splunk APM UIから、AlwaysOn Profilingを開いてみてください。
* `-Dsplunk.metrics.enabled=true` では、メモリやスレッドなどJVMメトリクスの送信を有効にしています。Dashboardsから、APM java servicesを開いてみてください。

その後、Splunk APM UIにアクセスして、それぞれのテレメトリーデータを確認してみましょう！


{{% notice title="Troubleshooting MetricSetsを追加する" style="info" %}}
サービスマップやTab Spotlightで、 `version` などのカスタム属性で分析できるようにするためには、Troubleshooting MetricSetsの設定をあらかじめ追加する必要があります。 
左メニューの **Settings → APM MetricSets** で、設定を管理することができます。 もしお使いのアカウントで分析できなければ、設定を追加してみましょう。
{{% /notice %}}


次のセクションではカスタム計装を追加して、OpenTelemetryでは何ができるのか、さらに見ていきます。
