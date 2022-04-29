---
title: Initial State
weight: 2
---

In this workshop we will be role playing as an **SRE team** responsible for an application consisting of a handful of microservices.

We have started with our application with no observability capability.

Our developers have added some log messages into the application as a way to get some visibility into the application. We have also deployed the [Open Telemetry Collector](https://opentelemetry.io/docs/collector/), which is a vendor-agnostic collector that can receive, process, and send telemetry data. We have done minimal configuration on it, so it includes sending out-of-the-box metrics (CPU, memory, disk, etc.) and has also been configured to pass application logs as well.

Here are a few views we get from this implementation:

(**INSERT**: Picture of infrastructure IM)

(**INSERT**: Picture of Log Observer Logs)

[Go to Event 1](../event1)