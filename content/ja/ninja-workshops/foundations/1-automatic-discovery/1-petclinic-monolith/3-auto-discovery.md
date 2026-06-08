---
title: Java の自動検出と設定
linkTitle: 3. Automatic Discovery
weight: 3
---

以下のコマンドでアプリケーションを起動できます。`mysql` プロファイルをアプリケーションに渡していることに注目してください。これにより、先ほど起動した MySQL データベースを使用するようアプリケーションに指示します。また、インスタンス名を使用して `otel.service.name` と `otel.resource.attributes` を論理名に設定しています。これらは後で UI でのフィルタリングにも使用されます

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Web ブラウザで `http://<IP_ADDRESS>:8083` にアクセスして、アプリケーションが実行されていることを確認できます（`<IP_ADDRESS>` は先ほど取得した IP アドレスに置き換えてください）。

Collector のインストール時に **AlwaysOn Profiling** と **Metrics** を有効にする設定を行いました。これにより、Collector がアプリケーションの CPU およびメモリプロファイルを自動的に生成し、Splunk Observability Cloud に送信します。

PetClinic アプリケーションを起動すると、Collector がアプリケーションを自動的に検出し、トレースとプロファイリングのためにインストルメントするのが確認できます。

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

Splunk APM UI にアクセスして、アプリケーションのコンポーネント、トレース、プロファイリング、DB クエリパフォーマンス、メトリクスを確認できます。左側のメニューから **APM → Overview** をクリックし、**Environment** ドロップダウンをクリックして、お使いの環境（例`<INSTANCE>-petclinic-env`）を選択してください（`<INSTANCE>` は先ほどメモした値に置き換えてください）。

検証が完了したら、コマンドプロンプトまたはターミナルウィンドウで `Ctrl-c` を押してアプリケーションを停止できます。

リソース属性は、報告されるすべてのスパンに追加できます（例`version=0.314`）。リソース属性のカンマ区切りリストも定義できます（例`key1=val1,key2=val2`）。

新しいリソース属性を指定して、Spring PetClinic アプリケーションを再度起動しましょう。実行コマンドにリソース属性を追加すると、Collector のインストール時に定義された内容が上書きされることに注意してください。新しいリソース属性 `version=0.314` を追加しましょう

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Splunk APM UI で最近のトレースにドリルダウンすると、スパン内に新しい `version` 属性が表示されます。
