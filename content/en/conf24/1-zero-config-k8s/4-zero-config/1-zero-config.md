---
title: Zero-Config Setup
linkTitle: 1. Zero-Config Setup
weight: 1
---

Let's look at how zero-config works with a single pod, the `api-gateway`. If you enable Zero configuration for a pod, the Collector will attach an init-Container to your existing pod, and restart the pod to activate it.

To show what happens when you enable Auto instrumentation, let's do a *before and after* of the content of a pod, the `api-gateway` in this case:

{{< tabs >}}
{P}{{% tab title="Describe api-gateway" %}}

``` bash
kubectl describe pods api-gateway |grep Image:
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

```bash
kubectl patch deployment api-gateway -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-java":"default/splunk-otel-collector"}}}}}'
```

{{% /tab %}}
{{% tab title="Patch Output" %}}

```text
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

#### Enable Java Zero-Config Auto-Instrumentation on all pods

To patch all the other services in the Spring Petclinic application, run the following command. This will add the `inject-java` annotation to all the services in the Spring Petclinic application. **This automatically causes pods to restart.**

{{< tabs >}}
{{% tab title="Patch all Petclinic services" %}}

```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"default/splunk-otel-collector\"}}}}}"

```

{{% /tab %}}
{{% tab title="Patch Output" %}}

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

{{% notice note %}}
There will be no change for the **config-server**, **discovery-server**, **admin-server** and **api-gateway** as we patched these earlier.
{{% /notice %}}
