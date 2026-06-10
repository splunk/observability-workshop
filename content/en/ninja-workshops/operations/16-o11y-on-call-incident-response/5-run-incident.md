---
title: Run the Incident
linkTitle: 6. Run Incident
weight: 6
time: 10 minutes
description: Trigger the detector, receive the Splunk On-Call incident, and complete the responder workflow.
---

## Goal

In this section, you will trigger or simulate the detector condition and follow the incident from Observability Cloud into Splunk On-Call.

## 1. Trigger the Demo App Condition

From the demo app directory, inject the issue:

```bash
cd workshop/on-call/checkout-demo
./scripts/inject-issue.sh latency-errors
```

The load generator is already calling `checkout-service`. After issue injection, `inventory-service` becomes slow and intermittently returns `503` responses. That causes `checkout-service` to emit `workshop.checkout.errors`.

Wait for the detector to evaluate. In Observability Cloud, open **Alerts & Detectors** and confirm the alert appears in active alerts.

## 2. Acknowledge in Splunk On-Call

1. Open Splunk On-Call.
2. Find the new incident routed to your team.
3. Confirm the incident was routed through the expected routing key.
4. Acknowledge the incident.

Acknowledgement stops paging for that incident and assigns ownership to the responder.

## 3. Inspect the Incident Payload

Open the incident details and review:

* Detector name.
* Rule name.
* Severity.
* Triggering condition.
* Dimensions or entity details.
* Runbook or dashboard link.
* Incident timeline.

The responder should be able to answer these questions from the payload:

* What service or entity is impacted?
* What condition triggered the incident?
* How long has it been happening?
* Where should investigation begin?
* Who owns the next action?

## 4. Investigate in Observability Cloud

Use the alert context to pivot into Observability Cloud:

1. Open the active alert or detector.
2. Review the chart and dimensions that triggered the alert.
3. Open **APM > Service map** and select `checkout-service`.
4. Confirm `checkout-service` calls `inventory-service`.
5. Open **Trace Analyzer** and filter for slow or erroring traces.
6. Look for the `checkout.reserve_inventory` span and the `inventory-service` `503` responses.

## 5. Practice Incident Actions

In Splunk On-Call, practice the actions responders use during a real incident:

| Action | Use it when |
| --- | --- |
| Acknowledge | You are taking ownership of first response. |
| Add responder | Another person or team needs to help. |
| Reroute | The incident belongs to another team. |
| Snooze | The incident is known and should pause temporarily. |
| Resolve | No further response action is required. |

## 6. Clear and Resolve

Return the app to healthy mode:

```bash
./scripts/remediate.sh
```

Confirm that Observability Cloud sends a clear notification. Then confirm the Splunk On-Call incident timeline shows recovery context or resolve the incident manually if your workflow requires manual closure.

## Debrief

Discuss the incident with the group:

* Was the detector actionable?
* Did the routing key send the incident to the right team?
* Did the payload include enough context?
* Was the first investigation step obvious?
* What should be changed before using this pattern in production?

## Reference

* [Getting started guide for Splunk On-Call users](https://help.splunk.com/en/splunk-cloud-platform/alert-and-respond/splunk-on-call/user-management/getting-started-guide-for-splunk-on-call-users)
* [Reroute incidents in Splunk On-Call](https://help.splunk.com/en/splunk-cloud-platform/alert-and-respond/splunk-on-call/incidents/re-route-incidents)
