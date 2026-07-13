---
title: What is an Agent
linkTitle: 2. What is an Agent
weight: 2
time: 5 minutes
---

## Agent Language

Before we go into the different types of agents it's important that we establish some language we use, so as to not cause confusion.

## OpenTelemetry

In OpenTelemetry, there are different components that are used to collect data from a system.

### Collector

OpenTelemetry defines the collector as:
> The OpenTelemetry Collector offers a vendor-agnostic implementation of how to receive, process and export telemetry data. It removes the need to run, operate, and maintain multiple agents/collectors. This works with improved scalability and supports open source observability data formats (e.g. Jaeger, Prometheus, Fluent Bit, etc.) sending to one or more open source or commercial backends.
- Source: [Open Telemetry Docs](https://opentelemetry.io/docs/collector/)

**Is a collector an agent itself?** In a sense, yes. It contains **receivers** which are used to collect data, has **processors** to -- you guessed it -- process it, and then **exporters** to send that data to one or more detinations (like gateways for routing, or observability backends).

#### Receivers

**Receivers** can work by pushing or pulling data, despite their name. For example they can collect the host's CPU, memory, and disk information by scraping that information. Or they can leave an endpoint that other systems can push information into.

#### Processors

**Processors** process the data. For example processors can:
* [redact](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor)
* [filter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor)
* [sample (tail)](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor)
* [sample (probabilistic)](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/probabilisticsamplerprocessor)
* [transform](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/metricstransformprocessor)

There are a few core processors that are common to use like the [memory limit processor](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/memorylimiterprocessor) (which can help mitigate out-of-memory situations) and the [batch processor](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/batchprocessor) (which puts telemetry into batches by compressing and sending data in fewer connections).

#### Exporters

Now we need to send the data somewhere, and the **exporters** do that. Logs to Splunk Platform typically use a [hec exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/splunkhecexporter). Other telemetry use different exporters to get to their destination.

#### Pipelines

These receivers, processors, and exports are all brought together in [pipelines](https://opentelemetry.io/docs/collector/configuration/#basics).

### Instrumentation Agents

So the collector provides a great backbone for collection, but how do we then collect data from the application side? That's where instrumentation agents come in.

