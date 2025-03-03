---
title: Create metrics using the Sum connector
linkTitle: a. Sum connector
time: 10 minutes
weight: 10
---

In this section, we will explore how to use the [**Sum Connector**](https://docs.splunk.com/observability/en/gdi/opentelemetry/components/sum-connector.html) to create metrics from our logs based on certain conditions.

<!--
Specifically, we will drop traces based on the span name, which is commonly used to filter out unwanted spans such as health checks or internal communication traces. In this case, we will be filtering out spans whose name is `"/_healthz"`, typically associated with health check requests and usually are quite "**noisy**".
!-->

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `a-sum`.
- Next, copy `*.yaml` from the `8-routing-data` directory into `a-sum`.
- Change **all** terminal windows to the `[WORKSHOP]/5-dropping-spans` directory.

Your updated directory structure will now look like this:

```text { title="Updated Directory Structure" }
[WORKSHOP]
└── 5-dropping-spans
    ├── agent.yaml
    └── gateway.yaml
```

{{% /notice %}}

Next, we will configure the **filter processor** and the respective pipelines.
