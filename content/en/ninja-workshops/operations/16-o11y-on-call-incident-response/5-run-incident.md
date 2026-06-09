---
title: Run the Incident
linkTitle: 5. Run Incident
weight: 5
time: 10 minutes
description: Trigger the detector, receive the Splunk On-Call incident, and complete the responder workflow.
---

## Goal

In this section, you will trigger or simulate the detector condition and follow the incident from Observability Cloud into Splunk On-Call.

## 1. Trigger or Simulate the Condition

Use one of these options:

| Option | When to use it |
| --- | --- |
| Lower the detector threshold temporarily | Fastest option for a workshop or demo org. |
| Generate load against the application | Best for a realistic APM or infrastructure incident. |
| Break a non-production dependency | Useful for synthetic or end-to-end journey tests. |
| Use existing sample data | Good when attendees do not have admin access to workloads. |

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
3. If this is an APM signal, open **APM > Service map** and select the affected service.
4. Open **Trace Analyzer** and filter for slow or erroring traces.
5. If this is an infrastructure signal, open the relevant host, Kubernetes workload, or navigator.
6. Check related dashboards for recent deploys, dependency changes, or resource saturation.

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

Return the threshold to its normal value or stop the workload issue. Confirm that Observability Cloud sends a clear notification. Then confirm the Splunk On-Call incident timeline shows recovery context or resolve the incident manually if your workflow requires manual closure.

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

