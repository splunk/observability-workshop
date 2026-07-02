---
title: Fix NGINX Propagation
linkTitle: 06. Fix NGINX Propagation
weight: 2
time: 15 minutes
description: In this step, you'll **edit** the edge gateway NGINX configuration to forward W3C Trace Context headers, then **redeploy** the gateway so the change takes effect. That restores correlation between Splunk RUM and your backend APM traces for the order path.

---

{{% notice title="Note" style="info" %}}
The workshop runs **two separate NGINX instances**. Only the **edge gateway** will be changed in this step.

### Why only the edge gateway?

Because this is the Order traffic path (where break #1 occurs):

```
Browser
  → Frontend NGINX (port 30080, NodePort)
    → frontend-api (Node.js BFF)
      → Edge Gateway NGINX (ClusterIP service gateway:80)   ← We are applying the fixes here
        → order-api:3001
```

So trace headers for `/api/purchases` must survive **frontend-api → gateway → order-api**. The edge gateway is dropping `traceparent`, `tracestate`, and `baggage` on the proxy hop to `order-api`.

{{% /notice %}}
---

## The fix



We now need to add explicit forwarding for the three W3C context headers in each `location` block:

```nginx
proxy_set_header traceparent $http_traceparent;
proxy_set_header tracestate $http_tracestate;
proxy_set_header baggage $http_baggage;
```

These directives tell NGINX to pass the incoming trace context from the client (Splunk RUM) through to the upstream service.

---

## Apply the fix

```
vi ~/deploy/k8s/gateway-config.yaml 
```

Locate the **`location /api/`** block inside the `default.conf` section (the indented NGINX config under `data:`).

Add explicit forwarding for the three W3C context headers **after** the standard `proxy_set_header` lines and **before** `proxy_http_version` / `proxy_pass`:

```nginx
    # W3C Trace Context propagation
    proxy_set_header traceparent $http_traceparent;
    proxy_set_header tracestate $http_tracestate;
    proxy_set_header baggage $http_baggage;
```

These directives tell NGINX to pass the incoming trace context from `frontend-api` through to `order-api`.

---

## Before and after

{{% notice title="Note" style="info" %}}
Only the **`location /api/`** block on the **edge gateway** is updated (not the frontend NGINX).
{{% /notice %}}

{{< tabs >}}
{{% tab title="Before" %}}

```nginx
        location /api/ {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_pass http://order_api;
        }
```

{{% /tab %}}
{{% tab title="After" %}}

```nginx
        location /api/ {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # W3C Trace Context propagation
            proxy_set_header traceparent $http_traceparent;
            proxy_set_header tracestate $http_tracestate;
            proxy_set_header baggage $http_baggage;

            proxy_http_version 1.1;
            proxy_pass http://order_api;
        }
```

{{% /tab %}}
{{< /tabs >}}

---

## Redeploy after saving

Saving the file does **not** update the running gateway. You must apply the ConfigMap and restart the deployment so NGINX loads the new config.

From the project root run the following:

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl apply -f deploy/k8s/gateway-config.yaml
kubectl -n cosmic-shop rollout restart deployment/gateway
kubectl -n cosmic-shop rollout status deployment/gateway --timeout=180s
```

Verify the pod picked up your changes:

```bash
kubectl -n cosmic-shop exec deploy/gateway -- grep traceparent /etc/nginx/conf.d/default.conf
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
proxy_set_header traceparent $http_traceparent;
```

{{% /tab %}}
{{< /tabs >}}

---

## Validation checklist

Run these commands after redeploy completes.

### 1. Confirm gateway pod restarted

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop rollout status deployment/gateway
kubectl -n cosmic-shop get pods -l app=gateway
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
deployment "gateway" successfully rolled out

NAME                       READY   STATUS    RESTARTS   AGE
gateway-xxxxxxxxxx-xxxxx   1/1     Running   0          30s
```

AGE should be recent (pod was recreated after config change).

{{% /tab %}}
{{< /tabs >}}

### 2. Confirm ConfigMap contains trace headers

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop get configmap gateway-nginx-config -o yaml | grep traceparent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
  proxy_set_header traceparent $http_traceparent;
```

You should see `traceparent`, `tracestate`, and `baggage` in the output.

{{% /tab %}}
{{< /tabs >}}

### 4. Confirm traceparent reaches order-api

Send a request **through the edge gateway** with a known trace header:

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop port-forward svc/gateway 8888:80 &
sleep 2

TRACE_ID="deadbeefdeadbeefdeadbeefdeadbeef"
curl -s -H "traceparent: 00-${TRACE_ID}-deadc0dedeadbeef-01" \
  -X POST http://localhost:8888/api/orders \
  -H "Content-Type: application/json" \
  -d '{"productId":"eyepiece-plossl-set","quantity":1,"customerEmail":"trace-test@cosmic.shop"}' \
  | python3 -m json.tool

kill %1 2>/dev/null
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
    "message": "Order created",
    "order": { "orderId": "ORD-...", ... },
    "traceHint": {
        "traceId": "deadbeefdeadbeefdeadbeefdeadbeef",
        ...
    }
}
```

The `traceHint.traceId` should match the trace ID you sent in the `traceparent` header -  confirming the gateway forwarded it to `order-api`.

{{% /tab %}}
{{< /tabs >}}

### 5. Generate new browser traffic

Place 2–3 new orders in the shop using a **fresh incognito window** or hard-refresh (Cmd+Shift+R).

### 6. Confirm partial correlation in Splunk

| Check | Expected after NGINX fix |
|-------|--------------------------|
| RUM "Backend Trace" link on checkout | **Visible** |
| payment-api / fulfillment-worker in same trace | **No — still broken** |

In **APM → Traces** view, open a recent `order-api` `POST /api/orders` trace. The order span should share a trace ID with the browser/RUM session after this fix.

---
