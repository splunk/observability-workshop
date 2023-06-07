---
title: Instrumentation in Kubernetes
weight: 7
---
TODO Note on .env being overwritten

TODO change name of environment from YOURENV to something else.

The development team has started using Kubernetes for container orchestration. Switch to the provided milestone `12microservices-k8s` with the instructions from "Getting Started".

The Kubernetes manifests are located in the `k8s` folder. Add auto-instrumentation to the `public_api` microservice `deployment` by configuring the Splunk distribution of OpenTelemetry Python. The `Dockerfile` has already been prepared.

Install the OpenTelemetry Collector to the environment using [Splunk's helm chart][splunk-otel-helm] and use the provided `values.yaml`:

{{< tabs >}}
{{% tab title="Shell Command" %}}

``` text
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

helm install my-splunk-otel-collector --set="splunkObservability.realm=${SPLUNK_REALM},splunkObservability.accessToken=${SPLUNK_ACCESS_TOKEN},clusterName=${CLUSTER_NAME}" splunk-otel-collector-chart/splunk-otel-collector -f values.yaml
```

{{% /tab %}}
{{< /tabs >}}

Rebuild the container images for the private registry:

{{< tabs >}}
{{% tab title="Shell Command" %}}
docker-compose build{{% /tab %}}
{{< /tabs >}}

Push the images to the private registry:

{{< tabs >}}
{{% tab title="Shell Command" %}}
docker-compose push{{% /tab %}}
{{< /tabs >}}

Deploy to the cluster with

{{< tabs >}}
{{% tab title="Shell Command" %}}

``` bash
kubectl apply -f k8s
```

{{% /tab %}}
{{< /tabs >}}

Test the service with:

{{< tabs >}}
{{% tab title="Shell Command" %}}

``` bash
ENDPOINT=$(kubectl get service/public-api -o jsonpath='{.spec.clusterIP}')
curl http://$ENDPOINT:8000/api -F text=@hamlet.txt
```

{{% /tab %}}
{{< /tabs >}}

The milestone for this task is `12microservices-k8s-autoi`. It has auto-instrumentation applied for *all* microservices.

[splunk-otel-helm]: https://github.com/signalfx/splunk-otel-collector-chart
