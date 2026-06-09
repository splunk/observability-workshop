---
title: Use Case and Outcomes
linkTitle: 1. Use Case
weight: 1
time: 5 minutes
description: Define the incident response use case before configuring detectors and paging.
---

## Use Case

The checkout service is a customer-facing dependency. A short latency spike is useful context, but a sustained checkout failure is a business-impacting incident. The operations goal is to page only when a responder can take action.

The target workflow is:

1. Observability Cloud detects a sustained checkout symptom.
2. The detector sends a notification to Splunk On-Call.
3. Splunk On-Call routes the incident to the checkout team by routing key.
4. The responder acknowledges the incident, opens the Observability Cloud links, and investigates service, trace, and infrastructure context.
5. The responder resolves or reroutes the incident and records what happened.

## Good Paging Signals

Use this checklist before creating a detector:

| Candidate signal | Page? | Reason |
| --- | --- | --- |
| `checkout` p95 latency above SLO for 5 minutes | Yes | Sustained user-impacting degradation. |
| `checkout` error rate above threshold for 5 minutes | Yes | Directly tied to failed transactions. |
| One pod restart | Usually no | Often self-healing unless correlated with errors. |
| CPU above 90 percent for one minute | Usually no | Useful symptom, but often noisy without service impact. |
| Synthetic checkout journey failure from multiple locations | Yes | Indicates customer-facing path failure. |

{{% notice title="Design principle" style="primary" icon="lightbulb" %}}
Use Observability Cloud for high-resolution detection and investigation. Use Splunk On-Call when the condition requires human coordination, ownership, and escalation.
{{% /notice %}}

## Success Criteria

At the end of this workshop, you should have:

* One Splunk On-Call routing key for the application or service team.
* One detector in Observability Cloud with a clear severity and alert message.
* One test incident in Splunk On-Call with payload context from Observability Cloud.
* A short responder runbook that explains the first three investigation steps.

## Discussion Prompts

Use these prompts with attendees before the hands-on sections:

* Which service-level symptoms should wake someone up?
* Which symptoms should create a ticket or dashboard event instead?
* What dimensions should be included in the alert payload?
* Which team owns the first response?
* When should the incident be rerouted or escalated?

