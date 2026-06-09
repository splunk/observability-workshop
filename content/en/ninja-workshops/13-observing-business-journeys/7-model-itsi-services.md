---
title: 7. Model ITSI Services
weight: 7
time: 30 minutes
---

In ITSI, model the customer journey as business services and the microservices as impacting technical services. This gives incident leaders a top-down view while preserving the technical path to root cause.

## Service Model

Create these business services:

| ITSI service | Type | Depends on | Importance |
|---|---|---|---|
| Astronomy Shop Revenue | Business application | Browse Catalog, Manage Cart, Complete Checkout, Confirm Order | Top-level service |
| Browse Catalog | Business transaction | `frontend`, `product-catalog`, `recommendation`, `ad`, `currency` | Medium |
| Manage Cart | Business transaction | `frontend`, `cart`, `valkey-cart` | High |
| Complete Checkout | Business transaction | `frontend`, `checkout`, `payment`, `shipping`, `currency`, `cart` | Critical |
| Confirm Order | Business transaction | `email`, `accounting`, `kafka`, `postgresql` | High |

Use service dependencies so the top-level service health reflects the transaction services. Give `Complete Checkout` higher importance because it maps directly to revenue capture.

## KPI Examples

Use the examples in:

```text
workshop/observing-business-journeys/itsi/o11y-alert-kpi-searches.md
```

Recommended KPIs:

| KPI | Service | Source |
|---|---|---|
| Active critical Observability alerts | All transaction services | Splunk platform alert events from Observability Cloud. |
| Latest impacted service | Transaction services | `sflo_dimensions` from alert payload. |
| Estimated revenue at risk | Complete Checkout | Alert state joined with workshop impact model. |
| Alert clear status | Transaction services | Observability Cloud clear notification. |

## Episode Aggregation Policy

Create an aggregation policy for Observability Cloud alerts:

- Filter: `index=o11y_alerts sflo_dimensions`.
- Group by: `business_transaction`, `business_application`, and detector.
- Title: `O11y: $business_transaction$ impact from $sflo_detector$`.
- Severity: map Observability Cloud severity to ITSI severity.
- Break episode when the clear event arrives.

## Glass Table

Build a glass table with:

- One top-level health score for **Astronomy Shop Revenue**.
- Four transaction blocks: **Browse Catalog**, **Manage Cart**, **Complete Checkout**, **Confirm Order**.
- A single value for active alerts.
- A single value for estimated revenue at risk.
- A table of latest impacted technical services.
- A link to the matching Observability Cloud APM dashboard.

{{< tabs >}}
{{% tab title="Question" %}}
Why should ITSI services be modeled as business transactions instead of only Kubernetes deployments?
{{% /tab %}}
{{% tab title="Answer" %}}
Because a Kubernetes deployment is an implementation detail. A business transaction tells responders which customer outcome is degraded and lets technical services roll up into business impact.
{{% /tab %}}
{{< /tabs >}}
