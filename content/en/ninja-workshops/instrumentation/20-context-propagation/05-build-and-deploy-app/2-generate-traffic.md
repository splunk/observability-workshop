---
title: 2. Generate Traffic
linkTitle: 2. Generate Traffic
weight: 2
time: 15 minutes
description: In this step, you'll generate traffic through Cosmic Observatory Shop. 
---

## Access the application

Open the Cosmic Observatory Shop in your browser:

**http://localhost:30080**

You should see the astronomy equipment catalog with telescopes, eyepieces, and astrophotography gear.

![app](./images/cosmic-shop.png)

Optional — RabbitMQ management UI:

**http://localhost:15672** (login: `guest` / `guest`)

![rabbitmq](./images/rabbitmq.png)

If the UI does not load, verify the loadbalancer port and use port-forward:

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
kubectl -n cosmic-shop port-forward svc/rabbitmq 15672:15672
```

---

## Generate initial traffic

1. Open the shop at http://localhost:30080
2. Enter an email address (e.g. `observer@cosmic.shop`)
3. Click **Purchase** on any product
4. Confirm the order in the modal

Repeat a few times to generate trace data.

---

### 1. Confirm telemetry in Splunk (allow 1–2 minutes)

After placing orders, confirm data is arriving:

| Signal | Where to look | Pass indicator |
|--------|---------------|----------------|
| RUM | RUM → Sessions, filter `cosmic-observatory-shop` | Sessions appear with page loads |
| APM | APM → Services, filter `workshop-context-prop` | `storefront-api`, `catalog-api`, `order-worker` listed |

> Traces will appear but **will not be connected** across services yet - that's expected for step 06.

---

## Troubleshooting

### ImagePullBackOff / ErrImagePull

k3d cannot pull `localhost:5111/...` from inside the cluster. Images must be **imported** into k3d:

{{< tabs >}}
{{% tab title="Script" %}}

```bash
make build
make fix-images
```

Or step by step:

```bash
make build
make import-images
kubectl -n cosmic-shop set image deployment/catalog-api catalog-api=cosmic-shop/catalog-api:latest
kubectl -n cosmic-shop patch deployment catalog-api --type=json \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/imagePullPolicy","value":"Never"}]'
kubectl -n cosmic-shop delete pod -l app=catalog-api --force --grace-period=0
kubectl -n cosmic-shop rollout status deployment/catalog-api --timeout=180s
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
kubectl -n cosmic-shop get pods -l app=catalog-api
```

```
NAME                           READY   STATUS    RESTARTS   AGE
catalog-api-xxxxxxxxxx-xxxxx   1/1     Running   0          30s
```
{{% /tab %}}
{{< /tabs >}}

---
