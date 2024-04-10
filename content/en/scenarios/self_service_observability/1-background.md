---
title: Background
linkTitle: 1 Background
weight: 1
time: 3 minutes
---

## Background

Let's review a few background concepts on **Open Telemetry** before jumping into the details.

First we have the **Open Telemetry Collector**, which lives on hosts or kubernetes nodes. These collectors can collect local information (like cpu, disk, memory, etc.). They can also collect metrics from other sources like prometheus (push or pull) or databases and other middleware.

![OTel Diagram](../images/otel-diagram.svg?width=60vw)
Source: [OTel Documentation](https://opentelemetry.io/docs/)

The way the **OTel Collector** collects and sends data is using **pipelines**. Pipelines are made up of:
* **Receivers**: Collect telemetry from one or more sources; they are pull- or push-based.
* **Processors**: Take data from receivers and modify or transform them. Unlike receivers and exporters, processors process data in a specific order.
* **Exporters**: Send data to one or more observability backends or other destinations.

![OTel Diagram](../images/otel-collector-details.svg?width=60vw)
Source: [OTel Documentation](https://opentelemetry.io/docs/collector/)

The final piece is applications which are instrumented; they will send traces (spans), metrics, and logs.

By default the instrumentation is designed to send data to the local collector (on the host or kubernetes node). This is desirable because we can then add metadata on it -- like which pod or which node/host the application is running on.