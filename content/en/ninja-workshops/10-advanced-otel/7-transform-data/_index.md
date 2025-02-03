---
title: Transform Data
linkTitle: 7. Transform Data
time: 10 minutes
weight: 7
---

The Transform Processor allows users to modify telemetry data (logs, metrics, and traces) as it passes through the pipeline. It enables users to filter, enrich, or transform data using the OpenTelemetry Transformation Language (OTTL).

### Setup

Create a new subdirectory named `7-transform-data` and copy all contents from the `6-senstive-data` directory into it. Then, delete any `*.out` and `*.log` files. Your updated directory structure should now look like this:

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
│   ├── gateway.yaml
│   ├── agent.yaml
│   ├── log-gen.sh (or .ps1)
│   ├── health.json
│   └── trace.json
└── otelcol
```

{{% /tab %}}

In this section, we will update the `agent.yaml` file to include a **transform** processor. This processor will help filter log resource attributes and set the log severity text based on the message body.

Previously, you may have noticed that the `SeverityText` and `SeverityNumber` values are undefined in the log record, but the severity is included in the `level` field of the log body

```text
<snip>
LogRecord #0
ObservedTimestamp: 2025-01-31 21:49:29.924017 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText: WARN
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
Attributes:
     -> log.file.path: Str(quotes.log)
Trace ID:
Span ID:
Flags: 0
  {"kind": "exporter", "data_type": "logs", "name": "debug"}
```

So, let's start an exercise to use a transform processor to enrich and filter the log record data.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Add a `Transform` Processor** and name it `logs:`
The `transform` processor allows you to manipulate logs, traces, and metrics dynamically without modifying application code.

In this case, we will be filtering the resource attributes and keeping only relevant metadata fields (`com.splunk.sourcetype`, `host.name`, `otelcol.service.mode`):

  ```yaml
  transform/logs:
    log_statements: 
      - context: resource
        statements:
          - keep_keys(attributes, ["com.splunk.sourcetype","host.name", "otelcol.service.mode"])
  ```

Notice that the `keep_keys` statement is only applicable to the log resource context.

Logs often contain structured data encoded as JSON within the log body. Extracting these fields into attributes allows for better indexing, filtering, and querying. Instead of manually parsing JSON in downstream systems, OTTL enables automatic transformation at the telemetry pipeline level.

- **Add another context block** for the log along with set statements to set the severity_text and severity_number of the log record based on the matching severity level from the log body.

  ```yaml
      - context: log
        statements:
      - context: log
        statements:
          - set(cache, ParseJSON(body)) where IsMatch(body, "^\\{")
          - flatten(cache, "")
          - merge_maps(attributes, cache, "upsert")
          - set(severity_text, attributes["level"])
          - set(severity_number, 1) where severity_text == "TRACE"
          - set(severity_number, 5) where severity_text == "DEBUG"
          - set(severity_number, 9) where severity_text == "INFO"
          - set(severity_number, 13) where severity_text == "WARN"
          - set(severity_number, 17) where severity_text == "ERROR"
          - set(severity_number, 21) where severity_text == "FATAL"
  ```
This transformation checks if the log body contains a JSON object, then extracts its fields into log attributes while preserving nested structures. The flatten(cache) step ensures that deeply nested JSON fields can be accessed as top-level attributes. 



- **Update the `logs` pipeline**: Add the `transform` processor into the `logs:` pipeline:

  ```yaml
  logs:                                   # Logs Pipeline
      receivers: [filelog/quotes, otlp]   # Array of receivers in this pipeline
      processors:         # Array of Processors in this pipeline
      - memory_limiter    # You also could use [memory_limiter]
      - resourcedetection
      - resource/add_mode
      - transform/logs
      - batch
  ```

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**, the results for the `Logs` pipeline should look like this:

![redacting 1](../images/transform-data-7-1.png)
