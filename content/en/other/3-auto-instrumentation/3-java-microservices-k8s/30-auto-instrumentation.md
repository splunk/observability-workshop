---
title: Setting up Zero configuration Auto instrumentation for APM
linkTitle: 30. Auto-instrumentation & Metrics
weight: 30
---

In the previous chapter, we enabled the OpenTelemetry Collector for Kubernetes on our cluster and configured it to send metrics both Kubernetes and Mysql metrics to the **Splunk Observability Cloud**. The next section will enable auto-instrumentation for our Java apps running in the pods in our cluster.

{{% notice title="Zero Config Auto Instrumentation" style="info" %}}
It is important to understand that Zero Config Auto instrumentation is designed to get Trace/Span & Profiling data out of your existing application, without requiring  you to change your code or requiring to rebuild.
{{% /notice %}}

For this workshop we will be using the Zero config option of the Opentelemetry Collector in Kubernetes.
This means that the Collector monitors you pods running in Kubernetes, and if they match certain criteria, they will en able auto instrumentation on the pod.

For Java it is looking for the Kubernetes TAG `instrumentation.opentelemetry.io/inject-java\` set to `true` or to the location of the otel collector, like `default/splunk-otel-collector`. The last one will work across namespaces, so this what we will use in our examples

## 1. Triggering Zero Configuration  Instrumentation for the Discovery, Config and Admin servers

Due to the time it takes for the PetClinic microservices application to sync and get into a working order, we are going trigger auto instrumentation for the three management microservices of the Petclinic Java Application now as these services need to be up and running before the actual application can run. Let's run a script that will patch these three services and annotate them so the opentelemetry operator will initialise the zero config instrumentation and will start instrumenting them.

{{< tabs >}}
{{% tab title="Patching admin services" %}}

```bash
. ~/workshop/petclinic/scripts/patch-admin-services.sh
```

{{% /tab %}}
{{% tab title="Admin Services patching Output" %}}

```text
Patching deployment for config-server
deployment.apps/config-server patched
Patching deployment for discovery-server
deployment.apps/discovery-server patched
Patching deployment for admin-server
deployment.apps/admin-server patched
```

{{% /tab %}}
{{< /tabs >}}

## 2. Setting up Java auto instrumentation on the api-gateway pod

If you enable Zero configuration for a pod, the Collector will attach an init-Container to your existing pod, and restart the pod to activate it.

To show what happens when you enable Auto instrumentation, lets do a For & After of the content of a pod, the `api-gateway` in this case:

```bash
kubectl describe pods api-gateway |grep Image:
```

The resulting output should say:

```text
Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.2
```

This container is pulled from a remote repository `quay.io` and was not build to send traces to the **Splunk Observability Cloud**  

Lets enable the Java auto instrumentation on the api-gateway service first by adding the `inject-java` tag to kubernetes with the `kubectl patch deployment` command.
{{< tabs >}}
{{% tab title="Patch api-gateway service" %}}

```bash
kubectl patch deployment api-gateway -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-java":"default/splunk-otel-collector"}}}} }'
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

Next to the original pod from before, you should see an initContainer named **opentelemetry-auto-instrumentation**. ( If you get two api-gateway containers, the original one is still terminating, so give ity a few seconds):

```text
Image:         ghcr.io/signalfx/splunk-otel-java/splunk-otel-java:v1.30.0
Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.2
```

{{% notice title="Using the deployment.yaml" style="info" %}}
If you want your pods to send traces automatically, you can add the annotation to the deployment.yaml as is shown below. This will add the instrumentation library during the initial deployment.

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  labels: 
    app.kubernetes.io/part-of: spring-petclinic
spec:
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
      annotations:
        instrumentation.opentelemetry.io/inject-java: "true"
