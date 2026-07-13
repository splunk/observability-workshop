---
title: Redeploy after NGINX fix
weight: 1
time: 5 minutes

---

## Redeploy After Saving

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

## Validation Checklist

Run these commands after redeploy completes.

#### 1. Confirm gateway pod restarted

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

#### 2. Confirm ConfigMap contains trace headers

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

#### 3. Confirm traceparent reaches order-api

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

###$ 4. Generate new browser traffic

Place 2–3 new orders in the shop using a **fresh incognito window** or hard-refresh (Cmd+Shift+R).

## Troubleshooting

Here's some of the potential issues you may encounter in this step & suggested remediation steps.

{{< details summary="Click here for Troubleshooting Guidance" >}}

#### Potential Issue 1: Traces still disconnected after fix

- Confirm you **saved** `deploy/k8s/gateway-config.yaml` and ran **`make fix-nginx`** (or the manual `kubectl apply` + restart commands)
- Confirm the gateway pod restarted: `kubectl -n cosmic-shop get pods -l app=gateway`
- Verify the ConfigMap: `kubectl -n cosmic-shop get configmap gateway-nginx-config -o yaml | grep traceparent`
- Verify inside the pod: `kubectl -n cosmic-shop exec deploy/gateway -- cat /etc/nginx/conf.d/default.conf`
- Generate **new** traffic - old traces won't change retroactively

#### Potential Issue 2: ConfigMap updated but pod still shows old config

NGINX does not hot-reload ConfigMap volume changes on an existing pod. Always **`rollout restart deployment/gateway`** after editing the YAML.

#### Potential Issue 3: CORS preflight stripping headers

If you add CORS to NGINX, ensure `traceparent` and `tracestate` are in `Access-Control-Allow-Headers`:

```nginx
add_header Access-Control-Allow-Headers 'Content-Type, traceparent, tracestate, baggage';
```
{{< /details >}}

