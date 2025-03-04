---
title: Create metrics using the Sum connector
linkTitle: a. Sum connector
time: 10 minutes
weight: 10
---

In this section, we will explore how to use the [**Sum Connector**](https://docs.splunk.com/observability/en/gdi/opentelemetry/components/sum-connector.html) can be used to sum attribute values from spans, span events, metrics, data points, and log records.

In this section we will use the sum connector to create metrics from our to create metrics from our logs based on certain conditions.

<!--
Specifically, we will drop traces based on the span name, which is commonly used to filter out unwanted spans such as health checks or internal communication traces. In this case, we will be filtering out spans whose name is `"/_healthz"`, typically associated with health check requests and usually are quite "**noisy**".
!-->

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `a-sum`.
- Next, copy all contents from the `8-routing-data` directory into `a-sum`.
- After copying, remove any `*.out` and `*.log` files.
- Change **all** terminal windows to the `[WORKSHOP]/a-sum` directory.

Next, we will configure the **Sum Connector** and the respective pipelines.

- **Add a sum connector**

sum:
    metrics:
      starwars_count:
        description: "Count of 'starwars' in logs"
        conditions:
        - attributes["severity"] == "ERROR"
      lotr_count:
        description: "Count of 'lotr' in logs"
        unit: "1"
        aggregation: "count"




{{% /notice %}}