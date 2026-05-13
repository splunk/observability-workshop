---
title: Distributed Tracing and Bi-Directional Drilldowns
linkTitle: 4.1 Configure Instrumentation
weight: 1
time: 10 minutes
description: Configure instrumentation
---

## Summary of the changes we need to make

The [ThousandEyes documentation](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing), and specifically [the page for Splunk Observability APM](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing/distributed-tracing-splunk-apm), shows what is needed for distributed tracing:

For Propagators:
- `baggage` for 
- `b3` allows extraction of ThousandEyes B3 headers.
- `tracecontext` preserves `traceparent` and `tracestate`

In addition setting the sampler to `parentbased_always_on` ensures the trace continues once ThousandEyes starts the request. However this is not needed with Splunk, since Splunk samples 100% of traces.

We will make the following changes:
* Step 1: Modify the OTel Collector
  * Ensure all 3 propagators are set
* Step 2: Patch the application
  * Patch the services to inject java instrumentation

### Step 1: Modify the OTel Collector

Let's check the configuration of the instrumentation:

{{< tabs >}}
{{% tab title="Script" %}}
```bash
kubectl describe instrumentation splunk-otel-collector
```
{{% /tab %}}
{{% tab title="Example Abbreviated Output" %}}
```text
Name:         splunk-otel-collector
Namespace:    default
Labels:       app=splunk-otel-collector
...
Spec:
...
  Propagators:
    tracecontext
    baggage
    b3
...
```
{{% /tab %}}
{{< /tabs >}}

Under `Propagators` you can see that the ones we need are already set, so we don't need to make that change.

### Step 2: Patch the application

First, let's check which container images are deployed:

{{< tabs >}}
{{% tab title="Script" %}}
```bash
kubectl describe pods api-gateway | grep Image:
```
{{% /tab %}}
{{% tab title="Example Output" %}}
```text
    Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.7
```
{{% /tab %}}
{{< /tabs >}}

We can see there is only one container for the `api-gateway`. Once we patch the application we will see multiple container images (one for the api-gateway, and the other for instrumentation).

Let's inject the java instrumentation. (NOTE: There will be no change for the `config-server`, `discovery-server` and `admin-server` as these have already been patched.):

{{< tabs >}}
{{% tab title="Script" %}}
```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"default/splunk-otel-collector\"}}}}}"
```
{{% /tab %}}
{{% tab title="Example Output" %}}
```text
deployment.apps/admin-server patched (no change)
deployment.apps/api-gateway patched
deployment.apps/config-server patched (no change)
deployment.apps/customers-service patched
deployment.apps/discovery-server patched (no change)
deployment.apps/vets-service patched
deployment.apps/visits-service patched

```
{{% /tab %}}
{{< /tabs >}}

{{% notice title="For other runtimes" style="info" %}}
For other runtimes, use the annotation that matches the language; for example:
- `instrumentation.opentelemetry.io/inject-nodejs`
- `instrumentation.opentelemetry.io/inject-python`
- `instrumentation.opentelemetry.io/inject-dotnet`
{{% /notice %}}

We can check that our instrumentation deployed with:
{{< tabs >}}
{{% tab title="Script" %}}
```bash
kubectl describe pods api-gateway | grep Image:
```
{{% /tab %}}
{{% tab title="Example Output" %}}
```text
    Image:         ghcr.io/signalfx/splunk-otel-java/splunk-otel-java:v2.27.0
    Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.7
```
{{% /tab %}}
{{< /tabs >}}

You can also see that this pod has the Java instrumentation enabled, and the propagators are including `baggage`, `b3` and `tracecontext`:

{{< tabs >}}
{{% tab title="Script" %}}
```bash
kubectl describe pods api-gateway | grep OTEL_PROPAGATORS
```
{{% /tab %}}
{{% tab title="Example Output" %}}
```text
      OTEL_PROPAGATORS:                      tracecontext,baggage,b3
```
{{% /tab %}}
{{< /tabs >}}

