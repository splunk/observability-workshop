---
title: 2. Deploy the Baseline
weight: 2
---

## Install the Splunk OTel Collector

The [Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart) is the production way to deploy the collector to Kubernetes. It handles the collector deployment, service, and configuration automatically.

### Add the Helm Repository

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
helm repo update
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
"splunk-otel-collector-chart" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
```

{{% /tab %}}
{{< /tabs >}}

### Install the Collector

This installs the Splunk OTel Collector **without** OBI. We'll enable OBI in the next step to show the before/after.

{{% notice title="Note" style="info" %}}
The environment variables `ACCESS_TOKEN`, `REALM`, and `INSTANCE` are pre-configured on your workshop instance. Run `env` to verify they exist.
{{% /notice %}}

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm -n obi-workshop install splunk-otel-collector \
  splunk-otel-collector-chart/splunk-otel-collector \
  --set="splunkObservability.realm=${REALM}" \
  --set="splunkObservability.accessToken=${ACCESS_TOKEN}" \
  --set="clusterName=${INSTANCE}-k8s" \
  --set="environment=${INSTANCE}-ebpf"
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
NAME: splunk-otel-collector
LAST DEPLOYED: Thu Feb 27 22:30:15 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
```

{{% /tab %}}
{{< /tabs >}}

## Deploy the Workshop Applications

The applications go into their own namespace:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd ~/workshop/obi/03-obi-k8s
kubectl apply -f namespace.yaml
kubectl apply -f apps.yaml
kubectl apply -f load-generator.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
namespace/obi-workshop created
deployment.apps/frontend created
service/frontend created
deployment.apps/order-processor created
service/order-processor created
deployment.apps/payment-service created
service/payment-service created
deployment.apps/load-generator created
```

{{% /tab %}}
{{< /tabs >}}

## Verify Everything is Running

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n obi-workshop
kubectl get pods  -n obi-workshop -l app.kubernetes.io/name=splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
NAME                                     READY   STATUS    RESTARTS   AGE
frontend-7d8b9f4c5-x2k4n                1/1     Running   0          30s
load-generator-5c6d7e8f9-m3j2k          1/1     Running   0          28s
order-processor-8e9f0a1b2-p4q5r         1/1     Running   0          30s
payment-service-9f0a1b2c3-s6t7u         1/1     Running   0          30s

NAME                                                  READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-abc12                      1/1     Running   0          45s
splunk-otel-collector-cluster-receiver-xyz34           1/1     Running   0          45s
```

{{% /tab %}}
{{< /tabs >}}

## Test the Application

Access the frontend via the NodePort:

``` bash
kubectl port-forward -n obi-workshop svc/frontend 30000:3000 &; sleep 5
```

Once the port is forwarded you can curl and hit the page:

``` bash
curl -s http://localhost:30000/create-order | python3 -m json.tool
```

## Confirm APM is Empty

{{% notice title="Exercise" style="green" icon="running" %}}

Check Splunk APM, filtering by environment `<INSTANCE>-ebpf`. You should see infrastructure metrics from the collector, but **no application traces** yet. The services are running but uninstrumented.

{{% /notice %}}
