---
title: Always-On Profiling & Metrics
linkTitle: 1. Always-On Profiling
weight: 1
---

先ほどHelmチャート (chart) を使用してSplunk Distribution of the OpenTelemetry Collectorをインストール (install) した際、**AlwaysOn Profiling**と**Metrics**を有効にするように設定しました。これにより、OpenTelemetry Javaはアプリケーション (application) のCPUとメモリ (memory) のプロファイリング (profiling) を自動的に生成し、Splunk Observability Cloudに送信します。

PetClinicアプリケーションをデプロイ (deploy) してアノテーション (annotation) を設定すると、collectorは自動的にアプリケーションを検出し、トレース (trace) とプロファイリング (profiling) のためにインストルメント (instrument) します。これを確認するために、次のスクリプト (script) を実行して、インストルメント (instrument) しているJavaコンテナ (container) の1つの起動ログ (log) を調べることができます：

ログ (log) には、Javaの自動検出と設定によって取得されたフラグ (flag) が表示されます：

{{< tabs >}}
{{% tab title="Run the script" %}}

``` logs
.  ~/workshop/petclinic/scripts/get_logs.sh
```

{{% /tab %}}
{{% tab title="Example output" %}}

``` text {wrap="false"}
2024/02/15 09:42:00 Problem with dial: dial tcp 10.43.104.25:8761: connect: connection refused. Sleeping 1s
2024/02/15 09:42:01 Problem with dial: dial tcp 10.43.104.25:8761: connect: connection refused. Sleeping 1s
2024/02/15 09:42:02 Connected to tcp://discovery-server:8761
Picked up JAVA_TOOL_OPTIONS:  -javaagent:/otel-auto-instrumentation-java/javaagent.jar
Picked up _JAVA_OPTIONS: -Dspring.profiles.active=docker,mysql -Dsplunk.profiler.call.stack.interval=150
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
[otel.javaagent 2024-02-15 09:42:03:056 +0000] [main] INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: splunk-1.30.1-otel-1.32.1
[otel.javaagent 2024-02-15 09:42:03:768 +0000] [main] INFO com.splunk.javaagent.shaded.io.micrometer.core.instrument.push.PushMeterRegistry - publishing metrics for SignalFxMeterRegistry every 30s
[otel.javaagent 2024-02-15 09:42:07:478 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2024-02-15 09:42:07:478 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - Profiler configuration:
[otel.javaagent 2024-02-15 09:42:07:480 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                  splunk.profiler.enabled : true
[otel.javaagent 2024-02-15 09:42:07:505 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                splunk.profiler.directory : /tmp
[otel.javaagent 2024-02-15 09:42:07:505 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -       splunk.profiler.recording.duration : 20s
[otel.javaagent 2024-02-15 09:42:07:506 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -               splunk.profiler.keep-files : false
[otel.javaagent 2024-02-15 09:42:07:510 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -            splunk.profiler.logs-endpoint : http://10.13.2.38:4317
[otel.javaagent 2024-02-15 09:42:07:513 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -              otel.exporter.otlp.endpoint : http://10.13.2.38:4317
[otel.javaagent 2024-02-15 09:42:07:513 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -           splunk.profiler.memory.enabled : true
[otel.javaagent 2024-02-15 09:42:07:515 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -             splunk.profiler.tlab.enabled : true
[otel.javaagent 2024-02-15 09:42:07:516 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -        splunk.profiler.memory.event.rate : 150/s
[otel.javaagent 2024-02-15 09:42:07:516 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.call.stack.interval : PT0.15S
[otel.javaagent 2024-02-15 09:42:07:517 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -  splunk.profiler.include.internal.stacks : false
[otel.javaagent 2024-02-15 09:42:07:517 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.tracing.stacks.only : false
[otel.javaagent 2024-02-15 09:42:07:517 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2024-02-15 09:42:07:518 +0000] [main] INFO com.splunk.opentelemetry.profiler.JfrActivator - Profiler is active.
```

{{% /tab %}}
{{< /tabs >}}
私たちが注目しているのは、`com.splunk.opentelemetry.profiler.ConfigurationLogger`によって書き込まれたセクション、つまり**Profiling Configuration**です。

`splunk.profiler.directory`など、制御できるさまざまな設定を確認できます。これは、エージェント (agent) がSplunkに送信する前にコールスタック (call stack) を書き込む場所です。（これは、コンテナ (container) の設定方法によって異なる場合があります。）

変更したいもう1つのパラメータ (parameter) は`splunk.profiler.call.stack.interval`です。これは、システム (system) がCPU Stack traceをキャプチャ (capture) する頻度です。Pet Clinicアプリケーションのような短いスパン (span) がある場合は、このインターバル (interval) 設定を短くすることをお勧めします。デモ (demo) アプリケーションでは、デフォルト (default) のインターバル (interval) 値を変更しなかったため、スパン (span) に常にCPU Call Stackが関連付けられているとは限りません。

これらのパラメータ (parameter) を設定する方法は[こちら](https://help.splunk.com/en/splunk-observability-cloud/manage-data/available-data-sources/supported-integrations-in-splunk-observability-cloud/apm-instrumentation/instrument-a-java-application/configure-the-java-agent#profiling-configuration-java)で確認できます。以下の例では、`deployment.yaml`でコールスタック (call stack) のより高い収集レート (rate) を設定する方法を示しています。これは、JAVA_OPTIONS configセクション (section) でこの値を設定することで行います。

``` yaml
env:
- name: JAVA_OPTIONS
  value: "-Xdebug -Dsplunk.profiler.call.stack.interval=150"
```

<!--
jwe: not sure what the next paragraph is referring to, so commenting out for now.
If you don't see those lines as a result of the script, the startup may have taken too long and generated too many connection errors, try looking at the logs directly with `kubectl` or the `k9s` utility that is installed.
-->
