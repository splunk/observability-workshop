---
title: Connect Observability Cloud
linkTitle: 3. Connect O11y
weight: 3
time: 10 minutes
description: Create the Splunk On-Call notification integration in Splunk Observability Cloud.
---

## Goal

In this section, you will create the notification integration in Splunk Observability Cloud that lets detectors send alert notifications to Splunk On-Call.

## How the Connection Works

There are three separate configuration pieces:

| Piece | Where it is configured | Purpose |
| --- | --- | --- |
| Service API Endpoint | Splunk On-Call | Receives alert notifications from Observability Cloud. |
| Notification integration | Splunk Observability Cloud | Stores the endpoint URL and validates that Observability Cloud can reach Splunk On-Call. |
| Routing key | Detector recipient in Observability Cloud | Tells Splunk On-Call which escalation policy should receive the incident. |

The integration is intentionally split this way. You create the endpoint integration once, then reuse it across multiple detectors with different routing keys.

For example:

| Detector | Integration | Routing key |
| --- | --- | --- |
| Checkout latency critical | `Checkout On-Call` | `checkout-INITIALS` |
| Payments error rate critical | `Checkout On-Call` or shared org integration | `payments` |
| Platform Kubernetes node pressure | Shared On-Call integration | `platform` |

## What the Integration Provides

When a detector alert condition is met, Observability Cloud sends an alert notification to Splunk On-Call. Splunk On-Call then creates or updates an incident and routes it through the escalation policy attached to the routing key.

The responder gets:

* The detector name and rule name.
* The alert severity.
* The triggering condition.
* The signal value and dimensions included in the detector message.
* Any runbook, dashboard, or service links included in the message.
* A Splunk On-Call incident timeline for acknowledgement, reroute, escalation, notes, and resolution.

The integration does not move traces, metrics, dashboards, or logs into Splunk On-Call. Those stay in Observability Cloud. The incident should link responders back to Observability Cloud for investigation.

## 1. Open the Splunk On-Call Integration

1. Log in to Splunk Observability Cloud.
2. Open **Data Management**.
3. Go to **Available integrations**, or select **Add Integration** from **Deployed integrations**.
4. In the integration filter, select **All**.
5. Search for **Splunk On-Call**.
6. Open the Splunk On-Call notification integration.

If your user interface shows integration categories, look under notification services or all integrations.

## 2. Create the Integration

1. Select **New Integration** or **Add Integration**.
2. The default integration name might appear as `VictorOps`. Rename it to `Checkout On-Call`.
3. In **Post URL**, paste the full Splunk On-Call **Service API Endpoint** that you copied earlier.
4. Confirm that the URL still contains `$routing_key`.
5. Save the integration.
6. Confirm that Observability Cloud displays a validation success message.

{{% notice title="Naming convention" style="info" %}}
Use names that make routing intent obvious, such as `Checkout On-Call`, `Payments On-Call`, or `Platform Critical On-Call`. Clear names reduce mistakes when detector owners add recipients.
{{% /notice %}}

{{% notice title="Common mistake" style="warning" %}}
Do not replace `$routing_key` in the Post URL with `checkout-INITIALS`. If you replace the placeholder in the integration URL, the integration becomes tied to one route and detector-level routing will not work as intended.
{{% /notice %}}

## 3. Validate the Connection

Use this checklist before adding the integration to detectors:

| Item | Expected value |
| --- | --- |
| Integration name | `Checkout On-Call` |
| Post URL | The endpoint from the Splunk Observability Cloud System Monitoring tile |
| Placeholder | URL contains `$routing_key` |
| Validation | Observability Cloud shows the integration as validated |
| Routing key for the detector recipient | `checkout-INITIALS` |
| Owning team in Splunk On-Call | Checkout Workshop or the selected service team |
| Escalation policy in Splunk On-Call | Checkout Primary |

If validation fails:

* Confirm you copied the full endpoint URL from Splunk On-Call.
* Confirm the Splunk Observability Cloud System Monitoring integration is enabled in Splunk On-Call.
* Confirm the endpoint URL still includes `$routing_key`.
* Confirm you have not pasted a generic REST endpoint from a different Splunk On-Call integration tile.

## 4. Decide Severity Mapping

Use a simple severity map for this workshop:

| Detector severity | Splunk On-Call behavior |
| --- | --- |
| Critical | Page the primary responder immediately. |
| Major | Page during business hours or route to the primary policy if customer impact is confirmed. |
| Minor or Warning | Notify by email, chat, ticket, or dashboard event unless the team has a clear response action. |
| Info | Do not page. Use for context and event timelines. |

Splunk Observability Cloud detectors can send notifications when an alert condition is met and when it clears. In the incident exercise, you will verify both the trigger and recovery path.

## 5. Full Setup Example

Use these example values throughout the rest of the workshop:

| Field | Example value |
| --- | --- |
| Splunk On-Call team | `Checkout Workshop` |
| Escalation policy | `Checkout Primary` |
| Routing key | `checkout-abc` |
| Observability Cloud integration name | `Checkout On-Call` |
| Detector name | `Checkout Workshop - Sustained Degradation` |
| Alert severity | `Critical` |

The flow for these values is:

```text
Detector: Checkout Workshop - Sustained Degradation
  Alert recipient: VictorOps / Checkout On-Call
  Routing key: checkout-abc
        |
        v
Splunk On-Call routing key: checkout-abc
        |
        v
Escalation policy: Checkout Primary
        |
        v
Checkout Workshop on-call responder
```

{{% notice title="UI label note" style="info" %}}
Some Observability Cloud detector recipient menus still use the label **VictorOps** for Splunk On-Call. Select **VictorOps**, then choose the Splunk On-Call integration name you created.
{{% /notice %}}

## Reference

* [Send alert notifications to Splunk On-Call using Splunk Observability Cloud](https://help.splunk.com/splunk-observability-cloud/manage-data/available-data-sources/supported-integrations-in-splunk-observability-cloud/notification-services/send-alerts-to-splunk-on-call)
* [Send alert notifications to services using Splunk Observability Cloud](https://help.splunk.com/en?resourceId=admin_notif-services_admin-notifs-index)
