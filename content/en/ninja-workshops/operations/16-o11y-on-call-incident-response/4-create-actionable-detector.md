---
title: Create an Actionable Detector
linkTitle: 4. Create Detector
weight: 4
time: 15 minutes
description: Create a detector in Observability Cloud and route its alert recipient to Splunk On-Call.
---

## Goal

In this section, you will create or edit a detector in Splunk Observability Cloud and add the Splunk On-Call integration as an alert recipient.

Use an existing service metric if you have one. If you do not have application telemetry available, use a host, Kubernetes, synthetic, or sample metric that can safely trigger during the workshop.

## 1. Choose the Signal

Recommended signals for a checkout-service incident:

| Signal type | Example detector condition |
| --- | --- |
| APM latency | p95 checkout duration is above the service objective for 5 minutes. |
| APM errors | checkout error rate is above 5 percent for 5 minutes. |
| Synthetic monitoring | checkout browser test fails from two or more locations. |
| Infrastructure | checkout workload CPU remains above 90 percent and request latency is also elevated. |

{{% notice title="Workshop shortcut" style="primary" icon="lightbulb" %}}
For a fast lab, start with one metric that is already available and lower the threshold temporarily so the detector can trigger. Raise the threshold or deactivate the detector at the end of the workshop.
{{% /notice %}}

## 2. Create the Detector

1. In Splunk Observability Cloud, open the chart, service view, navigator, or dashboard that contains the signal.
2. Create a detector from the chart or open **Alerts & Detectors** and create a new detector.
3. Name the detector `Checkout Workshop - Sustained Degradation`.
4. Select the alert signal.
5. Configure a static or dynamic threshold that represents sustained impact.
6. Use a duration such as 5 minutes to avoid paging on short spikes.
7. Run the detector preview or pre-flight check to estimate alert volume.

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

First response:
1. Open the detector and review the triggering dimension.
2. Open APM > Service map and select checkout.
3. Check Trace Analyzer for slow or erroring checkout traces.
4. Check Infrastructure > Kubernetes or hosts for resource saturation.

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
