---
title: Java 向けの自動検出と自動構成
linkTitle: 3. Automatic Discovery
weight: 3
---

これで、以下のコマンドでアプリケーションを起動できます。アプリケーションには `mysql` プロファイルを渡している点に注意してください。これにより、アプリケーションは先ほど起動した MySQL データベースを使用するようになります。また、`otel.service.name` と `otel.resource.attributes` には、インスタンス名を使用した論理的な名前を設定しています。これらは UI でのフィルタリングにも使用されます。

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

`http://<IP_ADDRESS>:8083` にアクセスすると、アプリケーションが動作していることを確認できます（`<IP_ADDRESS>` は先ほど取得した IP アドレスに置き換えてください）。

Collector をインストールした際、**AlwaysOn Profiling** と **Metrics** を有効化するよう構成しました。これにより、Collector はアプリケーションの CPU およびメモリのプロファイルを自動的に生成し、Splunk Observability Cloud に送信します。

PetClinic アプリケーションを起動すると、Collector がアプリケーションを自動的に検出し、トレースとプロファイリングのために計装する様子を確認できます。

{{% tab title="Example output" %}}

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

ここで Splunk APM UI にアクセスし、アプリケーションコンポーネント、トレース、プロファイリング、DB Query Performance、メトリクスを確認できます。左側のメニューから **APM** をクリックし、**Environment** ドロップダウンをクリックして、自身の環境（例：`<INSTANCE>-petclinic`）を選択してください（`<INSTANCE>` は先ほど控えた値に置き換えます）。

確認が完了したら、`Ctrl-c` を押してアプリケーションを停止できます。

リソース属性は、レポートされる各スパンに追加できます。例えば `version=0.314` のように指定します。`key1=val1,key2=val2` のように、カンマ区切りでリソース属性のリストを定義することもできます。

新しいリソース属性を使用して PetClinic を再度起動してみましょう。なお、実行コマンドにリソース属性を追加すると、Collector のインストール時に定義した内容を上書きする点に注意してください。新しいリソース属性 `version=0.314` を追加してみましょう。

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Splunk APM UI に戻り、最近のトレースをドリルダウンすると、スパンに新しい `version` 属性が表示されていることを確認できます。
