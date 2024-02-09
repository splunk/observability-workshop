---
title: Traces & Database Query Performance
linkTitle: 40. Traces 
weight: 40
hidden: false
---

## 1. Introduction

As we have seen in the previous chapter, once you have enabled Zero Config Auto Instrumentation and started to run invocations though your application, traces will be send to **Splunk Observability Cloud Suite**
With these Traces we Splunk will automatically  generate Dependency maps and RED Metrics. In this next section we are going to examine the traces itself  and what information they provide to help you understand the behaviour of your services all without touching your code.

## 2.  Select a Trace in APM

There are multiple ways you can find a trace in Splunk APM.,

<!--

When we installed the collector we configured it to enable **AlwaysOn Profiling** and **Metrics**. This means that the collector will automatically generate CPU and Memory profiles for the application and send them to Splunk Observability Cloud.

When you deployed the PetClinic application, the collector automatically detect the application and instrument it for traces and profiling.

{{% tab title="Example output" %}}

``` text {wrap="false"}
Picked up JAVA_TOOL_OPTIONS:  -javaagent:/otel-auto-instrumentation-java/javaagent.jar
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
[otel.javaagent 2024-02-06 15:25:20:210 +0000] [main] INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: splunk-1.30.0-otel-1.32.0
[otel.javaagent 2024-02-06 15:25:20:691 +0000] [main] INFO com.splunk.javaagent.shaded.io.micrometer.core.instrument.push.PushMeterRegistry - publishing metrics for SignalFxMeterRegistry every 30s
[otel.javaagent 2024-02-06 15:25:22:485 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2024-02-06 15:25:22:485 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - Profiler configuration:
[otel.javaagent 2024-02-06 15:25:22:486 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                  splunk.profiler.enabled : true
[otel.javaagent 2024-02-06 15:25:22:487 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                splunk.profiler.directory : /tmp
[otel.javaagent 2024-02-06 15:25:22:487 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -       splunk.profiler.recording.duration : 20s
[otel.javaagent 2024-02-06 15:25:22:488 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -               splunk.profiler.keep-files : false
[otel.javaagent 2024-02-06 15:25:22:488 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -            splunk.profiler.logs-endpoint : http://10.13.2.123:4317
[otel.javaagent 2024-02-06 15:25:22:489 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -              otel.exporter.otlp.endpoint : http://10.13.2.123:4317
[otel.javaagent 2024-02-06 15:25:22:489 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -           splunk.profiler.memory.enabled : true
[otel.javaagent 2024-02-06 15:25:22:490 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -             splunk.profiler.tlab.enabled : true
[otel.javaagent 2024-02-06 15:25:22:490 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -        splunk.profiler.memory.event.rate : 150/s
[otel.javaagent 2024-02-06 15:25:22:491 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.call.stack.interval : PT10S
[otel.javaagent 2024-02-06 15:25:22:491 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -  splunk.profiler.include.internal.stacks : false
[otel.javaagent 2024-02-06 15:25:22:492 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.tracing.stacks.only : false
[otel.javaagent 2024-02-06 15:25:22:492 +0000] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2024-02-06 15:25:22:492 +0000] [main] INFO com.splunk.opentelemetry.profiler.JfrActivator - Profiler is active.
```

{{% /tab %}}

## 3. Review Profiling Data Collection

You can now visit the Splunk APM UI and examine the application components, traces, profiling, DB Query performance and metrics. From the left-hand menu **APM** → **Explore**, click the environment dropdown and select your environment e.g. `<INSTANCE>-petclinic` (where`<INSTANCE>` is replaced with the value you noted down earlier).

![APM Environment](../images/apm-environment.png)

Once your validation is complete you can stop the application by pressing `Ctrl-c`.

## 4. Adding Resource Attributes to Spans

Resource attributes can be added to every reported span. For example `version=0.314`. A comma-separated list of resource attributes can also be defined e.g. `key1=val1,key2=val2`.

Let's launch the PetClinic again using new resource attributes. Note, that adding resource attributes to the run command will override what was defined when we installed the collector. Let's add two new resource attributes `deployment.environment=$INSTANCE-petclinic-env,version=0.314`:

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Back in the Splunk APM UI we can drill down on a recent trace and see the new `version` attribute in a span.

-->