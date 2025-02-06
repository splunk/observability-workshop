---
title: 7. Transform Data
linkTitle: 7. Transform Data
time: 10 minutes
weight: 7
---

The [**Transform Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) lets you modify telemetry data—logs, metrics, and traces—as it flows through the pipeline.

Using the **OpenTelemetry Transformation Language (OTTL)**, you can filter, enrich, and transform data on the fly without touching your application code.

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

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `7-transform`.
- Next, copy all contents from the `6-sensitve-data` directory into `7-routing`.
- After copying, remove any `*.out` and `*.log` files.

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
│   ├── agent.yaml
│   ├── gateway.yaml
│   ├── health.json
│   ├── log-gen.sh (or .ps1)
│   └── trace.json
└── otelcol
```

{{% /tab %}}
{{% /tabs %}}

We’ll update `agent.yaml` to include a Transform Processor that will:

- **Filter** log resource attributes
- **Parse** JSON structured log data into attributes
- **Set** log severity levels based on the log message body

You may have noticed that in previous logs, fields like `SeverityText` and `SeverityNumber` were undefined (this is typical of the filelog receiver). However, the severity is embedded within the log body:

```text
<snip>
LogRecord #0
ObservedTimestamp: 2025-01-31 21:49:29.924017 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
Attributes:
     -> log.file.path: Str(quotes.log)
Trace ID:
Span ID:
Flags: 0
  {"kind": "exporter", "data_type": "logs", "name": "debug"}
```

Logs often contain structured data encoded as JSON within the log body. Extracting these fields into attributes allows for better indexing, filtering, and querying. Instead of manually parsing JSON in downstream systems, OTTL enables automatic transformation at the telemetry pipeline level.

{{% notice title="Exercise" style="green" icon="running" %}}
- **Update Agent.yaml** Switch to your **Agent** terminal window and navigate to the `[WORKSHOP]/7-transform-data` directory. Open the `agent.yaml` file that you copied earlier in your editor.

- **Configure the `transform(logs)` processor:** Ensure the processor is applied to `log_statements` in the `resource` context and filter the resource attributes, keeping only relevant metadata fields (`com.splunk.sourcetype`, `host.name`, `otelcol.service.mode`):

  ```yaml
  transform/logs:                     # Processor Type/Name
    log_statements:                   # Log Processing Statements
      - context: resource             # Log Context
        statements:                   # Transform Statements Array
          - keep_keys(attributes, ["com.splunk.sourcetype","host.name", "otelcol.service.mode"])
            #List of attribute keys to keep

  ```

- **Add another context block** to the `log_statements` and set the `severity_text` and `severity_number` of the log record based on the matching severity `level` from the log `body`.

  ```yaml
      - context: log                  # Log Context
        statements:                   # Transform Statements Array
          - set(cache, ParseJSON(body)) where IsMatch(body, "^\\{")  
            # Parses the log body as JSON and stores the result in a temporary 'cache' variable 
            # Only applies if the body starts with '{', indicating it's JSON-formatted

          - flatten(cache, "")        
            # Flattens the JSON structure in 'cache' to remove nested levels, making all keys top-level
            # Useful for simplifying complex JSON logs

          - merge_maps(attributes, cache, "upsert")  
            # Merges the flattened 'cache' data into the log's attributes
            # 'upsert' ensures that existing keys are updated, and new keys are added

          - set(severity_text, attributes["level"])  
            # Maps the 'level' attribute from the log data to the OpenTelemetry 'severity_text' field
            # Ensures that log severity levels are standardized

          - set(severity_number, 1) where severity_text == "TRACE"  
          - set(severity_number, 5) where severity_text == "DEBUG"  
          - set(severity_number, 9) where severity_text == "INFO"   
          - set(severity_number, 13) where severity_text == "WARN"  
          - set(severity_number, 17) where severity_text == "ERROR"  
          - set(severity_number, 21) where severity_text == "FATAL"  
            # Assigns severity numbers by log level

  ```



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
{{% notice title="Tip" style="primary" icon="lightbulb" %}}
This method of mapping all JSON fields to top-level attributes should only be used for **testing and debugging OTTL**. It will result in high cardinality in a production scenario.
{{% /notice %}}
