---
title: 3. Dropping Spans
linkTitle: 3. Dropping Spans
time: 10 minutes
weight: 5
---

In this section, we will explore how to use the [**Filter Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md) to selectively drop spans based on certain conditions.

Specifically, we will drop traces based on the span name, which is commonly used to filter out unwanted spans such as health checks or internal communication traces. In this case, we will be filtering out spans whose name is `"/_healthz"`, typically associated with health check requests and usually are quite "**noisy**".

{{% notice title="Exercise" style="green" icon="running" %}}

> [!IMPORTANT]
> **Change _ALL_ terminal windows to the `[WORKSHOP]/3-dropping-spans` directory.**

Copy `*.yaml` from the `2-building-resilience` directory into `3-dropping-spans`. Your updated directory structure will now look like this:

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}

Next, we will configure the **filter processor** and the respective pipelines.
