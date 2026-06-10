---
title: Create an Actionable Detector
linkTitle: 5. Create Detector
weight: 5
time: 15 minutes
description: Create a detector in Observability Cloud and route its alert recipient to Splunk On-Call.
---

## Goal

In this section, you will create a detector in Splunk Observability Cloud using the checkout demo app metric and add the Splunk On-Call integration as an alert recipient.

## 1. Choose the Signal

Use the custom metric emitted by the checkout demo app:

| Signal | Value |
| --- | --- |
| Metric | `workshop.checkout.errors` |
| Filter | `deployment.environment:on-call-workshop` |
| Split by | `app.issue_mode`, `http.response.status_code`, or `status` |
| Trigger | Error count is greater than `0` for a fast workshop, or greater than `5` for 5 minutes for a quieter detector. |

Alternative signal:

| Signal | Value |
| --- | --- |
| Metric | `workshop.checkout.latency_ms` |
| Filter | `deployment.environment:on-call-workshop` |
| Analytics | p95 latency |
| Trigger | p95 is greater than `1500` ms for several minutes. |

{{% notice title="Workshop shortcut" style="primary" icon="lightbulb" %}}
For a fast lab, use `workshop.checkout.errors` and set the threshold to greater than `0`. For a more realistic lab, require several errors over a 5-minute window.
{{% /notice %}}

## 2. Create the Detector

1. In Splunk Observability Cloud, create a new chart.
2. Search for the metric `workshop.checkout.errors`.
3. Add the filter `deployment.environment:on-call-workshop`.
4. Add a **Sum** aggregation. For the workshop, group by `app.issue_mode` and `http.response.status_code`.
5. Save the chart or create a detector directly from the chart.
6. Name the detector `Checkout Workshop - Sustained Degradation`.
7. Configure a static threshold.
8. Use threshold `> 0` for a fast demo, or `> 5` for 5 minutes for a quieter lab.
9. Run the detector preview or pre-flight check to estimate alert volume.

## 3. Add the Alert Message

Use an alert message that tells the responder what is broken, why they were paged, and where to start.

```text
Checkout service degradation detected.

Impact:
- Checkout may be slow or failing for customers.

Trigger:
- Detector: {{{detectorName}}}
- Rule: {{{ruleName}}}
- Condition: {{{readableRule}}}
- Signal value: {{inputs.A.value}}
- Dimensions: {{{dimensions}}}

First response:
1. Open the detector and review the triggering dimension.
2. Open APM > Service map and select checkout-service.
3. Check Trace Analyzer for slow or erroring checkout traces.
4. Check inventory-service for latency or 503 responses.

Runbook:
https://example.com/runbooks/checkout
```

Replace the runbook URL with your team's real runbook, dashboard, or service catalog page.

## 4. Add Splunk On-Call as a Recipient

1. Continue to the detector **Alert Recipients** step.
2. Select **Add recipient**.
3. Choose **VictorOps**. This is the detector recipient label used for Splunk On-Call.
4. Select the `Checkout On-Call` integration.
5. Enter the routing key you created earlier: `checkout-INITIALS`.
6. Save and activate the detector.

The recipient configuration should now look like this:

| Field | Value |
| --- | --- |
| Recipient type | `VictorOps` |
| Integration | `Checkout On-Call` |
| Routing key | `checkout-INITIALS` |
| Severity | `Critical` for this workshop example |

## 5. Validate the Detector Setup

Before triggering the alert, verify the complete chain:

| Check | How to verify |
| --- | --- |
| Detector is active | Open **Alerts & Detectors** and confirm the detector is enabled. |
| Recipient is configured | Edit the detector and confirm the alert recipient is `VictorOps / Checkout On-Call`. |
| Routing key is exact | Confirm the routing key matches the Splunk On-Call key exactly. |
| Escalation policy is attached | In Splunk On-Call, open **Settings > Routing Keys** and confirm the key maps to `Checkout Primary`. |
| Responder can receive pages | Confirm the escalation policy has a user or rotation with a notification policy. |
| Message is actionable | Confirm the alert message includes impact, trigger, first response, and runbook context. |

## 6. Optional Terraform Path

This repository includes a Terraform example in `workshop/on-call` that creates a CPU detector and sends notifications to Splunk On-Call.

Use it when you want to demonstrate Observability-as-code:

```bash
cd workshop/on-call
terraform init
terraform plan
terraform apply
```

Do not commit real access tokens or routing keys. See `workshop/on-call/README.md` for the expected variables.

The Terraform notification string follows this pattern:

```text
VictorOps,<observability-cloud-integration-id>,<splunk-on-call-routing-key>
```

Use the UI path first if this is your first time setting up the integration. Use Terraform after you have confirmed the integration ID and routing key.

## Checkpoint

Before continuing, confirm that:

* The detector is active.
* The detector has the Splunk On-Call integration as a recipient.
* The recipient uses the routing key assigned to your workshop team.
* The alert message includes first-response context.

## Reference

* [Introduction to alerts and detectors in Splunk Observability Cloud](https://help.splunk.com/en/?resourceId=alerts-detectors-notifications_alerts-and-detectors_alerts-detectors-notifications)
* [Intro to AutoDetect alerts and detectors](https://help.splunk.com/splunk-observability-cloud/create-alerts-detectors-and-service-level-objectives/create-alerts-and-detectors/use-and-customize-autodetect-alerts-and-detectors/intro-to-autodetect-alerts-and-detectors)