```

{{% /notice %}}

## 3. Check the result in Splunk APM

Once the container is patched it will be restarted, let's go back to the **Splunk Observability Cloud** with the URL provided by the Instructor to check our service.

First, Navigate to the **APM** ![APM](../images/apm-icon.png?classes=inline&height=25px) section to see the traces from your service in the **Explore** Pane. Use the filter option and change the *environment* filter **(1)** and search for the name of your workshop instance in the drop down box, it should be the [INSTANCE]-workshop. (where `INSTANCE` is the value from the shell script you run earlier). Make sure it is the only one selected.
![apm](../images/zero-config-first-services-overview.png)
You should see the name **(2)** of the api-gateway service and metrics in the Latency and Request & Errors charts. (You can ignore the Critical Alert, Its caused by the sudden request increase generated by the load generator, It will become the norm in a bit and go away).   You should also see the config-server, discovery-server and admin-server services.

Next, click on **Explore** **(3)** to see the services in the automatically generated dependency map and select the api-gateway service.
![apm map](../images/zero-config-first-services-map.png)

Here you can see the interaction between the Services.

## 4. Enable Java auto instrumentation on all pods

As shown in the above scenario, you could run tracing for a single service, and with the ability of Splunk to handle the *full fidelity* of all your interactions, will allow you to see everything that is happening inside that one single service, something that can be useful, if you are 100% sure the issue you are trying to identify is only happening inside that specific service, independent of any relating services.

However, the more common scenario is that you need to see the full interaction between all services. So lets patch all the deployments (labeled with `app.kubernetes.io/part-of=spring-petclinic`) to add the inject annotation.
remember: **This automatically causes pods to restart.**

Note, there will be no change for the *config-server, discovery-server, admin-server & api-gateway* as we patched these earlier.

{{< tabs >}}
{{% tab title="Patch all Petclinic services" %}}

```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"default/splunk-otel-collector\"}}}}}"

```

{{% /tab %}}
{{% tab title="kubectl patch Output" %}}

```text
deployment.apps/config-server patched (no change)
deployment.apps/admin-server patched (no change)
deployment.apps/customers-service patched
deployment.apps/visits-service patched
deployment.apps/discovery-server patched (no change)
deployment.apps/vets-service patched
deployment.apps/api-gateway patched (no change)
```

{{% /tab %}}
{{< /tabs >}}

It will take the Petclinic Microservice application a few minutes to start up and fully synchronise.
In the mean time let's examine the metrics that are available for each service that is instrumented and visit the request, error, and duration (RED) metrics Dashboard

## 5. Examine R.E.D. Metrics for the api-gateway

 Splunk APM provides a set of built-in dashboards that present charts and visualized metrics to help you see problems occurring in real time and quickly determine whether the problem is associated with a service, a specific endpoint, or the underlying infrastructure.  To look at this dashboard for `api-gateway`, make sure you have the `api-gateway` service selected in the Dependency map as show above, then click on the ***View Dashboard** Link **(1)**  at the top of the right hand pane.
This will bring you to the services dashboard:

![metrics dashboard](../images/zero-config-first-services-metrics.png)

This dashboard, that is available for each of your instrumented services, offers an overview of the key `request, error, and duration (RED)` metrics based on Monitoring MetricSets created from endpoint spans for your services, endpoints, and Business Workflows. They also present related host and Kubernetes metrics to help you determine whether problems are related to the underlying infrastructure, as in the above image.
As the dashboards allow you to go back in time with the *Time picker* window **(1)**, its the perfect spot to identify behaviour you wish to be alerted on, and with a click on one of the bell icons **(2)** available in each chart, you can set up an alert to do just that.

If you scroll down the page, you get host and Kubernetes metrics related to your service as well.
Let's move on to look at some of the traces.
<!--
{{< tabs >}}
{{% tab title="Tail Log" %}}

``` bash
. ~/workshop/petclinic/scripts/tail_logs.sh
```

{{% /tab %}}
{{% tab title="Tail Log Output" %}}

```text
{"severity":"error","msg": "Error: net::ERR_CONNECTION_REFUSED at http://10.13.2.123:81/#!/welcome"}
{"severity":"error","msg": "Error: net::ERR_CONNECTION_REFUSED at http://10.13.2.123:81/#!/welcome"}
{"severity":"info","msg":"Welcome Text = "Welcome to Petclinic"}
{"severity":"info","msg":"@ALL"}
{"severity":"info","msg":"@owner details page"}
{"severity":"info","msg":"@pet details page"}
{"severity":"info","msg":"@add pet page"}
{"severity":"info","msg":"@veterinarians page"}
{"severity":"info","msg":"cookies was"}
```

{{% /tab %}}
{{< /tabs >}}

Once the services are fully initialized, you now should see all the different services appear in Splunk APM:
![all services](../images/apm-full-service.png)
Of course, we want to check the Dependency map by clicking Explore:
![full map](../images/apm-map-full.png)
-->