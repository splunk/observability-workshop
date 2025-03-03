---
title: 8. Routing Data
linkTitle: 8. Routing Data
time: 10 minutes
weight: 8
---

The [**Routing Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) in OpenTelemetry is a powerful feature that allows you to direct data (`traces`, `metrics`, or `logs`) to different pipelines based on specific criteria. This is especially useful in scenarios where you want to apply different processing or exporting logic to subsets of your telemetry data.

For example, you might want to send *production* data to one exporter while directing *test* or *development* data to another. Similarly, you could route certain spans based on their attributes, such as service name, environment, or span name, to apply custom processing or storage logic.

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `8-routing-data`.
- Next, copy `*.yaml` from the `7-transform-data` directory into `8-routing-data`.
- Change **all** terminal windows to the `[WORKSHOP]/8-routing-data` directory.

Your updated directory structure will now look like this:

```text { title="Updated Directory Structure" }
[WORKSHOP]
└── 8-routing
    ├── agent.yaml
    └── gateway.yaml
```

{{% /notice %}}

Next, we will configure the routing connector and the respective pipelines.
