---
title: Patching the Deployment
linkTitle: 1. Patching the Deployment
weight: 1
---

To configure **automatic discovery and configuration**, the deployments need to be patched to add the instrumentation annotation. Once patched, the OpenTelemetry Collector will inject the automatic discovery and configuration library and the Pods will be restarted in order to start sending traces and profiling data. First, confirm that the `api-gateway` does not have the `splunk-otel-java` image by running the following:

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

Next, enable the Java automatic discovery and configuration for all the services by adding the annotation to the deployments. The following command will patch the all deployments. This will trigger the OpenTelemetry Operator to inject the `splunk-otel-java` image into the Pods:

{{< tabs >}}
{{% tab title="Patch all PetClinic services" %}}

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
deployment.apps/api-gateway patched
```

{{% /tab %}}
{{< /tabs >}}

There will be no change for the **config-server**, **discovery-server** and **admin-server** as these have already been patched.

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

A new image has been added to the `api-gateway` which will pull `splunk-otel-java` from `ghcr.io` (Note: if you see two `api-gateway` containers, the original one is probably still terminating, so give it a few seconds).

Navigate back to the Kubernetes Navigator in **Splunk Observability Cloud**. After a couple of minutes, you will see that the Pods are being restarted by the operator and the automatic discovery and configuration container will be added. This will look similar to the screenshot below:

![restart](../../images/k8s-navigator-restarted-pods.png)

Wait for the Pods to turn green in the Kubernetes Navigator, then go tho the next section.
