---
title: Fix NGINX Propagation
linkTitle: 06. Fix NGINX Propagation
weight: 6
time: 15 minutes
description: In this step, you'll **edit** the edge gateway NGINX configuration to forward W3C Trace Context headers, then **redeploy** the gateway so the change takes effect. That restores correlation between Splunk RUM and your backend APM traces for the order path.

---

{{% notice title="Note" style="info" %}}
The workshop runs **two separate NGINX instances**. Only the **edge gateway** will be changed in this step.

#### Why only the edge gateway?

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

## The Fix

We now need to add explicit forwarding for the three W3C context headers in each `location` block:

These directives tell NGINX to pass the incoming trace context from the client (Splunk RUM) through to the upstream service.

## Apply the Fix

```
vi deploy/k8s/gateway-config.yaml 
```

Locate the **`location /api/`** block inside the `default.conf` section (the indented NGINX config under `data:`) and add explicit forwarding for the three W3C context headers **after** the standard `proxy_set_header` lines and **before** `proxy_http_version` / `proxy_pass`

```nginx
proxy_set_header traceparent $http_traceparent;
proxy_set_header tracestate $http_tracestate;
proxy_set_header baggage $http_baggage;
```


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

{{% notice title="Note" style="green" icon="running" %}}
These directives tell NGINX to pass the incoming trace context from `frontend-api` through to `order-api`.
{{% /notice %}}
