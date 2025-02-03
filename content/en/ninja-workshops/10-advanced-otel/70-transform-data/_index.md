---
title: Transform Data
linkTitle: 7. Transform Data
time: 10 minutes
weight: 7
---

The Transform Processor allows users to modify telemetry data (logs, metrics, and traces) as it passes through the pipeline. It enables users to filter, enrich, or transform data using OpenTelemetry's Telemetry Query Language (OTTL)

### Setup

On your machine, navigate to the directory where you're running the workshop. Create a new subdirectory called `7-transform-data`, then copy the latest versions of `agent.yaml` and `trace.json` from `[WORKSHOP]/6-sensitive-data` into this new directory.

Next, move into the `[WORKSHOP]/7-transform-data` directory.

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

Previously, you may have noticed that the `SeverityText` and `SeverityNumber` values are undefined in the log record, but are included in the log message body

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

So, Let's start an exercise to use a transform processor to enrich and filter the log record data.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Add a `Transform` Processor** and name it `logs:`
The `transform` processor allows you to manipulate logs, traces, and metrics dynamically without modifying application code. 

In this case, we will be filtering the resource attributes and keeping only relevant metadata fields (sourcetype, host.name, service.mode) 

  ```yaml
  transform/logs:
    log_statements: 
      - context: resource
        statements:
          - keep_keys(attributes, ["com.splunk.sourcetype","host.name", "otelcol.service.mode"])
  ```
Notice that the keep_keys statement is only applicable to the log resource context. 

- **Add an other context block for the log along with set statements to set the severity_text of the log record based on the matching severity level from the unstructured log. 

  ```yaml
      - context: log
        statements:
          - set(severity_text, "INFO") where IsMatch(body, "\\[INFO\\]")
          - set(severity_text, "WARN") where IsMatch(body, "\\[WARN\\]")
          - set(severity_text, "DEBUG") where IsMatch(body, "\\[DEBUG\\]")
          - set(severity_text, "ERROR") where IsMatch(body, "\\[ERROR\\]")
  ```

- **Update the `logs` pipeline**: Add the `transform` processor into the `logs:` pipeline 

  ```yaml
  logs:                  # Logs Pipeline
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
