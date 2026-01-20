---
title: Workshop Overview
linkTitle: 1. Workshop Overview
weight: 1
archetype: chapter
time: 2 minutes
description: Workshop Overview
---

**Introduction**  
The goal of this workshop is to give you hands-on experience troubleshooting an issue using Splunk Observability Cloud to identify its root cause. We’ve provided a fully instrumented microservices-based application running on Kubernetes, which sends metrics, traces, and logs to Splunk Observability Cloud for real-time analysis.

**Who Should Attend?**  
This workshop is ideal for anyone looking to gain practical knowledge of Splunk Observability. It's designed for individuals with little or no prior experience with the platform.

**What You’ll Need**  
All you need is your laptop and a browser with access to external websites. The workshop can be attended either in-person or via Zoom. If you don’t have the Zoom client installed, you can still join using your browser.

**Workshop Overview**  
In this 3-hour session, we’ll cover the fundamentals of Splunk Observability—the only platform offering streaming analytics and NoSample Full Fidelity distributed tracing—in an interactive, hands-on setting. Here's what you can expect:

- **OpenTelemetry**  
  Learn why OpenTelemetry is essential for modern observability and how it enhances visibility into your systems.

- **Tour of the Splunk Observability User Interface**  
  Take a guided tour of Splunk Observability Cloud’s interface, where we’ll show you how to navigate the five key components: APM, RUM, Log Observer, Synthetics, and Infrastructure.

- **Generate Real User Data**  
  Dive into a simulated retail experience on the Online Boutique Website. Using your browser, mobile, or tablet, explore the site and generate real user data that includes metrics (Is there a problem?), traces (Where is the problem?), and logs (What’s causing the problem?).

- **Splunk Real User Monitoring (RUM)**  
  Analyze the real user data collected from participants’ browser sessions. Your task is to identify poorly performing sessions and begin the troubleshooting process.

- **Splunk Application Performance Monitoring (APM)**  
  Gain end-to-end visibility by linking a RUM trace (front-end) to an APM trace (back-end). You’ll explore how telemetry from various services is captured and visualized in Splunk Observability Cloud, helping you detect anomalies and errors.

- **Splunk Log Observer (LO)**  
  Learn how to leverage the "Related Content" feature to easily navigate between components. In this case, we’ll move from an APM trace to the related logs for deeper insight into issues.

- **Splunk Synthetics**  
  Discover how Synthetics can help with 24/7 monitoring of your application. We’ll walk you through setting up a simple synthetic test that runs every minute to monitor the performance and availability of the Online Boutique website.

By the end of this session, you'll have gained practical experience with Splunk Observability Cloud and a solid understanding of how to troubleshoot and resolve issues across your application stack.

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