Now we can validate the in-cluster API path from the namespace where the ThousandEyes Enterprise Agent runs.

{{% notice title="Be patient" style="warning" %}}
This may take some time until you get the expected output.
{{% /notice %}}

Try running:

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl run te-petclinic-curl \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS http://api-gateway.default.svc.cluster.local:82/api/customer/owners
```
{{% /tab %}}
{{% tab title="Example Output" %}}
```text
[{"id":1,"firstName":"George","lastName":"Franklin","address":"110 W. Liberty St.","city":"Madison","telephone":"6085551023","pets":[{"id":1,"name":"Leo","birthDate":"2000-09-07","type":{"id":1,"name":"cat"}}]},{"id":2,"firstName":"Betty","lastName":"Davis","address":"638 Cardinal Ave.","city":"Sun Prairie","telephone":"6085551749","pets":[{"id":2,"name":"Basil","birthDate":"2002-08-06","type":{"id":6,"name":"hamster"}}]},{"id":3,"firstName":"Eduardo","lastName":"Rodriquez","address":"2693 Commerce St.","city":"McFarland","telephone":"6085558763","pets":[{"id":4,"name":"Jewel","birthDate":"2000-03-07","type":{"id":2,"name":"dog"}},{"id":3,"name":"Rosy","birthDate":"2001-04-17","type":{"id":2,"name":"dog"}}]},{"id":4,"firstName":"Harold","lastName":"Davis","address":"563 Friendly St.","city":"Windsor","telephone":"6085553198","pets":[{"id":5,"name":"Iggy","birthDate":"2000-11-30","type":{"id":3,"name":"lizard"}}]},{"id":5,"firstName":"Peter","lastName":"McTavish","address":"2387 S. Fair Way","city":"Madison","telephone":"6085552765","pets":[{"id":6,"name":"George","birthDate":"2000-01-20","type":{"id":4,"name":"snake"}}]},{"id":6,"firstName":"Jean","lastName":"Coleman","address":"105 N. Lake St.","city":"Monona","telephone":"6085552654","pets":[{"id":8,"name":"Max","birthDate":"1995-09-04","type":{"id":1,"name":"cat"}},{"id":7,"name":"Samantha","birthDate":"1995-09-04","type":{"id":1,"name":"cat"}}]},{"id":7,"firstName":"Jeff","lastName":"Black","address":"1450 Oak Blvd.","city":"Monona","telephone":"6085555387","pets":[{"id":9,"name":"Lucky","birthDate":"1999-08-06","type":{"id":5,"name":"bird"}}]},{"id":8,"firstName":"Maria","lastName":"Escobito","address":"345 Maple St.","city":"Madison","telephone":"6085557683","pets":[{"id":10,"name":"Mulligan","birthDate":"1997-02-24","type":{"id":2,"name":"dog"}}]},{"id":9,"firstName":"David","lastName":"Schroeder","address":"2749 Blackhawk Trail","city":"Madison","telephone":"6085559435","pets":[{"id":11,"name":"Freddy","birthDate":"2000-03-09","type":{"id":5,"name":"bird"}}]},{"id":10,"firstName":"Carlos","lastName":"Estaban","address":"2335 Independence La.","city":"Waunakee","telephone":"6085555487","pets":[{"id":12,"name":"Lucky","birthDate":"2000-06-24","type":{"id":2,"name":"dog"}},{"id":13,"name":"Sly","birthDate":"2002-06-08","type":{"id":1,"name":"cat"}}]}]pod "te-petclinic-curl" deleted from default namespace
```
{{% /tab %}}
{{< /tabs >}}

You should see the full environment showing in Splunk Observability Cloud (filter on your environment, `thousandeyes-shw-xxxx`):
![ThousandEyes Service Map](../../images/splunk-apm-service-map.png?width=45vw)