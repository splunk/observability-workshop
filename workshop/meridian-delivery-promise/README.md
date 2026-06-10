# Meridian Delivery Promise App

This app supports the **Business Case Story** chapter in the ITSI alerting and monitoring workshop.

It models a specialty pharmacy that promises refrigerated medication deliveries inside a patient delivery window. The app is intentionally small, but it produces realistic service names and request paths for Splunk Observability Cloud and ITSI:

```text
meridian-loadgen
  -> patient-confirmation
      -> route-planner-api
          -> geocoding-provider
      -> courier-mobile-api
      -> notification-gateway
```

## What It Demonstrates

- A business service called `Medication Delivery Promise`.
- A patient-facing confirmation flow with backend dependencies.
- Degradation modes that create latency, queue risk, and frontend slowness.
- OpenTelemetry-ready service names and business attributes for APM.
- Simple incident toggles that align to ITSI KPIs, dependencies, episodes, and glass tables.

## Quick Start Without Splunk Credentials

This mode runs the app locally and disables trace export.

```bash
cd workshop/meridian-delivery-promise
cp .env.example .env
docker compose up -d --build
./scripts/smoke-test.sh
```

Open the patient portal:

```text
http://localhost:8090
```

## Send Telemetry to Splunk Observability Cloud

Edit `.env`:

```bash
OTEL_TRACES_EXPORTER=otlp
SPLUNK_REALM=us1
SPLUNK_ACCESS_TOKEN=<your-access-token>
```

Start the collector profile:

```bash
docker compose --profile o11y up -d --build
```

In Splunk APM, look for these services:

- `patient-confirmation`
- `route-planner-api`
- `geocoding-provider`
- `courier-mobile-api`
- `notification-gateway`
- `meridian-loadgen`

Useful span attributes:

| Attribute | Example |
|---|---|
| `business.service` | `Medication Delivery Promise` |
| `business.transaction` | `patient-delivery-confirmation` |
| `business.capability` | `Route Planning` |
| `business.criticality` | `high` |
| `delivery.region` | `north-hub` |
| `delivery.window` | `08:00-10:00` |
| `delivery.priority` | `cold-chain` |
| `app.issue_mode` | `geocode-latency` |

## Incident Modes

Use the script:

```bash
./scripts/set-incident.sh healthy
./scripts/set-incident.sh geocode-latency
./scripts/set-incident.sh queue-backlog
./scripts/set-incident.sh patient-portal-slow
```

Or use the buttons in the portal.

| Mode | Story effect | ITSI concept to teach |
|---|---|---|
| `healthy` | Normal delivery confirmations | Baseline service health |
| `geocode-latency` | Route planning slows because the geocoding dependency is slow | Dependency and KPI rollup |
| `queue-backlog` | The route planner is working, but dispatch risk is growing | Queue-age KPI and early warning |
| `patient-portal-slow` | Backend services are healthy, but patient pages are slow | User experience as a service KPI |

## Suggested ITSI Model

Parent service:

```text
Medication Delivery Promise
```

Child services:

```text
Patient Confirmation
Route Planning
Courier Updates
Patient Notifications
```

Starter KPIs:

| KPI | Source idea |
|---|---|
| Route planner p95 latency | APM service latency for `route-planner-api` |
| Oldest pending route age | `/api/summary` or simulated event payload |
| Delivery confirmation success rate | Patient confirmation request success |
| Patient portal page load p95 | Optional RUM metric |
| At-risk routes | `/api/summary` or simulated event payload |

## Demo ITSI Events

If direct Observability Cloud detector integration is not ready, use the app output as the basis for small HEC events into Splunk platform. The endpoint below gives simple values that map well to KPI searches:

```bash
curl -s http://localhost:8090/api/summary | jq
```

## Cleanup

```bash
./scripts/cleanup.sh
```
