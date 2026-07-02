---
title: Rebuild and Deploy RabbitMQ fix
weight: 1
time: 5 minutes

---

## Rebuild and redeploy after saving

From the project root run these steps:

```bash
bash scripts/build-images.sh payment-api fulfillment-worker
bash scripts/import-images-k3d.sh payment-api fulfillment-worker
kubectl -n cosmic-shop rollout restart deployment/payment-api
kubectl -n cosmic-shop rollout restart deployment/fulfillment-worker
kubectl -n cosmic-shop rollout status deployment/payment-api --timeout=180s
kubectl -n cosmic-shop rollout status deployment/fulfillment-worker --timeout=180s
```

---

## Validation checklist

Run these commands after redeploy completes.

### 1. Confirm health endpoints report propagation enabled

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop exec deploy/payment-api -- wget -qO- http://localhost:3005/health
kubectl -n cosmic-shop exec deploy/fulfillment-worker -- wget -qO- http://localhost:3006/health
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{"status":"ok","service":"payment-api","stage":"payment","rabbitmq":true,"propagation":true}
{"status":"ok","service":"fulfillment-worker","stage":"fulfillment","propagation":true}
```

{{% /tab %}}
{{< /tabs >}}

### 2. Confirm rollouts completed

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop rollout status deployment/payment-api
kubectl -n cosmic-shop rollout status deployment/fulfillment-worker
```

{{% /tab %}}
{{< /tabs >}}

### 3. Confirm startup logs mention propagation

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop logs deployment/payment-api --tail=3
kubectl -n cosmic-shop logs deployment/fulfillment-worker --tail=3
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
RabbitMQ context propagation: ENABLED
...
RabbitMQ context propagation: ENABLED
```

{{% /tab %}}
{{< /tabs >}}

### 4. Place a test order and verify worker processing

{{% /notice %}}
Place **new** orders after redeploy - messages published before the fix will not carry trace context.

{{% /notice %}}

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s -X POST http://localhost:30080/api/purchases \
  -H "Content-Type: application/json" \
  -d '{"productId":"filter-nebula-uhc","quantity":1,"customerEmail":"propagation-test@cosmic.shop"}' \
  | python3 -m json.tool

sleep 2
kubectl -n cosmic-shop logs deployment/fulfillment-worker --tail=3
```

{{% /tab %}}
{{< /tabs >}}

---

## Troubleshooting

{{< details summary="Click here to see the answer" >}}
### Potential Issue 1. Fulfillment worker still shows orphan traces

- Confirm **both** files were edited (producer inject + consumer extract)
- Confirm you ran **`make fix-rabbitmq`** (rebuilds both images — restart alone is not enough)
- Verify both health endpoints show `"propagation": true`
- Generate **new** orders after the fix

### Potential Issue 2. Only payment-api health is true

The consumer stub must be replaced with `extractTraceContext()` - fixing only the producer is not sufficient.

### Potential Issue 3. Alternate pattern: auto-instrumentation

Some teams use **`@opentelemetry/instrumentation-amqplib`** (OpenTelemetry JS contrib) instead of manual inject/extract. 

The failure mode is the same - instrumentation disabled or misconfigured - but the issue is resolved by enabling the library in `instrumentation.js` rather than editing publish/consume code. 

This workshop uses raw `amqplib` because that is still common in Node.js services and makes the inject/extract contract explicit.

---
