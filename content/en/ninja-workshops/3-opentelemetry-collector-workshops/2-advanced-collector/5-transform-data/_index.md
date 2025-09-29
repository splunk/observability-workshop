---
title: 5. Transform Data
linkTitle: 5. Transform Data
time: 10 minutes
weight: 7
---

The [**Transform Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) lets you modify telemetry data—logs, metrics, and traces—as it flows through the pipeline. Using the **OpenTelemetry Transformation Language (OTTL)**, you can filter, enrich, and transform data on the fly without touching your application code.

In this exercise we’ll update `gateway.yaml` to include a **Transform Processor** that will:

- **Filter** log resource attributes.
- **Parse** JSON structured log data into attributes.
- **Set** log severity levels based on the log message body.

You may have noticed that in previous logs, fields like `SeverityText` and `SeverityNumber` were undefined. This is typical of the `filelog` receiver. However, the severity is embedded within the log body e.g.:

```text
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
```

Logs often contain structured data encoded as JSON within the log body. Extracting these fields into attributes allows for better indexing, filtering, and querying. Instead of manually parsing JSON in downstream systems, OTTL enables automatic transformation at the telemetry pipeline level.

{{% notice title="Exercise" style="green" icon="running" %}}

> [!IMPORTANT]
> **Change _ALL_ terminal windows to the `5-transform-data` directory and run the `clear` command.**

Copy `*.yaml` from the `4-sensitve-data` directory into `5-transform-data`. Your updated directory structure will now look like this:

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}

