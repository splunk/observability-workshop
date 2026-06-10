---
title: Incident Response with Splunk Observability Cloud and Splunk On-Call
linkTitle: O11y and On-Call Incident Response
weight: 7
archetype: chapter
authors: ["Splunk"]
description: Use Observability Cloud detectors and Splunk On-Call routing to reduce alert noise, page the right responder, and shorten incident response time.
time: 30 minutes
---

## Use Case

Application teams often have strong telemetry but weak response workflows. Dashboards show service health, traces reveal root cause, and infrastructure metrics show resource pressure, but the right responder still needs to be notified, own the incident, and coordinate action.

This use case connects **Splunk Observability Cloud** and **Splunk On-Call** for a customer-facing checkout service:

1. Observability Cloud monitors service latency, errors, synthetic journey health, and infrastructure symptoms.
2. A detector identifies sustained customer impact.
3. The detector sends an alert notification to Splunk On-Call.
4. Splunk On-Call uses a routing key to page the checkout team escalation policy.
5. The responder acknowledges the incident, uses Observability Cloud to investigate, and resolves or reroutes the incident.

## Business Problem

Without a connected detection and response workflow, teams see these patterns:

* Alerts go to shared inboxes or chat channels with no clear owner.
* Infrastructure alerts page responders even when there is no service impact.
* Service-impacting incidents are delayed because the owning team is unclear.
* Responders lose time finding the right dashboard, trace, runbook, or escalation path.
* Post-incident reviews lack a complete timeline from detection through response.

## Target Outcome

The target operating outcome is a closed-loop incident workflow:

| Capability | Outcome |
| --- | --- |
| Observability Cloud detectors | Detect sustained symptoms in real time. |
| Detector alert message | Give responders impact, trigger, dimensions, and runbook context. |
| Splunk On-Call routing keys | Route incidents to the team that owns the service. |
| Escalation policies | Page the current responder and escalate when needed. |
| Incident timeline | Preserve acknowledgement, reroute, notes, and recovery events. |

## Integration Setup Flow

To connect Splunk Observability Cloud and Splunk On-Call for this use case, configure the workflow in this order:

1. In Splunk On-Call, create or select the owning team.
2. Create an escalation policy for that team.
3. Create a routing key and assign it to the escalation policy.
4. Enable the **Splunk Observability Cloud System Monitoring** integration tile in Splunk On-Call.
5. Copy the full Service API Endpoint, including the `$routing_key` placeholder.
6. In Splunk Observability Cloud, create a Splunk On-Call notification integration.
7. Paste the Service API Endpoint into the Observability Cloud integration **Post URL** field without replacing `$routing_key`.
8. Save and validate the integration.
9. Create or edit a detector.
10. In the detector recipient step, add **VictorOps**, select the Splunk On-Call integration, and enter the routing key.
11. Trigger or simulate the detector and confirm the incident routes to the expected Splunk On-Call team.

## What the Integration Provides

The integration provides the handoff between detection and response:

| Provides | Details |
| --- | --- |
| Alert-to-incident creation | Detector trigger notifications create or update incidents in Splunk On-Call. |
| Alert clear context | Detector clear notifications send recovery context into the response workflow. |
| Team routing | Routing keys map detector recipients to Splunk On-Call escalation policies. |
| Responder context | Detector messages can include impact, dimensions, current value, runbook links, and investigation steps. |
| Incident lifecycle | Splunk On-Call tracks acknowledgement, escalation, reroute, notes, and resolution. |

The integration does not replace Observability Cloud investigation. Responders still use Observability Cloud service maps, charts, traces, navigators, and dashboards to diagnose the incident.

## Reference Architecture

```text
OpenTelemetry, cloud integrations, synthetics, and APM
        |
        v
Splunk Observability Cloud
        |
        | detector trigger and clear notifications
        v
Splunk On-Call integration
        |
        | routing key: checkout
        v
Checkout team escalation policy
        |
        v
Primary responder, backup responder, manager
```

## Example Detection Strategy

Use service-impacting symptoms for pages:

| Detector | Page? | Notes |
| --- | --- | --- |
| Checkout p95 latency above SLO for 5 minutes | Yes | Directly represents user impact. |
| Checkout error rate above 5 percent for 5 minutes | Yes | Directly represents failed transactions. |
| Checkout synthetic flow fails from multiple locations | Yes | Confirms external user impact. |
| CPU above 90 percent on one host | Not by itself | Use as investigation context or combine with service impact. |
| Single pod restart | Not by itself | Track on dashboards or lower-severity notifications. |

## Workshop Mapping

Use the hands-on workshop at [Observability Cloud and On-Call](../../ninja-workshops/operations/16-o11y-on-call-incident-response/) to implement this use case.

The workshop covers:

* Splunk On-Call team, escalation policy, and routing key setup.
* Observability Cloud Splunk On-Call notification integration.
* A checkout demo app that emits APM traces and custom metrics through OpenTelemetry.
* Detector creation and alert-recipient configuration.
* Incident acknowledgement, investigation, reroute, and resolution.
* Production guardrails for severity, routing, message design, and noisy-alert reduction.

The demo app is located at:

```text
workshop/on-call/checkout-demo
```

It emits the services `checkout-service`, `inventory-service`, and `checkout-loadgen`, plus the metrics `workshop.checkout.requests`, `workshop.checkout.errors`, and `workshop.checkout.latency_ms`.

## Implementation Checklist

Before moving from workshop to production, confirm:

* Every paging detector has an owning team.
* Every routing key maps to an escalation policy.
* Every critical alert message includes a runbook or dashboard link.
* Every detector has been previewed against historical data.
* Every incident has a clear trigger and recovery path.
* Teams review alert noise and reroutes regularly.

## Example Configuration

Use this concrete example to test the workflow in a workshop organization:

| Setting | Example |
| --- | --- |
| Team | `Checkout Workshop` |
| Escalation policy | `Checkout Primary` |
| Routing key | `checkout-abc` |
| Observability Cloud integration | `Checkout On-Call` |
| Detector | `Checkout Workshop - Sustained Degradation` |
| Recipient type in detector | `VictorOps` |
| Recipient routing key | `checkout-abc` |

Expected result:

```text
Detector triggers in Observability Cloud
        |
        v
Observability Cloud sends notification to the Splunk On-Call endpoint
        |
        v
Splunk On-Call reads routing key checkout-abc
        |
        v
Checkout Primary escalation policy pages the current responder
```

## Official References

* [Introduction to alerts and detectors in Splunk Observability Cloud](https://help.splunk.com/en/?resourceId=alerts-detectors-notifications_alerts-and-detectors_alerts-detectors-notifications)
* [Send alert notifications to Splunk On-Call using Splunk Observability Cloud](https://help.splunk.com/splunk-observability-cloud/manage-data/available-data-sources/supported-integrations-in-splunk-observability-cloud/notification-services/send-alerts-to-splunk-on-call)
* [Set up an escalation policy in Splunk On-Call](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/splunk-on-call/introduction-to-splunk-on-call/getting-started-guide-for-splunk-on-call-admins/team-escalation-policy)
* [Getting started guide for Splunk On-Call users](https://help.splunk.com/en/splunk-cloud-platform/alert-and-respond/splunk-on-call/user-management/getting-started-guide-for-splunk-on-call-users)
