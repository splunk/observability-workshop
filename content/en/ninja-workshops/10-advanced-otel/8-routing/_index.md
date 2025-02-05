---
title: 8. Routing
linkTitle: 8. Routing
time: 10 minutes
weight: 8
---

The [**Routing Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) in OpenTelemetry is a powerful feature that allows you to direct data (`traces`, `metrics`, or `logs`) to different pipelines based on specific criteria. This is especially useful in scenarios where you want to apply different processing or exporting logic to subsets of your telemetry data.

For example, you might want to send *production* data to one exporter while directing *test* or *development* data to another. Similarly, you could route certain spans based on their attributes, such as service name, environment, or span name, to apply custom processing or storage logic.

### Setup

Create a new subdirectory named `8-routing` and copy all contents from the `7-transform-data` directory into it. Then, delete any `*.out` and `*.log` files. Your updated directory structure should now look like this:

{{% tab title="Updated Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
├── 5-dropping-spans
├── 6-sensitive-data
├── 7-transform-data
├── 8-routing
│   ├── agent.yaml
│   ├── health.json
│   ├── gateway.yaml
│   ├── log-gen.sh (or .ps1)
│   └── trace.json
└── otelcol
```

{{% /tab %}}

Next, we will configure the routing connector and the respective pipelines.
