---
title: Setting up Zero configuration Auto instrumentation for APM
linkTitle: 3. Auto-instrumentation & APM
weight: 30
---

For this workshop we will be using the Zero config option of the Opentelemetry Collector in Kubernetes.
This means that the Collector monitors you pods running in Kubernetes, and if they matcha certain criteria, they will en able auto instrumentation on the pod.

For Java this is the Kubernetes TAG `instrumentation.opentelemetry.io/inject-java\` set to `true`

## 1. Setting up Java auto instrumentation on the first pod

If you enable Zero configuration for a pod, the Collector will attach an initContainer to your existing pod, and restart the pod to activate it.

To show what happens when you enable Auto instrumentation let first do a for & after of the content of a pod, the `api-gateway` in this case:

```bash
kubectl describe pods api-gateway |grep Image:
```

The resulting output should say:

```text
Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.2
```

Lets add the Java auto instrumentation TAG to the api-gateway service first with the `kubectl patch deployment` command.
{{< tabs >}}
{{% tab title="Patch api-gateway service" %}}

```bash
kubectl patch deployment api-gateway -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-java":"true"}}}} }'
```

{{% /tab %}}
{{% tab title="kubectl patch Output" %}}

```text
deployment.apps/api-gateway patched
```

{{% /tab %}}
{{< /tabs >}}

Lets recheck the container(s) in your pod for the after look:

```bash
kubectl describe pods api-gateway |grep Image:
```

Next to the original pod from before, you should see an initContainer named **opentelemetry-auto-instrumentation**:

```text
Image:         ghcr.io/signalfx/splunk-otel-java/splunk-otel-java:v1.30.0
Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.2
```

## 2. Check the result in Splunk APM

Once the container is patched it will be restarted, let's login into the **Splunk Observability Cloud** with the URL provided by the Instructor to check out service.
First, Navigate to the  **APM** section to see the traces from your service in the **Explore** Pane.

Use the filter option and change the *environment* filter **(1)** and search for the name of your workshop instance in the drop down box, it should be the [INSTANCE]-workshop.  (where `INSTANCE` is the value from the shell script you run earlier). Make sure it is the only one selected.
![apm](../images/apm-api-gateway.png)
You should see the name **(2)** of the service and some metrics, if that is correct, click on **Explore** **(3)** to see the api-gateway service in the automatically generated dependency map.
![apm map](../images/api-gateeway-map.png)

## 3. Enable Java auto instrumentation on all pods

The above single service, will provide you *full fidelity* information on the interactions that are happening inside that one single service, something that can be useful, if you are 100% sure the issue you are trying to identify is only happening inside that specific service, independent of any relating services.

however, the mor common scenario is that you need to see the full interaction  between all services. So lets patch all the deployments (labeled with `app.kubernetes.io/part-of=spring-petclinic`) to add the inject annotation.
remember: **This automatically causes pods to restart.**

Note, there will be no change for the *api-gateway* as we patched it earlier.

{{< tabs >}}
{{% tab title="Patch all Petclinic services" %}}

```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"true\"}}}}}"

```

{{% /tab %}}
{{% tab title="kubectl patch Output" %}}

```text
deployment.apps/config-server patched
deployment.apps/admin-server patched
deployment.apps/customers-service patched
deployment.apps/visits-service patched
deployment.apps/discovery-server patched
deployment.apps/vets-service patched
deployment.apps/api-gateway patched (no change)
```

{{% /tab %}}
{{< /tabs >}}

It will take the Petclinic Microservice application a few minutes to start up and fully synchronise, but after its fully initialized, you now should see all the different services in Splunk APM:
![all services](../images/apm-full-service.png)
Of course, we want to check the Dependency map by clicking Explore:
![full map](../images/apm-map-full.png)

<!--
Next, run the script that will use the `maven` command to compile/build the PetClinic microservices:
{{< tabs >}}
{{% tab title="Running maven" %}}

```bash
./mvnw clean install -DskipTests -P buildDocker
```

{{% /tab %}}
{{% tab title="Maven Output" %}}

```text

