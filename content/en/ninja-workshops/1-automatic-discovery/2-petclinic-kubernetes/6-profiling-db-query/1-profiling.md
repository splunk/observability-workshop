---
title: Always-On Profiling & Metrics
linkTitle: 1. Always-On Profiling
weight: 1
---

When we installed the Splunk Distribution of the OpenTelemetry Collector using the Helm chart earlier, we configured it to enable **AlwaysOn Profiling** and **Metrics**. This means that OpenTelemetry Java will automatically generate CPU and Memory profiling for the application, sending them to Splunk Observability Cloud.

When you deploy the PetClinic application and set the annotation, the collector automatically detects the application and instruments it for traces and profiling. We can verify this by examining the startup logs of one of the Java containers we are instrumenting by running the following script:

The logs will show the flags that were picked up by the Java automatic discovery and configuration:

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
We are interested in the section written by the `com.splunk.opentelemetry.profiler.ConfigurationLogger` or the **Profiling Configuration**.

We can see the various settings you can control, such as the `splunk.profiler.directory`, which is the location where the agent writes the call stacks before sending them to Splunk. (This may be different depending on how you configure your containers.)

Another parameter you may want to change is `splunk.profiler.call.stack.interval`. This is how often the system captures a CPU Stack trace. You may want to reduce this interval setting if you have short spans like the ones we have in our Pet Clinic application. For the demo application, we did not change the default interval value, so Spans may not always have a CPU Call Stack related to them.

You can find how to set these parameters [here](https://help.splunk.com/en/splunk-observability-cloud/manage-data/available-data-sources/supported-integrations-in-splunk-observability-cloud/apm-instrumentation/instrument-a-java-application/configure-the-java-agent#profiling-configuration-java). In the example below, we see how to set a higher collection rate for call stacks in the `deployment.yaml`, by setting this value in the JAVA_OPTIONS config section.

``` yaml
env: 
- name: JAVA_OPTIONS
  value: "-Xdebug -Dsplunk.profiler.call.stack.interval=150"
```

<!--
jwe: not sure what the next paragraph is referring to, so commenting out for now.
If you don't see those lines as a result of the script, the startup may have taken too long and generated too many connection errors, try looking at the logs directly with `kubectl` or the `k9s` utility that is installed.
-->
