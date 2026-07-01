---
title: Build & Deploy Application
linkTitle: 05. Build & Deploy Application
weight: 5
time: 2 minutes
description: In this step, you'll build Docker images for all Cosmic Observatory Shop services, push them to the k3d local registry, and deploy the full stack to Kubernetes. 

---

## Build container images

From the project root, with `.env` configured:

```bash
make build
```

This builds and pushes four images to `localhost:5111`:

| Image | Service |
|-------|---------|
| `cosmic-shop/frontend` | React shop UI with Splunk RUM |
| `cosmic-shop/storefront-api` | Order API with Splunk APM |
| `cosmic-shop/catalog-api` | Product catalog with Splunk APM |
| `cosmic-shop/order-worker` | RabbitMQ consumer with Splunk APM |

---

## Validation checklist — build

### 1. Confirm all four images were pushed

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s http://localhost:5111/v2/_catalog | python3 -m json.tool
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
    "repositories": [
        "cosmic-shop/catalog-api",
        "cosmic-shop/frontend",
        "cosmic-shop/order-worker",
        "cosmic-shop/storefront-api"
    ]
}
```

{{% /tab %}}
{{< /tabs >}}

### 2. Confirm images exist locally

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker images | grep cosmic-shop
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
localhost:5111/cosmic-shop/frontend          latest    abc123def456   2 minutes ago   45MB
localhost:5111/cosmic-shop/storefront-api    latest    def456abc789   2 minutes ago   180MB
localhost:5111/cosmic-shop/catalog-api       latest    ...
localhost:5111/cosmic-shop/order-worker      latest    ...
```

{{% /tab %}}
{{< /tabs >}}

---

## Deploy to Kubernetes

```bash
make deploy
```

This script:

1. Applies all Kubernetes manifests from `deploy/k8s/`
2. Creates a `splunk-otel` secret from your `.env` credentials
3. Points deployments at registry images
4. Waits for all rollouts to complete

---
