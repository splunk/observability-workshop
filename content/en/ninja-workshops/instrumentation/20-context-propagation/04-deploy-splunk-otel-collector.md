---
title: Install oTel Collector
linkTitle: 04. Install oTel Collector
weight: 4
time: 15 minutes
description: In this step, you'll deploy the Splunk Distribution of the OpenTelemetry Collector to your k3d cluster using Helm. 
---

Each application pod sends data to the collector via the node IP:

```
Pod → http://$(NODE_IP):4318 → Splunk OTel Collector DaemonSet → Splunk O11y Cloud
```

---

## Install via Helm

{{% notice title="Note" style="info" %}}
**Important:** `make deploy` will **auto-install** the collector if it is missing. You can also install it explicitly first.
{{% /notice %}}

Ensure your `.env` file is configured, then run:

```bash
make collector
```

Or manually:

```bash
source .env

helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
helm repo update

helm upgrade --install splunk-otel-collector splunk-otel-collector-chart/splunk-otel-collector \
  --namespace cosmic-shop \
  --create-namespace \
  -f deploy/helm/splunk-otel-values.yaml \
  --set="splunkObservability.realm=${SPLUNK_REALM}" \
  --set="splunkObservability.accessToken=${SPLUNK_ACCESS_TOKEN}" \
  --set="clusterName=${CLUSTER_NAME}" \
  --set="environment=${SPLUNK_DEPLOYMENT_ENV}"
```

---

## Validation checklist

Run these commands after `make collector` completes.

### 1. Confirm Helm release is installed

{{< tabs >}}
{{% tab title="Script" %}}

```bash
helm list -n cosmic-shop
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
NAME                    NAMESPACE   REVISION   STATUS     CHART                         APP VERSION
splunk-otel-collector   cosmic-shop 1          deployed   splunk-otel-collector-0.x.x   0.x.x
```

STATUS must be `deployed`. If it shows `failed`, re-check `SPLUNK_REALM` and `SPLUNK_ACCESS_TOKEN` in `.env`.

{{% /tab %}}
{{< /tabs >}}

### 2. Confirm collector pods are running

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop get pods -l app.kubernetes.io/name=splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
NAME                                  READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-xxxxx     1/1     Running   0          60s
```

READY should be `1/1` and STATUS should be `Running`. If STATUS is `CrashLoopBackOff`, check logs in step 3.

{{% /tab %}}
{{< /tabs >}}

---

## Confirm your cluster in Splunk Observability Cloud

1. Open Splunk Observability Cloud
2. Navigate to **Infrastructure → Kubernetes → Kubernetes Clusters**
3. Search for your cluster name (`cosmic-shop-cluster` or the value of `CLUSTER_NAME` in `.env`)

The cluster should appear within a few minutes of the collector starting.

---

## Troubleshooting

### Helm install fails with auth error

Verify `SPLUNK_ACCESS_TOKEN` and `SPLUNK_REALM` in `.env` are correct and the token has ingest permissions.

### No cluster in Infrastructure navigator

Wait 2–3 minutes. Confirm the collector pod is running and check its logs for export errors.

---
