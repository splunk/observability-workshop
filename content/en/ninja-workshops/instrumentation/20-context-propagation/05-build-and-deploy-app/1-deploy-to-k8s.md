---
title: 1. Deploy to K8s
linkTitle: 1. Deploy to K8s
weight: 1
time: 10 minutes
description: In this step, you'll deploy the Splunk Distribution of the OpenTelemetry Collector to your k3d cluster using Helm. 

---

## Deploy to Kubernetes

```bash
make deploy
```

This script:

1. Applies all Kubernetes manifests from `deploy/k8s/`
2. Creates a `splunk-otel` secret from your `.env` credentials
3. Points deployments at the registry images
4. Waits for all rollouts to complete

---

## Validation checklist - Deploy

### 1. Confirm all pods are running

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop get pods
```

**Expected output:**

```
NAME                                  READY   STATUS    RESTARTS   AGE
catalog-api-xxxxxxxxxx-xxxxx          1/1     Running   0          2m
frontend-xxxxxxxxxx-xxxxx             1/1     Running   0          2m
gateway-xxxxxxxxxx-xxxxx              1/1     Running   0          2m
order-worker-xxxxxxxxxx-xxxxx         1/1     Running   0          2m
rabbitmq-xxxxxxxxxx-xxxxx             1/1     Running   0          2m
splunk-otel-collector-agent-xxxxx     1/1     Running   0          10m
storefront-api-xxxxxxxxxx-xxxxx       1/1     Running   0          2m
```

**Failure indicators:**

| STATUS | Likely cause |
|--------|--------------|
| `ImagePullBackOff` | Images not pushed - run `make build` again |
| `CrashLoopBackOff` | Check logs with `kubectl -n cosmic-shop logs deployment/<name>` |
| `Pending` | Insufficient cluster resources - check `kubectl describe pod <name>` |

{{% /tab %}}
{{< /tabs >}}

### 2. Confirm services and NodePort

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop get svc
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)              AGE
catalog-api      ClusterIP   10.43.xxx.xxx   <none>        3002/TCP             2m
frontend         NodePort    10.43.xxx.xxx   <none>        80:30080/TCP         2m
gateway          ClusterIP   10.43.xxx.xxx   <none>        80/TCP               2m
order-worker     ClusterIP   10.43.xxx.xxx   <none>        3003/TCP             2m
rabbitmq         NodePort    10.43.xxx.xxx   <none>        5672:xxxxx/TCP,15672:15672/TCP   2m
storefront-api   ClusterIP   10.43.xxx.xxx   <none>        3001/TCP             2m
```

{{% /tab %}}
{{< /tabs >}}

### 3. Confirm backend health endpoints

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop exec deploy/frontend-api -- wget -qO- http://localhost:3007/health
kubectl -n cosmic-shop exec deploy/catalog-api -- wget -qO- http://localhost:3002/health
kubectl -n cosmic-shop exec deploy/order-api -- wget -qO- http://localhost:3001/health
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{"status":"ok","service":"frontend-api","stage":"bff"}
{"status":"ok","service":"catalog-api"}
{"status":"ok","service":"order-api","stage":"order"}
```

{{% /tab %}}
{{< /tabs >}}

### 4. Confirm shop UI responds

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:30080/
curl -s http://localhost:30080/ | head -5
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
HTTP 200
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
```
{{% /tab %}}
{{< /tabs >}}

### 5. Confirm API catalog endpoint via gateway

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s http://localhost:30080/api/catalog | python3 -m json.tool | head -20
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
    "products": [
        {
            "id": "telescope-orion-8",
            "name": "Orion 8\" Dobsonian Telescope",
            "price": 449.99,
            ...
        }
    ]
}
```
{{% /tab %}}
{{< /tabs >}}

### 6. Confirm RabbitMQ management UI

{{< tabs >}}
{{% tab title="Script" %}}

The RabbitMQ Service uses **NodePort 15672** so k3d can expose the management UI through the loadbalancer.

**Verify the k3d loadbalancer mapped port 15672:**

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
0.0.0.0:30080->30080/tcp, 0.0.0.0:15672->15672/tcp, ...
```

If **15672 is missing** from that output, the cluster was created without the RabbitMQ port mapping — see `RabbitMQ UI is not loading` below.

**Confirm HTTP responds:**

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:15672/
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
HTTP 200
```

Open **http://localhost:15672** in a browser and log in with `guest` / `guest`.

**If RabbitMQ UI is not loading**, use port-forward in a **separate terminal** (keep it open):

```bash
kubectl -n cosmic-shop port-forward svc/rabbitmq 15672:15672
```

Then open http://localhost:15672 again.

{{% /tab %}}
{{< /tabs >}}

---
