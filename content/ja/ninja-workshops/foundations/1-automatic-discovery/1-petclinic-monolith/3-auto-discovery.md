---
title: Java 向け自動ディスカバリーおよび設定
linkTitle: 3. 自動ディスカバリー
weight: 3
---

以下のコマンドでアプリケーションを起動できます。`mysql` プロファイルをアプリケーションに渡していることに注目してください。これにより、先ほど起動したMySQLデータベースを使用するようアプリケーションに指示します。また、`otel.service.name` と `otel.resource.attributes` をインスタンス名を使用した論理名に設定しています。これらはUIでのフィルタリングにも使用されます

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

`http://<IP_ADDRESS>:8083`（`<IP_ADDRESS>` を先ほど取得したIPアドレスに置き換えてください）にアクセスして、アプリケーションが実行されていることを確認できます。

Collectorをインストールした際、**AlwaysOn Profiling** と **Metrics** を有効にするように設定しました。これにより、CollectorはアプリケーションのCPUおよびメモリプロファイルを自動的に生成し、Splunk Observability Cloudに送信します。

PetClinicアプリケーションを起動すると、Collectorがアプリケーションを自動的に検出し、トレースとプロファイリングのために計装するのが確認できます。

{{% tab title="出力例" %}}

``` text {wrap="false"}
Picked up JAVA_TOOL_OPTIONS: -javaagent:/usr/lib/splunk-instrumentation/splunk-otel-javaagent.jar
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
[otel.javaagent 2024-08-20 11:35:58:970 +0000] [main] INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: splunk-2.6.0-otel-2.6.0
[otel.javaagent 2024-08-20 11:35:59:730 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2024-08-20 11:35:59:730 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - Profiler configuration:
[otel.javaagent 2024-08-20 11:35:59:730 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                  splunk.profiler.enabled : true
[otel.javaagent 2024-08-20 11:35:59:731 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                splunk.profiler.directory : /tmp
[otel.javaagent 2024-08-20 11:35:59:731 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -       splunk.profiler.recording.duration : 20s
[otel.javaagent 2024-08-20 11:35:59:731 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -               splunk.profiler.keep-files : false
[otel.javaagent 2024-08-20 11:35:59:732 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -            splunk.profiler.logs-endpoint : null
[otel.javaagent 2024-08-20 11:35:59:732 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -              otel.exporter.otlp.endpoint : null
[otel.javaagent 2024-08-20 11:35:59:732 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -           splunk.profiler.memory.enabled : true
[otel.javaagent 2024-08-20 11:35:59:732 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -        splunk.profiler.memory.event.rate : 150/s
[otel.javaagent 2024-08-20 11:35:59:732 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.call.stack.interval : PT10S
[otel.javaagent 2024-08-20 11:35:59:733 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -  splunk.profiler.include.internal.stacks : false
[otel.javaagent 2024-08-20 11:35:59:733 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.tracing.stacks.only : false
[otel.javaagent 2024-08-20 11:35:59:733 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2024-08-20 11:35:59:733 +0000] [main] INFO com.splunk.opentelemetry.profiler.JfrActivator - Profiler is active.
```

{{% /tab %}}

Splunk APM UIにアクセスして、アプリケーションコンポーネント、トレース、プロファイリング、DB Queryパフォーマンス、メトリクスを確認できます。左側のメニューから **APM** をクリックし、**Environment** ドロップダウンをクリックして、ご自身の環境（例：`<INSTANCE>-petclinic`、`<INSTANCE>` は先ほどメモした値に置き換えてください）を選択します。

検証が完了したら、`Ctrl-c` を押してアプリケーションを停止できます。

リソース属性は、報告されるすべてのスパンに追加できます。例えば `version=0.314` のように指定します。カンマ区切りのリソース属性リストも定義できます（例：`key1=val1,key2=val2`）。

新しいリソース属性を使用してPetClinicを再度起動しましょう。実行コマンドにリソース属性を追加すると、Collectorのインストール時に定義された内容が上書きされることに注意してください。新しいリソース属性 `version=0.314` を追加しましょう

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Splunk APM UIに戻り、最近のトレースをドリルダウンすると、スパン内に新しい `version` 属性が表示されます。
