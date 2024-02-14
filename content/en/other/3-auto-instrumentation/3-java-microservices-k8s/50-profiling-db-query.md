---
title: Splunk APM Always-on Profiling & Database Query Performance
linkTitle: 50. Always-on Profiling & Database Query Performance 
weight: 50
hidden: false
---
## 1. Introduction

As we have seen in the previous chapter, you can trace your interactions between the various services using APM without touching your code, which will allow you to identify issues faster. However as seen, beside tracing, Splunk Zero Config for Auto-Instrumentations offers additional features out of the box that can help you finding issues faster. In this section we are going to look at 2 of them:

* Always-on Profiling and Java Metrics
* Database Query Performance

If you want to dive deeper in Always-on Profiling or DB-Query performance, we have a separate Ninja Workshop called ***Debug Problems*** that you can follow for more detailed info.

## 2. AlwaysOn Profiling and Metrics

When we installed the Splunk Distribution of the OpenTelemetry Collector using the Helm chart earlier, we configured it to enable **AlwaysOn Profiling** and **Metrics**. This means that the collector will automatically generate CPU and Memory profiles for the application and send them to Splunk Observability Cloud.

When you deploy the PetClinic application, and set the Annotation, the collector automatically detects the application and instruments it for traces and profiling.

we can verify this by examining the  startup logs of one of our Java based containers we are instrumenting by running the following script:

```bash
.  ~/workshop/petclinic/scripts/get_logs.sh
```

The logs will show what flags where picked up by the Jav Auto instrumentation agent:

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
<!--
We are interested in the **Profiling Configuration**:

We can see the various settings you can control, some that are  useful depending on your use case like the `splunk.profiler.directory` -  The location where the agent  writes the call stacks before sending them to Splunk. This may be different depending how you configure your containers.
An other parameter you may want to change is `splunk.profiler.call.stack.interval` This is how often the system takes a CPU Stack trace. You may want to reduce this if you have short spans like we have in our application. (we kept the default as the spans in this demo application are extremely short, so Span may not always have a CPU  Call Stack related to it.)

You can find how to set these parameters [here](https://docs.splunk.com/observability/en/gdi/get-data-in/application/java/configuration/advanced-java-otel-configuration.html#profiling-configuration-java). ad this is how you set it in your deployment.yaml  exactly how pass any JAVA option to the the java application running in your container:

```text
 env: 
    - name: JAVA_OPTIONS
      value: "-Dsplunk.profiler.call.stack.interval=150"
```
-->

## 2. Looking at Profiling Data in the Trace Waterfall

Make sure you have your original (or similar) Trace  & Span **(1)** selected in the APM Waterfall view and select  **Memory Stack Traces (2)** from the right hand pane:

![profiling from span](../images/flamechart-in-waterfall.png)

The pane should show you the  Memory Stack Trace Flame Graph **(3)**, you can scroll down and/or make the pane  for a better view wider by dragging the right  side of the pane.

As AlwaysOn Profiling is constantly taking snapshots, or stack traces, of your application’s code and reading through thousands of stack traces is not practical, AlwaysOn Profiling aggregates and summarizes profiling data, providing a convenient way to explore Call Stacks in a view called the **Flame Graph**. It represents a summary of all stack traces captured from your application.  You can use the Flame Graph to discover which lines of code might be causing performance issues and to confirm whether the changes you make to the code have the intended effect.

To dive deeper in the Always-on Profiling, select Span **(3)** in the Profiling Pane under **Memory Stack Traces**
This will bring you to the Always-on Profiling main screen, with the Memory view pre selected:

![Profiling main](../images/profiling-memory.png)

* Java Memory Metric Charts **(1)**,  Allow you to `Monitor Heap Memory, Application Activity` like `Memory Allocation Rate`  and `Garbage Collecting` Metrics.
* Ability to focus/see metrics and Stack Traces only related to the Span **(2)**, This will filter out background activities running in the Java application if required.
* Java Function calls identified.**(3)**, allowing you to drill down  into the Methods called from that function.
* The Flame Graph,  with details of the 

<!--

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