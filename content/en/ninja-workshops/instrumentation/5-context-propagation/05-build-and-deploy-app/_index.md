---
title: Build & Deploy Application
linkTitle: 05. Build & Deploy Application
weight: 5
time: 10 minutes

---
In this step, you'll build Docker images for all Cosmic Observatory Shop services, push them to the k3d local registry, and deploy the full stack to Kubernetes.

## Build Container Images

With all required `env` values configured, run:

```bash
cd ~/workshop/context-propagation
make build
```

This builds and pushes four images to `localhost:5111`

| Image | Service |
|-------|---------|
| `cosmic-shop/frontend` | React shop UI with Splunk RUM |
| `cosmic-shop/storefront-api` | Order API with Splunk APM |
| `cosmic-shop/catalog-api` | Product catalog with Splunk APM |
| `cosmic-shop/order-worker` | RabbitMQ consumer with Splunk APM |

## Validation Checklist - Build

#### 1. Confirm all images were pushed

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

#### 2. Confirm all relevant images exist

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker images | grep '^cosmic-shop/'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
cosmic-shop/catalog-api:latest      04c6bff29774        364MB         77.7MB        
cosmic-shop/frontend-api:latest         ...             ...            ...    
cosmic-shop/frontend:latest             ...             ...            ...       
cosmic-shop/fulfillment-worker:latest   ...             ...            ...        
cosmic-shop/order-api:latest            ...             ...            ...        
cosmic-shop/payment-api:latest          ...             ...            ...   
cosmic-shop/payment-gateway:latest      ...             ...            ...
```
{{% /tab %}}
{{< /tabs >}}
