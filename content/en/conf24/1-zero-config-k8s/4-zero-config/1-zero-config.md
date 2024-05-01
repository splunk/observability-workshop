---
title: Zero-Config Setup
linkTitle: 1. Zero-Config Setup
weight: 1
---

To see how Zero-Config works with a single pod we will patch the `api-gateway`. Once patched, the OpenTelemetry Collector will inject the auto-instrumentation library and the Pod will be restarted in order to start sending traces and profiling data. To show what happens when you enable Auto-Instrumentation, let's do a *before and after* of the configuration:

{{< tabs >}}
{P}{{% tab title="Describe api-gateway" %}}

``` bash
kubectl describe pods api-gateway | grep Image:
```

{{% /tab %}}
{{% tab title="Describe Output" %}}

``` text
Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.2
```

{{% /tab %}}
{{< /tabs >}}

This container was pulled from a remote repository `quay.io` and was not built to send traces to **Splunk Observability Cloud**. To enable the Java auto instrumentation on the api-gateway service add the `inject-java` annotation to Kubernetes with the `kubectl patch deployment` command.

{{< tabs >}}
{{% tab title="Patch api-gateway" %}}

``` bash
kubectl patch deployment api-gateway -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-java":"default/splunk-otel-collector"}}}}}'
```

{{% /tab %}}
{{% tab title="Patch Output" %}}

``` text
deployment.apps/api-gateway patched
```

{{% /tab %}}
{{< /tabs >}}

To check the container image(s) of the `api-gateway` pod again, run the following command:

{{< tabs >}}
{{% tab title="Describe api-gateway" %}}

``` bash
kubectl describe pods api-gateway | grep Image:
```

{{% /tab %}}
{{% tab title="Describe Output" %}}

```text
Image:         ghcr.io/signalfx/splunk-otel-java/splunk-otel-java:v1.30.0
Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.2
```

{{% /tab %}}
{{< /tabs >}}

A new image has been added to the `api-gateway` which will pull `splunk-otel-java` from `ghcr.io` (if you see two `api-gateway` containers, the original one is probably still terminating, so give it a few seconds).

To patch all the other services in the Spring Petclinic application, run the following command. This will add the `inject-java` annotation to the remaining services. There will be no change for the **config-server**, **discovery-server**, **admin-server** and **api-gateway** as these have already been patched.

{{< tabs >}}
{{% tab title="Patch all Petclinic services" %}}

``` bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"default/splunk-otel-collector\"}}}}}"

```

{{% /tab %}}
{{% tab title="Patch Output" %}}

``` text
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

Navigate back to the Kubernetes Navigator in **Splunk Observability Cloud**. After a couple of minutes you will see that the Pods are being restarted by the operator and the Zero config container will be added. This will look similar to the screenshot below:

![restart](../../images/k8s-navigator-restarted-pods.png)
