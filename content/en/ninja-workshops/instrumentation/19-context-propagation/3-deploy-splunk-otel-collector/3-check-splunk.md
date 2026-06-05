---
title: 3. Check Splunk
weight: 3
---

## Confirm Infrastructure Metrics in Splunk

{{% notice title="Note" style="green" icon="running" %}}

Allow **2–5 minutes** after deploy for infrastructure metrics to appear..

{{% /notice %}}

1. Open **Infrastructure → Kubernetes** (or **Infrastructure Monitoring**)
2. Filter by cluster **`trace-workshop`** (`k8s.cluster.name`)
3. Confirm node CPU/memory and pod metrics (for example `k8s.node.*`, `k8s.pod.*`, `system.cpu.*`)

{{% notice title="Note" style="grey" icon="running" %}}
All infrastructure metrics are tagged with `k8s.cluster.name=trace-workshop-<your-Initials>` (from `K8S_CLUSTER_NAME` in `workshop-config` ConfigMap).
{{% /notice %}}

If infrastructure metrics are missing:

| Check | Action |
|-------|--------|
| Agent DaemonSet | `kubectl get pods -n trace-workshop -l app=splunk-otel-collector-agent` — all Ready |
| Agent logs | `kubectl logs daemonset/splunk-otel-collector-agent -n trace-workshop` — no kubelet TLS errors |
| RBAC | ServiceAccount `splunk-otel-collector` has ClusterRole `splunk-otel-collector-workshop` |
| Token | Ingest token must include **Infrastructure Monitoring** permissions |
| Cluster filter | Set **k8s.cluster.name** = `trace-workshop` in Splunk IMM |


## Confirm APM Data in Splunk

1. Open **APM → Services**
2. Set **Environment** to your `WORKSHOP_ENV` value (for example `trace-propagation-workshop`)
3. Confirm **storefront-service**, **payment-proxy**, and **inventory-service** are listed

If services do not appear:

| Check | Action |
|-------|--------|
| Token | Use an **ingest** access token with APM permissions (not a RUM-only token) |
| Realm | Match `SPLUNK_REALM` to your org (US0 → `us0`, EU0 → `eu0`) |
| Environment filter | In APM, set **Environment** = your `WORKSHOP_ENV` |
| Time range | Set to **Last 15 minutes** after generating traffic |
| Collector logs | `kubectl logs deployment/splunk-otel-collector -n trace-workshop` |
| Traces pipeline | Config must use `otlphttp` to `https://ingest.<realm>.signalfx.com/v2/trace/otlp` |

## Observe ServiceMap & Traces in Splunk APM (Phase 1)

1. Open **APM → Traces**
2. Set **Environment** to `trace-propagation-workshop` (or your `WORKSHOP_ENV`)
3. Filter service: **storefront-service** and open a trace waterfall

### What you should see after the collector is live

| Hop | Splunk trace behavior |
|-----|----------------------|
| **storefront → inventory-service** | **Correlated** — spans for both services appear in the **same trace** |
| **storefront → payment-service** | **Not correlated** — `payment-service` appears as a **separate root trace** |
| **payment-proxy** | Usually in the **same trace as storefront** (inbound from storefront); the break is on the **outbound** hop to payment |
| **payment-service → order-service** | **Correlated** — HTTP from payment to order links in **one trace** (payment’s root trace) |
| **order-service → RabbitMQ → fulfilment-service** | **RabbitMQ shows as an inferred service** on the order trace (publish/receive spans with `messaging.system=rabbitmq`, `server.address=rabbitmq`). **order and fulfilment traces stay disconnected** — no trace context on AMQP messages in Phase 1 |


{{% notice title="Exercise" style="green" icon="running" %}}

This asymmetry is intentional: HTTP auto-instrumentation can propagate context where headers survive, but the **message bus** does not carry trace context until you fix it in Phase 2 (Steps 7–8).

{{% /notice %}}

### Why traces connect or break

{{% notice title="Note" style="info" %}}
In **APM → Service map**, dependencies appear even when Trace Analyzer waterfalls are disconnected on the payment leg.
{{% /notice %}}

| Hop | What happens |
|-----|----------------|
| Client → edge proxy | `traceparent` removed before storefront |
| Storefront → **inventory** (direct HTTP) | `filter_headers_for_mode()` removes headers from `inject_outbound_headers()`, but the Splunk OTel **`requests` auto-instrumentation** still injects W3C `traceparent`. **inventory-service** (`auto` mode) extracts W3C — traces link. |
| Storefront → **payment-proxy** | Same `requests` instrumentation may link storefront and payment-proxy on the inbound hop |
| **payment-proxy → payment-service** | Proxy **strips** W3C and `X-Workshop-Trace` and uses `suppress_instrumentation()` — **payment-service** starts a **new trace root** |
| **payment-service → order-service** (HTTP) | Payment calls order with `inject_outbound_headers()` plus **`requests` auto-instrumentation**; order-service extracts on inbound HTTP — **same trace as payment** |
| **order-service → RabbitMQ** | Order emits **PRODUCER/CONSUMER** spans with Splunk messaging tags (`messaging.destination.name`, `server.address`) so **RabbitMQ appears as an inferred service** in the trace waterfall |
| **RabbitMQ → fulfilment-service** | Phase 1: **no trace headers** on messages; pika auto-instrumentation disabled; fulfilment consumer uses a **new root** unless Step 7 publishes carriers |
| Fulfilment → email | Separate roots continue until Phase 2 Steps 7–9 |
