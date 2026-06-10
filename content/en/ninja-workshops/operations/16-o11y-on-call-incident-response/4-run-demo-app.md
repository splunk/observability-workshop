---
title: Run the Checkout Demo App
linkTitle: 4. Run Demo App
weight: 4
time: 15 minutes
description: Start the included checkout demo app and verify its telemetry in Splunk Observability Cloud.
---

## Goal

In this section, you will run the included checkout demo app. The app sends traces and custom metrics to Splunk Observability Cloud through a local Splunk OpenTelemetry Collector.

The app gives the workshop a real signal for the detector and incident workflow:

```text
checkout-loadgen -> checkout-service -> inventory-service -> Splunk OpenTelemetry Collector -> Splunk Observability Cloud
```

## 1. Locate the App

The app is in this repository:

```bash
cd workshop/on-call/checkout-demo
```

The app includes:

| File or directory | Purpose |
| --- | --- |
| `docker-compose.yml` | Runs the services and Splunk OpenTelemetry Collector. |
| `app/checkout_service.py` | Customer-facing checkout service. |
| `app/inventory_service.py` | Downstream dependency that can inject latency and errors. |
| `app/loadgen.py` | Sends ongoing checkout traffic. |
| `otel-collector/config.yaml` | Sends traces and metrics to Observability Cloud. |
| `scripts/` | Helpers for start, smoke traffic, issue injection, remediation, and shutdown. |

## 2. Configure Splunk Access

Create a local environment file:

```bash
cp .env.example .env
```

Edit `.env` and set:

```text
SPLUNK_REALM=us1
SPLUNK_ACCESS_TOKEN=<your-observability-access-token>
ENVIRONMENT=on-call-workshop
```

{{% notice title="Token type" style="info" %}}
Use a Splunk Observability Cloud access token that can ingest traces and metrics. Do not use a Splunk On-Call API key for this app. Splunk On-Call is used later as the alert recipient.
{{% /notice %}}

## 3. Start the App

Start the stack:

```bash
./scripts/start.sh
```

The script builds the Python app image and starts:

* `splunk-otel-collector`
* `checkout-service`
* `inventory-service`
* `loadgen`

Check the local scenario endpoint:

```bash
curl http://127.0.0.1:18080/scenario
```

Send a few manual requests:

```bash
./scripts/smoke-test.sh
```

## 4. Verify Local Health

Check the services:

```bash
curl http://127.0.0.1:18080/health
curl http://127.0.0.1:18081/health
docker compose ps
```

If a container is unhealthy or restarting, check logs:

```bash
docker compose logs -f checkout-service inventory-service loadgen splunk-otel-collector
```

## 5. Verify Observability Cloud Telemetry

In Splunk Observability Cloud:

1. Open **APM**.
2. Search for `checkout-service`.
3. Confirm the service map shows `checkout-service` calling `inventory-service`.
4. Open **Metric Finder** or create a chart.
5. Search for `workshop.checkout.errors`.
6. Filter by `deployment.environment:on-call-workshop`.

The app emits these custom metrics:

| Metric | Use |
| --- | --- |
| `workshop.checkout.requests` | Request volume. |
| `workshop.checkout.errors` | Failed checkout requests caused by inventory issues. |
| `workshop.checkout.latency_ms` | End-to-end checkout latency. |

Useful dimensions:

| Dimension | Use |
| --- | --- |
| `app.issue_mode` | Shows whether the app is healthy, slow, erroring, or both. |
| `app.cart.type` | Lets you split the signal by cart path. |
| `http.response.status_code` | Separates successful and failed responses. |
| `status` | Separates `success` from `error`. |

{{% notice title="Indexing delay" style="primary" icon="lightbulb" %}}
APM services and custom metrics can take 1 to 3 minutes to appear after the first traffic reaches Observability Cloud.
{{% /notice %}}

## 6. Incident Modes

Do not inject the issue yet if you have not created the detector. You will use these commands in the incident section:

```bash
./scripts/inject-issue.sh latency-errors
./scripts/remediate.sh
```

Available issue modes:

| Mode | Behavior |
| --- | --- |
| `healthy` | Inventory responds normally. |
| `latency` | Inventory sleeps before responding. |
| `errors` | Inventory returns intermittent `503` responses. |
| `latency-errors` | Inventory is slow and intermittently returns `503`. |

## Checkpoint

Before continuing, confirm that:

* `checkout-service` appears in APM.
* The service map shows `inventory-service`.
* `workshop.checkout.errors` is available in Metric Finder or chart search.
* The app is currently in `healthy` mode.
