---
title: What is OpenTelemetry & why should you care?
linkTitle: 2. OpenTelemetry
weight: 2
archetype: chapter
time: 2 minutes
description: Learn about OpenTelemetry and why you should care about it.
hidden: true
---

## OpenTelemetry

With the rise of cloud computing, microservices architectures, and ever-more complex business requirements, the need for Observability has never been greater. Observability is the ability to understand the internal state of a system by examining its outputs. In the context of software, this means being able to understand the internal state of a system by examining its telemetry data, which includes **metrics**, **traces**, and **logs**.

To make a system observable, it must be instrumented. That is, the code must emit traces, metrics, and logs. The instrumented data must then be sent to an Observability back-end such as **Splunk Observability Cloud**.

| Metrics | Traces | Logs |
|:-------:|:------:|:----:|
| _**Do I have a problem?**_ | _**Where is the problem?**_ | _**What is the problem?**_ |

OpenTelemetry does two important things:

* Allows you to **own** the data that you generate rather than be stuck with a proprietary data format or tool.
* Allows you to learn **a single set** of APIs and conventions

These two things combined enable teams and organizations the flexibility they need in today’s modern computing world.

There are a lot of variables to consider when getting started with Observability, including the all-important question: _"How do I get my data into an Observability tool?"_. The industry-wide adoption of OpenTelemetry makes this question easier to answer than ever.

## Why Should You Care?

OpenTelemetry is completely open-source and free to use. In the past, monitoring and Observability tools relied heavily on proprietary agents meaning that the effort required to change or set up additional tooling required a large amount of changes across systems, from the infrastructure level to the application level.

Since OpenTelemetry is vendor-neutral and supported by many industry leaders in the Observability space, adopters can switch between supported Observability tools at any time with minor changes to their instrumentation. This is true regardless of which distribution of OpenTelemetry is used – like with Linux, the various distributions bundle settings and add-ons but are all fundamentally based on the community-driven OpenTelemetry project.

Splunk has fully committed to OpenTelemetry so that our customers can collect and use **ALL** their data, in any type, any structure, from any source, on any scale, and all in real-time. OpenTelemetry is fundamentally changing the monitoring landscape, enabling IT and DevOps teams to bring data to every question and every action. You will experience this during these workshops.

![OpenTelemetry Logo](images/otel.png)
