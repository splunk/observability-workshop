---
title: 7. Transform Data
linkTitle: 7. Transform Data
time: 10 minutes
weight: 7
---

The [**Transform Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) lets you modify telemetry data—logs, metrics, and traces—as it flows through the pipeline. Using the **OpenTelemetry Transformation Language (OTTL)**, you can filter, enrich, and transform data on the fly without touching your application code.

In this exercise we’ll update `agent.yaml` to include a **Transform Processor** that will:

- **Filter** log resource attributes.
- **Parse** JSON structured log data into attributes.
- **Set** log severity levels based on the log message body.

You may have noticed that in previous logs, fields like `SeverityText` and `SeverityNumber` were undefined (this is typical of the `filelog` receiver). However, the severity is embedded within the log body:

```text
<snip>
LogRecord #0
ObservedTimestamp: 2025-01-31 21:49:29.924017 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
</snip>
```

Logs often contain structured data encoded as JSON within the log body. Extracting these fields into attributes allows for better indexing, filtering, and querying. Instead of manually parsing JSON in downstream systems, OTTL enables automatic transformation at the telemetry pipeline level.

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `7-transform`.
- Next, copy all contents from the `6-sensitve-data` directory into `7-transform`.
- After copying, remove any `*.out` and `*.log` files.
- Change **all** terminal windows to the `[WORKSHOP]/7-transform` directory.

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
│   ├───checkpoint-dir
│   ├── agent.yaml
│   ├── gateway.yaml
│   ├── health.json
│   ├── log-gen.sh (or .ps1)
│   └── trace.json
└── otelcol
```

{{% /tab %}}
{{% /tabs %}}
{{% /notice %}}
