---
title: Create metrics using the count connector
linkTitle: a. Sum connector
time: 10 minutes
weight: 10
---

In this section, we will explore how to use the [**count Connector**](https://docs.splunk.com/observability/en/gdi/opentelemetry/components/count-connector.html) can be used to count attribute values from spans, span events, metrics, data points, and log records.

In this section we will use the count connector to count the number of Star Wars or Lord of the Rings quotes provided by our logs.

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `a-sum`.
- Next, copy all contents from the `8-routing-data` directory into `a-sum`.
- After copying, remove any `*.out` and `*.log` files.
- Change **all** terminal windows to the `[WORKSHOP]/a-sum` directory.

Next, we will configure the **Count Connector** and the respective pipelines.

- **Add a Count Connector**

count:
    metrics:
      starwars_count:
        description: "Count of 'Star Wars' Quotes in logs"
        conditions:
        - attributes["Movies"] == "SW"
      lotr_count:
        description: "Count of 'Lord of the Rings' Quotes in logs"
        unit: "1"
        aggregation: "count"

{{% /notice %}}