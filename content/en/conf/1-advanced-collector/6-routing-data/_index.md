---
title: 6. Routing Data
linkTitle: 6. Routing Data
time: 10 minutes
weight: 8
---

The [**Routing Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) in OpenTelemetry is a powerful feature that allows you to direct data (`traces`, `metrics`, or `logs`) to different pipelines based on specific criteria. This is especially useful in scenarios where you want to apply different processing or exporting logic to subsets of your telemetry data.

For example, you might want to send *production* data to one exporter while directing *test* or *development* data to another. Similarly, you could route certain spans based on their attributes, such as service name, environment, or span name, to apply custom processing or storage logic.

{{% notice title="Exercise" style="green" icon="running" %}}

> [!IMPORTANT]
> **Change _ALL_ terminal windows to the `[WORKSHOP]/6-routing-data` directory and run the `clear` command.**

Copy `*.yaml` from the `5-transform-data` directory into `6-routing-data`. Your updated directory structure will now look like this:

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}

Next, we will configure the routing connector and the respective pipelines.
