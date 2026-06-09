---
title: 4. Enrich Observability Data
weight: 4
time: 25 minutes
---

Splunk Observability Cloud can troubleshoot technical services without business attributes, but ITSI business impact improves when the alert payload already carries business context.

This lab enriches spans in the Splunk collector with the transform processor in:

```text
workshop/observing-business-journeys/values/splunk-otel-collector-values.yaml
```

## Attribute Strategy

| Attribute | Purpose | Example |
|---|---|---|
| `business.application` | Groups all services under the business application. | `astronomy-shop` |
| `business.capability` | Groups technical services by business capability. | `checkout` |
| `business.transaction` | Names the customer or business transaction. | `Complete Checkout` |
| `business.criticality` | Drives detector severity and ITSI importance. | `critical` |

## Collector Rules

The collector adds default business application context to every span, then stamps transaction context when it sees known routes or supporting services.

Example rule:

```yaml
- set(attributes["business.application"], "astronomy-shop")
- set(attributes["business.transaction"], "Complete Checkout") where attributes["http.route"] == "/api/checkout"
- set(attributes["business.capability"], "checkout") where resource.attributes["service.name"] == "checkout"
- set(attributes["business.criticality"], "critical") where attributes["business.transaction"] == "Complete Checkout"
```

## Verify in APM

Generate traffic by browsing the shop or by leaving the load generator running. Then:

1. Open **APM** in Splunk Observability Cloud.
2. Select the `business-journey-workshop` environment.
3. Open **Traces** and search for `business.application = astronomy-shop`.
4. Open traces for catalog, cart, and checkout flows.
5. Confirm spans include the expected business attributes.

## Create MetricSets

Create APM MetricSets for these span tags:

| Tag | MetricSet type | Why |
|---|---|---|
| `business.application` | Troubleshooting | Filter traces and Tag Spotlight by application. |
| `business.capability` | Troubleshooting and Monitoring | Build dashboards and detectors by capability. |
| `business.transaction` | Troubleshooting and Monitoring | Alert on journey health and route alerts to ITSI. |
| `business.criticality` | Troubleshooting and Monitoring | Split detectors and notifications by impact tier. |

In Splunk Observability Cloud:

1. Go to **Settings** then **APM & RUM MetricSets**.
2. Select the **APM** tab.
3. Add a custom MetricSet for each tag.
4. Enable **Also create Monitoring MetricSet** for `business.transaction`, `business.capability`, and `business.criticality`.

{{% notice title="Workshop Note" style="info" %}}
MetricSet analysis can take several minutes. If you are running this with a group, the instructor can create MetricSets once for the shared organization.
{{% /notice %}}
