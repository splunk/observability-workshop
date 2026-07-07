---
title: Types of Telemetry
linkTitle: 1. Types of Telemetry
weight: 1
time: 5 minutes
---

## Supported telemetry

OTel officially supports 4 types of telemetry, or signals.

We'll use the definitions provided by the [OTel docs](https://opentelemetry.io/docs/concepts/signals/):

### Metrics

> A metric is a measurement of a service captured at runtime. The moment of capturing a measurement is known as a metric event, which consists not only of the measurement itself, but also the time at which it was captured and associated metadata.

> Application and request metrics are important indicators of availability and performance. Custom metrics can provide insights into how availability indicators impact user experience or the business. Collected data can be used to alert of an outage or trigger scheduling decisions to scale up a deployment automatically upon high demand.

Good examples of metrics are:
- System
  - cpu utilization
  - memory utilization
  - disk usage
- Application Performance
  - response time
  - error count
- Business
  - total sales
  - count of customers

### Traces

> Traces give us the big picture of what happens when a request is made to an application. Whether your application is a monolith with a single database or a sophisticated mesh of services, traces are essential to understanding the full “path” a request takes in your application.

Traces are made up of spans. They are typically shown as a waterfall to easily see where time is spent in a given service or method.

### Logs

> A log is a timestamped text record, either structured (recommended) or unstructured, with optional metadata. Of all telemetry signals, logs have the biggest legacy. Most programming languages have built-in logging capabilities or well-known, widely used logging libraries.

There are a lot of benefits of having structured logs, and in a lot of ways a span acts as a very structured log. Application and host logs will contain metadata that allows it to easily be related to the other signals.

On the flip side logs are able to be unstructured. Splunk is well-recognized as a solution that can collect any kind of data.

### Baggage

> In OpenTelemetry, Baggage is contextual information that resides next to context. Baggage is a key-value store, which means it lets you propagate any data you like alongside context.

> Baggage means you can pass data across services and processes, making it available to add to traces, metrics, or logs in those services.

A lot of times we don't think about baggage because the instrumentation handles this for us. However it's important to understand this telemetry type, as there are times when we need to deal with it directly to address a challenge that the out of the box capabilities are not able to address.

## Other Telemetry

Other signals are still at the proposal stage for OpenTelemetry. But both of these are being used by Splunk Observability today and supported.

### Events

> Events are OpenTelemetry’s standardized format for LogRecords. All semantic conventions defined for logs SHOULD be formatted as Events. Requirements and details for the Event format can be found in the semantic conventions.

> Events are intended to be used by OpenTelemetry instrumentation. It is not a requirement that all LogRecords are formatted as Events.

Splunk Observability Cloud can receive events via APIs, and these can be particularly useful in displaying data on charts.

### Profiles

> A profile is a collection of samples and associated metadata that shows where applications consume resources during execution. A sample records values encountered in some program context (typically a stack trace), optionally augmented with auxiliary information like the trace ID corresponding to a higher-level request.

> The moment of capturing a sample is known as a sample event and consists not only of the observation data point, but also the time at which it was captured.

Profiles are used by Splunk Observability Cloud to get deeper understanding of where time is being spent in services -- in particular large services that have many more lines of code than a typical microservice.