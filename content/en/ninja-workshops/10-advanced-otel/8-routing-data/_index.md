---
title: 8. Routing Data
linkTitle: 8. Routing Data
time: 10 minutes
weight: 8
---

The [**Routing Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) in OpenTelemetry is a powerful feature that allows you to direct data (`traces`, `metrics`, or `logs`) to different pipelines based on specific criteria. This is especially useful in scenarios where you want to apply different processing or exporting logic to subsets of your telemetry data.

For example, you might want to send *production* data to one exporter while directing *test* or *development* data to another. Similarly, you could route certain spans based on their attributes, such as service name, environment, or span name, to apply custom processing or storage logic.

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `8-routing`.
- Next, copy all contents from the `7-transform-data` directory into `8-routing`.
- After copying, remove any `*.out` and `*.log` files.
- Change **all** terminal windows to the `[WORKSHOP]/8-routing` directory.

Your updated directory structure will now look like this:

{{% tabs %}}
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
│   ├───checkpoint-dir
│   ├── agent.yaml
│   ├── health.json
│   ├── gateway.yaml
│   ├── log-gen.sh (or .ps1)
│   └── trace.json
└── otelcol
```

{{% /tab %}}
{{% /tabs %}}
{{% /notice %}}

Next, we will configure the routing connector and the respective pipelines.
