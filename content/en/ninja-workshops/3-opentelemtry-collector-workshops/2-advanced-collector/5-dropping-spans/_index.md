---
title: 5. Dropping Spans
linkTitle: 5. Dropping Spans
time: 10 minutes
weight: 5
---

In this section, we will explore how to use the [**Filter Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md) to selectively drop spans based on certain conditions.

Specifically, we will drop traces based on the span name, which is commonly used to filter out unwanted spans such as health checks or internal communication traces. In this case, we will be filtering out spans whose name is `"/_healthz"`, typically associated with health check requests and usually are quite "**noisy**".

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `5-dropping-spans`.
- Next, copy all contents from the `4-resilience` directory into `5-dropping-spans`.
- After copying, remove any `*.out` and `*.log` files.
- Change **all** terminal windows to the `[WORKSHOP]/5-dropping-spans` directory.

Your updated directory structure will now look like this:

```text { title="Updated Directory Structure" }
[WORKSHOP]
└── 5-dropping-spans
    ├── checkpoint-dir
    ├── agent.yaml
    └── gateway.yaml
```

{{% /notice %}}

Next, we will configure the **filter processor** and the respective pipelines.
