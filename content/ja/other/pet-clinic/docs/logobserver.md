---
title: Log Observer
linktitle: 5. Log Observer
weight: 5
---

このセクションでは、Spring PetClinicアプリケーションをファイルシステムのファイルにログを書き込むように設定し、
Splunk OpenTelemetry Collectorがそのログファイルを読み取り（tail）、Splunk Observability Platformに情報を報告するように設定していきます。

## 1. FluentDの設定

Splunk OpenTelemetry Collectorを、Spring PetClinicのログファイルをtailし
Splunk Observability Cloudエンドポイントにデータを報告するように設定する必要があります。

Splunk OpenTelemetry Collectorは、FluentDを使用してログの取得/報告を行い、
Spring PetClinicのログを報告するための適切な設定を行うには、
デフォルトディレクトリ（`/etc/otel/collector/fluentd/conf.d/`）にFluentDの設定ファイルを追加するだけです。

以下は、サンプルのFluentD設定ファイル `petclinic.conf` を新たに作成し、

```bash
sudo nano /etc/otel/collector/fluentd/conf.d/petclinic.conf
```


ファイル `/tmp/spring-petclinic.log` を読み取るよう設定を記述します。

```
<source>
  @type tail
  @label @SPLUNK
  tag petclinic.app
  path /tmp/spring-petclinic.log
  pos_file /tmp/spring-petclinic.pos_file
  read_from_head false
  <parse>
    @type none
  </parse>
</source>
```


このとき、ファイル `petclinic.conf` のアクセス権と所有権を変更する必要があります。

```bash
sudo chown td-agent:td-agent /etc/otel/collector/fluentd/conf.d/petclinic.conf
sudo chmod 755 /etc/otel/collector/fluentd/conf.d/petclinic.conf
```

ファイルが作成されたら、FluentDプロセスを再起動しましょう。

```bash
sudo systemctl restart td-agent
```


## 3. Logbackの設定

Spring Pet Clinicアプリケーションは、いくつかのJavaログライブラリを使用することができます。
このシナリオでは、logbackを使ってみましょう。

リソースフォルダに `logback.xml` という名前のファイルを作成して…

```bash
nano src/main/resources/logback.xml
```


以下の設定を保存しましょう:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xml>
<configuration scan="true" scanPeriod="30 seconds">
  <contextListener class="ch.qos.logback.classic.jul.LevelChangePropagator">
      <resetJUL>true</resetJUL>
  </contextListener>
  <logger name="org.springframework.samples.petclinic" level="debug"/>
  <appender name="file" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>/tmp/spring-petclinic.log</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>springLogFile.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>5</maxHistory>
      <totalSizeCap>1GB</totalSizeCap>
    </rollingPolicy>
    <encoder>
      <pattern>
      %d{yyyy-MM-dd HH:mm:ss} - %logger{36} - %msg trace_id=%X{trace_id} span_id=%X{span_id} trace_flags=%X{trace_flags} service.name=%property{otel.resource.service.name}, deployment.environment=%property{otel.resource.deployment.environment} %n
      </pattern>
    </encoder>
  </appender>
  <root level="debug">
    <appender-ref ref="file" />
  </root>
</configuration>
```

その後、アプリケーションを再構築して再度実行していきます。


```bash
./mvnw package -Dmaven.test.skip=true
```

```bash
java -javaagent:./splunk-otel-javaagent.jar \
-Dserver.port=8083 \
-Dotel.service.name=$(hostname).service \
-Dotel.resource.attributes=deployment.environment=$(hostname),version=0.317 \
-Dsplunk.profiler.enabled=true \
-Dsplunk.profiler.memory.enabled=true \
-Dsplunk.metrics.enabled=true \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


これまで通り、アプリケーション `http://<VM_IP_ADDRESS>:8083`  にアクセスしてトラフィックを生成すると、ログメッセージが報告されるようになります。

左側のLog Observerアイコンをクリックして、ホストとSpring PetClinicアプリケーションからのログメッセージのみを選択するためのフィルタを追加できます。

1. Add Filter → Field → host.name → <あなたのホスト名>
2. Add Filter → Field → service.name → <あなたのホスト名>.service


## 4. まとめ

これでワークショップは終了です。
これまでに、Splunk Observability Cloudにメトリクス、トレース、ログ、データベースクエリのパフォーマンス、コードプロファイリングが報告されるようになりました。
おめでとうございます！
