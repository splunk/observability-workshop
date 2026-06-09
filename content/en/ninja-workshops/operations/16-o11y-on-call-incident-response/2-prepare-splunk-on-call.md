---
title: Prepare Splunk On-Call
linkTitle: 2. Prepare On-Call
weight: 2
time: 15 minutes
description: Create the team, escalation policy, and routing key used by Observability Cloud notifications.
---

## Goal

In this section, you will configure the response side of the workflow in Splunk On-Call. Observability Cloud will later send detector notifications to a routing key, and Splunk On-Call will use that routing key to page the correct team.

{{% notice title="Permissions" style="info" %}}
You need Splunk On-Call global admin or alert admin permissions to retrieve the integration endpoint and create routing keys. A team admin can help manage the team schedule and escalation policy, but might need a global admin or alert admin to create the routing key.
{{% /notice %}}

## 1. Create or Select a Team

1. Log in to Splunk On-Call.
2. Open **Teams**.
3. Create a team named `Checkout Workshop` or select an existing application team.
4. Add at least one workshop participant to the team.

For a real deployment, map teams to durable ownership boundaries such as `checkout`, `payments`, `search`, or `platform`. Avoid routing keys that represent individual people.

## 2. Create an Escalation Policy

1. Open the team you selected.
2. Go to **Escalation Policies**.
3. Select **Add Escalation Policy**.
4. Name the policy `Checkout Primary`.
5. Add the primary responder or primary rotation as the first step.
6. Add a second step that pages a backup responder or manager after 5 to 10 minutes.
7. Save the policy.

{{% notice title="Why this matters" style="primary" icon="lightbulb" %}}
An escalation policy is the link between an incoming incident and the person or rotation that is actually on call. The routing key chooses the policy; the policy chooses who gets paged.
{{% /notice %}}

## 3. Create a Routing Key

1. Open **Settings**.
2. Select **Routing Keys**.
3. Create a new routing key named `checkout-INITIALS`, replacing `INITIALS` with a unique workshop identifier.
4. Assign the routing key to the `Checkout Primary` escalation policy.
5. Save the routing key.

Routing keys are operational ownership labels. Use service or team names such as `checkout`, `payments`, `platform`, or `database`. Avoid names tied to an individual responder.

Record the routing key here:

```text
Routing key: checkout-________
```

## 4. Locate the Observability Cloud Integration Endpoint

1. Open **Integrations**.
2. Select **3rd Party Integrations**.
3. Search for **Splunk Observability Cloud System Monitoring**.
4. Enable the integration if it is not already enabled.
5. Copy the full **Service API Endpoint** value, including the literal `$routing_key` text at the end of the URL.

Record the endpoint here:

```text
Service API endpoint: ________________________________
```

{{% notice title="Do not replace the placeholder yet" style="info" %}}
Keep `$routing_key` in the endpoint URL when you paste the URL into Observability Cloud. Observability Cloud asks for the actual routing key later, when you add the integration as a detector recipient.
{{% /notice %}}

You will use the service API endpoint in the next section when creating the Observability Cloud notification integration. You will use the routing key when configuring the detector recipient.

## Checkpoint

Before continuing, confirm that you have:

* A team.
* An escalation policy.
* A routing key assigned to that policy.
* The Splunk On-Call service API endpoint for Observability Cloud notifications, including `$routing_key`.

## Reference

* [Set up an escalation policy in Splunk On-Call](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/splunk-on-call/introduction-to-splunk-on-call/getting-started-guide-for-splunk-on-call-admins/team-escalation-policy)
* [Schedule examples and routing keys in Splunk On-Call](https://help.splunk.com/en/splunk-cloud-platform/alert-and-respond/splunk-on-call/create-and-manage-on-call-schedules/schedule-examples)
