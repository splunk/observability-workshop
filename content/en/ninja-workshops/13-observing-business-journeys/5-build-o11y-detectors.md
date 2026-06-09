---
title: 5. Build O11y Detectors
weight: 5
time: 25 minutes
---

The goal of the detector layer is to catch technical symptoms in Splunk Observability Cloud and send the alert with enough business context for ITSI to group and prioritize it.

Create one detector per important business transaction. Start with checkout, then add catalog and cart.

## Detector Candidates

| Detector | Signal | Filter | Trigger |
|---|---|---|---|
| Checkout latency | `service.request.duration.ns.p99` | `business.transaction:Complete Checkout` | p99 above workshop threshold for 5 minutes. |
| Checkout errors | `service.request.count` split by `sf_error` | `business.transaction:Complete Checkout` | Error rate above workshop threshold for 5 minutes. |
| Cart errors | `service.request.count` split by `sf_error` | `business.transaction:Manage Cart` | Error rate above workshop threshold for 5 minutes. |
| Catalog errors | `service.request.count` split by `sf_error` | `business.transaction:Browse Catalog` | Error rate above workshop threshold for 5 minutes. |

Use a threshold that works for the demo. The point of the workshop is the mapping and alert flow, not production-grade threshold tuning.

## Alert Message Fields

Add the following to the detector description or runbook fields so they are visible in Splunk platform and ITSI:

```text
business.application=astronomy-shop
business.transaction={{business.transaction}}
business.capability={{business.capability}}
business.criticality={{business.criticality}}
service={{sf_service}}
environment={{sf_environment}}
```

Use the detector's available variables and dimensions for your organization. The exact variable picker can differ by detector type.

## Detector Routing

For each detector:

1. Set severity based on `business.criticality`.
2. Add the Splunk platform integration as an alert recipient.
3. Add a runbook URL or dashboard link that points responders back to APM.
4. Activate and save the detector.

## Validation

After the detector is saved, confirm it can send to Splunk platform:

```spl
index=<o11y_alert_index> sflo_dimensions
| table _time sflo_event_type sflo_detector sflo_dimensions
| sort - _time
```

{{% notice title="Design Rule" style="info" %}}
Keep root cause investigation in Observability Cloud. Use ITSI to summarize impact, correlate alerts, create episodes, and present the business view.
{{% /notice %}}