Successfully tagged quay.io/phagen/spring-petclinic-api-gateway:latest
[INFO] Built quay.io/phagen/spring-petclinic-api-gateway
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] spring-petclinic-microservices 0.0.1 ............... SUCCESS [  0.770 s]
[INFO] spring-petclinic-admin-server ...................... SUCCESS [01:03 min]
[INFO] spring-petclinic-customers-service ................. SUCCESS [ 29.031 s]
[INFO] spring-petclinic-vets-service ...................... SUCCESS [ 22.145 s]
[INFO] spring-petclinic-visits-service .................... SUCCESS [ 20.451 s]
[INFO] spring-petclinic-config-server ..................... SUCCESS [ 12.260 s]
[INFO] spring-petclinic-discovery-server .................. SUCCESS [ 14.174 s]
[INFO] spring-petclinic-api-gateway 0.0.1 ................. SUCCESS [ 29.832 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 03:14 min
[INFO] Finished at: 2024-01-02T12:43:20Z
[INFO] ------------------------------------------------------------------------
```

{{% /tab %}}
{{< /tabs >}}

{{% notice style="info" %}}
This will take a few minutes the first time you run, `maven` will download a lot of dependencies before it compiles the application. Future builds will be a lot quicker.
{{% /notice %}}

## 3. Check Docker Images

Once the build completes, you need to verify if the containers are indeed built:

{{< tabs >}}
{{% tab title="Check Docker Containers" %}}

```bash
docker images
```

{{% /tab %}}
{{% tab title="Docker Output" %}}

``` text

splunk@show-no-config-i-027057abec7c0c6d3:~/spring-petclinic-microservices$ docker images
REPOSITORY                                          TAG       IMAGE ID       CREATED              SIZE
quay.io/phagen/spring-petclinic-api-gateway         latest    f954254824ed   7 seconds ago        510MB
<none>                                              <none>    5dbbb7d1fbb2   9 seconds ago        563MB
quay.io/phagen/spring-petclinic-discovery-server    latest    0761e73d679d   26 seconds ago       500MB
<none>                                              <none>    d71dc0ff96f4   28 seconds ago       544MB
quay.io/phagen/spring-petclinic-config-server       latest    81a0ab6495c2   39 seconds ago       488MB
<none>                                              <none>    69d60a035bb9   40 seconds ago       519MB
quay.io/phagen/spring-petclinic-visits-service      latest    ca306495bf11   50 seconds ago       526MB
<none>                                              <none>    b60155eb8ab4   52 seconds ago       596MB
quay.io/phagen/spring-petclinic-vets-service        latest    29f1b1909b8b   About a minute ago   527MB
<none>                                              <none>    b07e8de54c99   About a minute ago   598MB
quay.io/phagen/spring-petclinic-customers-service   latest    5b21e448c91e   About a minute ago   526MB
<none>                                              <none>    722fa001614c   About a minute ago   596MB
quay.io/phagen/spring-petclinic-admin-server        latest    4a1906a91210   About a minute ago   498MB
<none>                                              <none>    96f61c7bb66a   About a minute ago   540MB
eclipse-temurin                                     17        807dd649ff14   13 days ago          407MB

```

{{% /tab %}}
{{< /tabs >}}
 ## 2. AlwaysOn Profiling and Metrics

When we installed the collector we configured it to enable **AlwaysOn Profiling** and **Metrics**. This means that the collector will automatically generate CPU and Memory profiles for the application and send them to Splunk Observability Cloud.

When you start the PetClinic application you will see the collector automatically detect the application and instrument it for traces and profiling.

{{% tab title="Example output" %}}

``` text {wrap="false"}
Picked up JAVA_TOOL_OPTIONS: -javaagent:/usr/lib/splunk-instrumentation/splunk-otel-javaagent.jar -Dsplunk.profiler.enabled=true -Dsplunk.profiler.memory.enabled=true
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
[otel.javaagent 2023-06-26 13:32:04:661 +0100] [main] INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: splunk-1.25.0-otel-1.27.0
[otel.javaagent 2023-06-26 13:32:05:294 +0100] [main] INFO com.splunk.javaagent.shaded.io.micrometer.core.instrument.push.PushMeterRegistry - publishing metrics for SignalFxMeterRegistry every 30s
[otel.javaagent 2023-06-26 13:32:07:043 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2023-06-26 13:32:07:044 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - Profiler configuration:
[otel.javaagent 2023-06-26 13:32:07:047 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                  splunk.profiler.enabled : true
[otel.javaagent 2023-06-26 13:32:07:048 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                splunk.profiler.directory : /tmp
[otel.javaagent 2023-06-26 13:32:07:049 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -       splunk.profiler.recording.duration : 20s
[otel.javaagent 2023-06-26 13:32:07:050 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -               splunk.profiler.keep-files : false
[otel.javaagent 2023-06-26 13:32:07:051 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -            splunk.profiler.logs-endpoint : null
[otel.javaagent 2023-06-26 13:32:07:053 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -              otel.exporter.otlp.endpoint : null
[otel.javaagent 2023-06-26 13:32:07:054 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -           splunk.profiler.memory.enabled : true
[otel.javaagent 2023-06-26 13:32:07:055 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -             splunk.profiler.tlab.enabled : true
[otel.javaagent 2023-06-26 13:32:07:056 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -        splunk.profiler.memory.event.rate : 150/s
[otel.javaagent 2023-06-26 13:32:07:057 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.call.stack.interval : PT10S
[otel.javaagent 2023-06-26 13:32:07:058 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -  splunk.profiler.include.internal.stacks : false
[otel.javaagent 2023-06-26 13:32:07:059 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.tracing.stacks.only : false
[otel.javaagent 2023-06-26 13:32:07:059 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2023-06-26 13:32:07:060 +0100] [main] INFO com.splunk.opentelemetry.profiler.JfrActivator - Profiler is active.
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