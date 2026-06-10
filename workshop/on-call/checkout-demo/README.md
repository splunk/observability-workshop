# On-Call Workshop Checkout Demo App

This app supports the **Observability Cloud and On-Call** workshop. It gives students a small service graph that can create real APM traces, custom metrics, latency, and errors for detector and Splunk On-Call testing.

## Services

```text
checkout-loadgen -> checkout-service /checkout -> inventory-service /reserve
                                      |
                                      v
                         Splunk OpenTelemetry Collector
                                      |
                                      v
                         Splunk Observability Cloud
```

The app has three containers:

| Service | Purpose |
| --- | --- |
| `checkout-service` | Customer-facing service. Emits checkout traces and custom metrics. |
| `inventory-service` | Downstream dependency. Can run healthy, slow, erroring, or both. |
| `loadgen` | Continuously calls checkout so Observability Cloud has live data. |

The Compose stack also runs `splunk-otel-collector`, which forwards traces and metrics to Splunk Observability Cloud.

## Telemetry

APM services:

```text
checkout-service
inventory-service
checkout-loadgen
```

Custom metrics:

```text
workshop.checkout.requests
workshop.checkout.errors
workshop.checkout.latency_ms
```

Useful dimensions:

```text
deployment.environment=on-call-workshop
app.workshop=on-call-incident-response
app.cart.type
app.issue_mode
http.response.status_code
status
```

## Prerequisites

You need:

* Docker with Docker Compose.
* A Splunk Observability Cloud realm, such as `us0`, `us1`, or `eu0`.
* A Splunk Observability Cloud access token that can ingest traces and metrics.

## Configure

```bash
cd workshop/on-call/checkout-demo
cp .env.example .env
```

Edit `.env`:

```text
SPLUNK_REALM=us1
SPLUNK_ACCESS_TOKEN=<your-observability-access-token>
ENVIRONMENT=on-call-workshop
```

## Start

```bash
./scripts/start.sh
```

Open the local scenario endpoint:

```bash
curl http://127.0.0.1:18080/scenario
```

Send a few manual requests:

```bash
./scripts/smoke-test.sh
```

The `loadgen` container sends ongoing checkout traffic once the stack is running.

## Find the App in Observability Cloud

In Splunk Observability Cloud:

1. Open **APM**.
2. Search for `checkout-service`.
3. Confirm the service map shows `checkout-service` calling `inventory-service`.
4. Open **Metric Finder** or a new chart.
5. Search for `workshop.checkout.errors`.
6. Filter by `deployment.environment:on-call-workshop` if your org has other workshop traffic.

## Create the Detector Signal

Use `workshop.checkout.errors` for the workshop detector.

Suggested detector logic:

| Setting | Value |
| --- | --- |
| Metric | `workshop.checkout.errors` |
| Filter | `deployment.environment:on-call-workshop` |
| Analytics | Sum, then rate per second or sum over a short window |
| Condition | Greater than `0` for a fast demo, or greater than `5` over 5 minutes for a quieter lab |
| Severity | Critical |
| Recipient | `VictorOps` / Splunk On-Call integration |
| Routing key | The routing key created in Splunk On-Call |

For a latency detector, use `workshop.checkout.latency_ms` and alert when p95 is greater than `1500` ms for several minutes.

## Inject an Incident

Create latency and errors:

```bash
./scripts/inject-issue.sh latency-errors
```

Other modes:

```bash
./scripts/inject-issue.sh latency
./scripts/inject-issue.sh errors
./scripts/inject-issue.sh healthy
```

Expected behavior:

* `latency`: inventory sleeps before responding.
* `errors`: inventory returns intermittent `503` errors.
* `latency-errors`: inventory is slow and intermittently returns `503`.
* `healthy`: inventory returns to normal.

## Resolve the Incident

```bash
./scripts/remediate.sh
```

Wait for the detector to clear, then resolve or confirm recovery in Splunk On-Call.

## Stop

```bash
./scripts/stop.sh
```

## Troubleshooting

Check local app health:

```bash
curl http://127.0.0.1:18080/health
curl http://127.0.0.1:18081/health
```

Check container status:

```bash
docker compose ps
docker compose logs -f checkout-service inventory-service loadgen
```

Check collector logs:

```bash
docker compose logs -f splunk-otel-collector
```

If telemetry does not appear in Observability Cloud:

* Confirm `SPLUNK_REALM` is correct.
* Confirm `SPLUNK_ACCESS_TOKEN` is an Observability Cloud ingest token.
* Confirm Docker can reach `https://ingest.<realm>.signalfx.com`.
* Wait 1 to 3 minutes for APM and metric indexes to populate.
