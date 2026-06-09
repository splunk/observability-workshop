---
title: Observability Cloud and On-Call
linkTitle: O11y and On-Call
weight: 16
archetype: chapter
authors: ["Splunk"]
description: Connect Splunk Observability Cloud detectors to Splunk On-Call, route alerts to the right team, and run a complete incident response workflow.
time: 60 minutes
draft: false
hidden: false
aliases:
  - /ninja-workshops/16-o11y-on-call-incident-response/
product: "Observability Cloud"
---

## Workshop Overview

This workshop shows how to turn a performance signal in **Splunk Observability Cloud** into an actionable incident in **Splunk On-Call**. The lab follows a checkout-service incident from detection, paging, acknowledgement, troubleshooting, and recovery.

By the end of the workshop, you will be able to:

* Explain when to use Observability Cloud detectors and Splunk On-Call routing together.
* Configure a Splunk On-Call team, escalation policy, and routing key for an application team.
* Create a Splunk On-Call notification integration in Observability Cloud.
* Add the On-Call integration as a detector recipient.
* Run an incident workflow: acknowledge, inspect payload details, add context, reroute or escalate, and resolve.
* Define operational guardrails that reduce noisy alerts and improve MTTR.

## Scenario

You are supporting the `checkout` service for an ecommerce application. The service already sends telemetry to Splunk Observability Cloud through OpenTelemetry. During traffic spikes, checkout latency increases and the service begins returning errors. The SRE team needs a workflow that does more than show red charts: the right responder must be paged with enough context to investigate immediately.

In this workshop, Observability Cloud is the detection and investigation system. Splunk On-Call is the response coordination system.

## Architecture

```text
Application and infrastructure telemetry
        |
        v
Splunk Observability Cloud
  - APM service view
  - Infrastructure navigators
  - dashboards
  - detectors
        |
        v
Splunk On-Call notification integration
        |
        v
Routing key: checkout
        |
        v
Checkout team escalation policy
        |
        v
On-call responder
```

## What the Integration Provides

The Splunk On-Call notification integration connects **detector alert notifications** from Splunk Observability Cloud to the **incident workflow** in Splunk On-Call.

| Integration capability | What it does |
| --- | --- |
| Trigger notification | Sends a detector alert to Splunk On-Call when an alert condition is met. |
| Clear notification | Sends recovery context when the detector alert condition clears. |
| Routing key handoff | Uses the routing key entered on the detector recipient to select the correct Splunk On-Call escalation policy. |
| Responder context | Carries detector name, rule name, severity, triggering condition, signal value, dimensions, and message text into the incident details. |
| Incident coordination | Lets responders acknowledge, reroute, escalate, add notes, and resolve the incident in Splunk On-Call. |

The integration does not stream all telemetry into Splunk On-Call. Metrics, traces, dashboards, and service maps stay in Observability Cloud. Splunk On-Call receives the alert notification and coordinates the human response.

{{% notice title="Important setup detail" style="info" %}}
When you copy the Splunk On-Call Service API Endpoint, keep the literal `$routing_key` placeholder in the URL. Do not replace it while creating the Observability Cloud integration. You enter the real routing key later when you add the Splunk On-Call integration as a detector recipient.
{{% /notice %}}

## Prerequisites

You need the following access before starting:

* A Splunk Observability Cloud organization.
* Permission to create or edit notification integrations in Observability Cloud.
* Permission to create or edit detectors in Observability Cloud.
* A Splunk On-Call account.
* Splunk On-Call global admin or alert admin access for the integration endpoint and routing key setup.
* A service, host, Kubernetes workload, synthetic test, or sample metric that can be used to create a detector.

{{% notice title="Instructor note" style="info" %}}
If attendees do not have a live application, use Observability Cloud sample data or an existing host metric. The core learning objective is the alert-to-incident workflow, not the specific metric used to trigger the detector.
{{% /notice %}}

## Lab Flow

1. Review the use case and decide what should page a human.
2. Prepare a Splunk On-Call team, escalation policy, and routing key.
3. Connect Splunk Observability Cloud to Splunk On-Call.
4. Create an actionable detector and add the On-Call recipient.
5. Trigger or simulate an incident and run the response workflow.
6. Operationalize the pattern for production teams.

## Official References

* [Introduction to alerts and detectors in Splunk Observability Cloud](https://help.splunk.com/en/?resourceId=alerts-detectors-notifications_alerts-and-detectors_alerts-detectors-notifications)
* [Send alert notifications to Splunk On-Call using Splunk Observability Cloud](https://help.splunk.com/splunk-observability-cloud/manage-data/available-data-sources/supported-integrations-in-splunk-observability-cloud/notification-services/send-alerts-to-splunk-on-call)
* [Set up an escalation policy in Splunk On-Call](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/splunk-on-call/introduction-to-splunk-on-call/getting-started-guide-for-splunk-on-call-admins/team-escalation-policy)
* [Getting started guide for Splunk On-Call users](https://help.splunk.com/en/splunk-cloud-platform/alert-and-respond/splunk-on-call/user-management/getting-started-guide-for-splunk-on-call-users)
