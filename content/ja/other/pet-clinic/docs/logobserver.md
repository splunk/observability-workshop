---
title: 5. Log Observer
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

以下は、サンプルのFluentD設定ファイル（`petclinic.conf`、ファイル`/tmp/spring-petclinic.log`を読み取り）です。

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

したがって、ファイルを作成する必要があります。

```bash
sudo nano /etc/otel/collector/fluentd/conf.d/petclinic.conf
```

また、petclinic.confファイルのアクセス権と所有権を変更する必要があります。

```bash
sudo chown td-agent:td-agent /etc/otel/collector/fluentd/conf.d/petclinic.conf
sudo chmod 755 /etc/otel/collector/fluentd/conf.d/petclinic.conf
```

そして、上のスニペットからコンテンツを貼り付けます。ファイルが作成されたら、FluentDプロセスを再起動する必要があります。

```bash
sudo systemctl restart td-agent
```

## 3. Logbackの設定

Spring PetClinicアプリケーションは、いくつかの異なるJavaログライブラリを使用して設定できます。
このシナリオでは、logbackを使用しています。以下は、サンプルのlogback設定ファイルです。

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

設定フォルダにlogback.xmlという名前のファイルを作成するだけです。

```bash
nano src/main/resources/logback.xml
```

そして、上のスニペットからXMLコンテンツを貼り付けます。
その後、アプリケーションを再構築して再度実行する必要があります。


```bash
./mvnw package -Dmaven.test.skip=true
```

```bash
java -javaagent:./splunk-otel-javaagent.jar \
-Dotel.service.name=$(hostname).service \
-Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-Dotel.resource.attributes=deployment.environment=$(hostname)-petclinic,version=0.317 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


次に、アプリケーションを再度アクセスしてもっと多くのトラフィックを生成し、
`http://<VM_IP_ADDRESS>:8080` でログメッセージが報告されるようになります（遠慮なくナビゲートしてクリックしてください）。

左側のLog Observerアイコンをクリックして
ホストとSpring PetClinicアプリケーションからのログメッセージのみを選択するためのフィルタを追加できます。

1. フィルタを追加 → フィールド → host.name → <あなたのホスト名>
2. フィルタを追加 → フィールド → service.name → <あなたのホスト名>-petclinic.service

## 4. まとめ

これでワークショップは終了です。
これまでに、Splunk Observability Cloudにメトリクス、トレース、ログ、データベースクエリのパフォーマンス、コードプロファイリングが報告されるようになりました。
おめでとうございます！
