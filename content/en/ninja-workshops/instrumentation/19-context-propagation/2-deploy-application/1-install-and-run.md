---
title: 1. Install and Run the App
weight: 1
---

## Prerequisites

### Required

- Docker Engine 24+ (image builds and k3d)
- **k3d** v5+ and **kubectl**
- Terminal with `curl`, `docker`, and `kubectl`
- **Splunk Observability Cloud** org with an **access token** and **realm**
- APM permissions to view services, traces, and MetricSets

{{< tabs >}}
{{% tab title="Verify Tooling" %}}

```bash
docker info --format '{{.ServerVersion}}'
k3d version
kubectl version --client
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
28.4.0
k3d version v5.9.0
k3s version v1.35.5-k3s1 (default)
Client Version: v1.36.1
Kustomize Version: v5.8.1
```

{{% /tab %}}
{{< /tabs >}}

### Optional

- `jq` for JSON output
- Basic Python and HTTP header familiarity

You're now ready to deploy application services on k3d

{{% exercise title="Install and Run" %}}

### Set Up the Environment

Navigate to the Phase 1 directory and create a virtual environment:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd ~/workshop/context-propagation/scripts
./1-start-lab.sh
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
Creating k3d cluster 'trace-workshop'...
INFO[0000] portmapping '8080:8080' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy] 
INFO[0000] portmapping '13133:13133' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy] 
INFO[0000] Prep: Network
INFO[0000] Created network 'k3d-trace-workshop'
INFO[0000] Created image volume k3d-trace-workshop-images ...
```

{{% /tab %}}
{{< /tabs >}}

### Set Your Splunk Credentials

Export your credentials as environment variables. Replace each placeholder with your actual values:

Your environment should have values for `ACCESS_TOKEN` and `REALM`when you type `env`

``` bash
export CLUSTER_NAME=trace-workshop-"<YOUR_INITIALS>"
export WORKSHOP_ENV="trace-propagation-<YOUR-INITIALS>"
```

If  some or all the values they do not exist export them as follows:

``` bash
export ACCESS_TOKEN="<YOUR_TOKEN>"
export REALM="<YOUR_REALM>"
export CLUSTER_NAME=trace-workshop-"<YOUR_INITIALS>"
export WORKSHOP_ENV="trace-propagation-<YOUR-INITIALS>"
```

### Run the App

The app will automatically start in the background, run validation checks and send 2 (or ]up-to 15) requests.

Expected Outout

``` json
{
  "order_id": "ord-70764",
  "product": "widget",
  "tier": "premium",
  "amount": 149.99,
  "inventory": true,
  "payment": true,
  "fulfilment": "dhl"
}
```

If nothing appears or if there's an error, run the validation scripts.

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd ~/workshop/context-propagation/scripts
./validate-services.sh
```

{{% /tab %}}
{{% tab title="Example Service Output" %}}

``` text
Health endpoints:
  OK    edge-proxy → storefront health
  OK    inventory-service health
  OK    payment-proxy health
  OK    payment-service health
  OK    order-service health
  OK    email-service health ...
```

{{% /tab %}}
{{% tab title="Example Request Output" %}}

``` json
{
  "order_id": "ord-56584",
  "product": "widget",
  "tier": "enterprise",
  "amount": 999.98,
  "inventory": true,
  "payment": true,
  "fulfilment": "fedex"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

### Check Splunk APM

1. Open [Splunk Observability Cloud UI](http://app.us1.signalfx.com) (url depends on your workshop location) and search for `trace-propagation-<your initials>` in APM -> Service Map
2. This will return no results..

{{% notice title="Note" style="info" %}}
At this point you have a running app and proof that there is no data in Splunk. The app has no instrumentation code whatsoever.
{{% /notice %}}
