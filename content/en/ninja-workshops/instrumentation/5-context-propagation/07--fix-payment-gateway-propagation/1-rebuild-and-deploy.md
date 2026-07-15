---
title: ReDeploy Gateway fix
weight: 1
time: 5 minutes

---

## Rebuild and Redeploy After Saving

{{% notice title="Note" style="info" %}}
Saving `server.js` does **not** update running pods until you rebuild and restart.
{{% /notice %}}

From the project root:

```bash
bash scripts/build-images.sh payment-gateway
bash scripts/import-images-k3d.sh payment-gateway
kubectl -n cosmic-shop rollout restart deployment/payment-gateway
kubectl -n cosmic-shop rollout status deployment/payment-gateway --timeout=180s
```

## Validation Checklist

Run these commands after redeploy completes.

#### 1. Confirm health endpoint reports propagation

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop exec deploy/payment-gateway -- wget -qO- http://localhost:3004/health
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{"status":"ok","service":"payment-gateway","stage":"proxy","propagation":true}
```

The health check probes whether `buildUpstreamHeaders()` adds a `traceparent` header when a span is active - it flips to `true` automatically once you add `propagation.inject()`.

{{% /tab %}}
{{< /tabs >}}

#### 2. Place a test order and inspect traces

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s -X POST http://localhost:30080/api/purchases \
  -H "Content-Type: application/json" \
  -d '{"productId":"telescope-orion-8","quantity":1,"customerEmail":"gateway-test@cosmic.shop"}' \
  | python3 -m json.tool
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
    "message": "Purchase complete \u2014 order placed and payment submitted for fulfillment",
    "order": {
        "orderId": "ORD-1783667419611",
        "productId": "telescope-orion-8",
        "productName": "Orion 8\" Dobsonian Telescope",
        "quantity": 1,
        "total": 449.99,
        "customerEmail": "gateway-test@cosmic.shop",
        "createdAt": "2026-07-10T07:10:19.611Z",
        "requestTraceId": "6891d2d87734d4959214491bb2c600af"
    },
    "payment": {
        "paymentId": "PAY-1783667419703",
        "orderId": "ORD-1783667419611",
        "amount": 449.99,
        "status": "authorized",
        "method": "stellar-credits",
        "processedAt": "2026-07-10T07:10:19.703Z"
    }
}
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Note" style="info" %}}
This workshop uses a Node.js proxy so you practice **application-layer** propagation bugs (common in BFFs and custom gateways). The NGINX ConfigMap approach from Step 06 applies when the break is at the **infrastructure proxy** layer instead.
{{% /notice %}}

## Troubleshooting

{{< details summary="Click here for Troubleshooting Guidance" >}}
#### Potential Issue 1. Traces still disconnected after fix

- Confirm you **saved** `services/payment-gateway/server.js` and ran **`make fix-payment-gateway`** (rebuild + import + restart)
- Confirm the pod restarted with a recent AGE: `kubectl -n cosmic-shop get pods -l app=payment-gateway`
- Verify health shows `"propagation": true`
- Generate **new** traffic - old traces won't change retroactively

#### Potential Issue 2. Health still shows `"propagation": false`

- Confirm `propagation.inject()` is inside `buildUpstreamHeaders()` and runs **before** `return headers`
- Confirm you removed `suppressTracing()` from the upstream fetch path
- Re-run the full rebuild chain - a restart alone is not enough if the image was not rebuilt

#### Potential Issue 3. If gateway setup is using NGINX / ConfigMap proxy 

Some teams implement payment routing with an **API gateway or NGINX sidecar** instead of a Node.js proxy. The failure mode is identical to Step 06: missing `proxy_set_header traceparent` directives.

If your organization uses that pattern, the fix would be a **ConfigMap** change to (`gateway-config.yaml`) rather than JavaScript:

```nginx
location /payments/ {
    proxy_set_header Host $host;
    proxy_set_header traceparent $http_traceparent;
    proxy_set_header tracestate $http_tracestate;
    proxy_set_header baggage $http_baggage;
    proxy_pass http://payment_api;
}
```
{{< /details >}}
