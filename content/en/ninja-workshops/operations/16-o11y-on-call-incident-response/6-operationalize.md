---
title: Operationalize the Pattern
linkTitle: 6. Operationalize
weight: 6
time: 5 minutes
description: Turn the workshop workflow into a production-ready operating model.
---

## Production Checklist

Use this checklist when adopting the workflow for real services:

| Area | Standard |
| --- | --- |
| Service ownership | Every paging detector maps to one owning team. |
| Routing keys | Routing keys represent services or teams, not people. |
| Severity | Critical pages humans immediately; lower severities use lower-noise channels. |
| Detector quality | Every paging detector has a sustained condition and a previewed alert count. |
| Alert payload | The message includes impact, trigger, dimensions, dashboard, and runbook. |
| Clear path | Recovery notifications are enabled and responders know how incidents close. |
| Muting | Maintenance windows use muting rules instead of disabling detectors permanently. |
| Review | Noisy alerts are reviewed after every incident or weekly on-call review. |

## Recommended Routing Model

Start with one routing key per major ownership boundary:

```text
checkout
payments
search
platform
database
network
```

For large teams, split by severity or operating model:

```text
checkout-critical
checkout-business-hours
platform-critical
platform-waiting-room
```

Use waiting-room or delayed escalation policies for conditions that often auto-resolve. Use immediate escalation for customer-impacting failures.

## Detector Design Patterns

Prefer detectors that combine a symptom with duration:

* Error rate above threshold for 5 minutes.
* Latency above service objective for 5 minutes.
* Synthetic journey failure from multiple locations.
* Resource saturation plus service impact.

Avoid detectors that page on isolated symptoms:

* Single container restart.
* One host CPU spike.
* One failed request.
* One transient cloud API error.

## Alert Message Template

Use this template for production detector messages:

```text
Summary:
<service> is experiencing <symptom>.

Impact:
<what users or dependencies might experience>

Trigger:
- Detector: {{{detectorName}}}
- Rule: {{{ruleName}}}
- Severity: {{ruleSeverity}}
- Condition: {{{readableRule}}}
- Value: {{inputs.A.value}}
- Dimensions: {{{dimensions}}}

First response:
1. <first dashboard or service view>
2. <first trace, log, or infrastructure pivot>
3. <rollback, scale, reroute, or escalation instruction>

Runbook:
<runbook URL>
```

## Metrics to Track

After adopting the workflow, track these operating metrics:

| Metric | Why it matters |
| --- | --- |
| Alert volume by service | Finds noisy services and detectors. |
| Acknowledgement time | Measures whether paging reaches the right responder. |
| Reroute rate | Shows ownership or routing-key issues. |
| Auto-resolve rate | Identifies alerts that may need a waiting room. |
| MTTR by incident type | Measures whether observability context improves recovery. |

## Wrap-up

The value of this workflow is not just that an alert can create an incident. The value is that detection, routing, response ownership, and investigation context are connected:

* Observability Cloud detects and explains the technical symptom.
* Splunk On-Call routes the incident and coordinates human response.
* The responder starts with service context, not a generic page.
* Teams can review the incident timeline and improve the detector or runbook.

