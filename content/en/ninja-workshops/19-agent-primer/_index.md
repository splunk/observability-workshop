---
title: Splunk Observability Agent Primer
linkTitle: Splunk Observability Agent Primer
weight: 19
archetype: chapter
time: 2 minutes
authors: ["Bill Grant", "Others TBD"]
description: This workshop will provide a backdrop for understanding the different agents used within Splunk. Then it will go on a deeper dive on Open Telemetry. The workshop may be a good primer to use before going into other ninja workshops tackling a specific challenge. 
draft: false
hidden: true
---

**Splunk** has a number of agents that represent the different ways to collect data for **Observability**.

In some sense an observability backend can be impartial; as long as the data is provided in a format that is expected, the backend technically doesn't care what agent sent the data.

Knowing which agent to use is an important decision, and one that is often made at the beginning of an Observability implementation.

Splunk has been the largest contributor to OpenTelemetry, which sets out to democratize the collection of data. When more vendors and customers standardize on this plane, the users of Observability win, by benefitting from the collective development of software. It also means users can switch between vendors with less disruption to their business.

**OpenTelemetry** is certainly the most common technology **Splunk** recommends for observability use cases. But is it the only one? And which **OpenTelemetry** agent (or agents)? This primer will help to make sense of that.

It's accurate up until April of 2026, but this is a landscape that changes, and with that it will be important to ensure you have the latest recommendations from **Splunk**.

This workshop will provide a lens into these different agents and when to use them.

The first few pages will offer a primer on signals and OpenTelemetry. You can skim past these sessions if you are already familiar with these concepts.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
The easiest way to navigate through this workshop is by using:

* the left/right arrows (**<** | **>**) on the top right of this page
* the left (◀️) and right (▶️) cursor keys on your keyboard
  {{% /notice %}}
