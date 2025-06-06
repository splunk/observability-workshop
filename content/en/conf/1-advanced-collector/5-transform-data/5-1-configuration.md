---
title: 5.1 Configuration
linkTitle: 5.1 Configuration
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}
**Add a `transform` processor**: Switch to your **Agent terminal** window and edit the `agent.yaml` and add the following `transform` processor:

```yaml
  transform/logs:                      # Processor Type/Name
    log_statements:                    # Log Processing Statements
      - context: resource              # Log Context
        statements:                    # List of attribute keys to keep
          - keep_keys(attributes, ["com.splunk.sourcetype", "host.name", "otelcol.service.mode"])
```

By using the `-context: resource` key we are targeting the `resourceLog` attributes of logs.

This configuration ensures that only the relevant resource attributes (`com.splunk.sourcetype`, `host.name`, `otelcol.service.mode`) are retained, improving log efficiency and reducing unnecessary metadata.

**Adding a Context Block for Log Severity Mapping**: To properly set the `severity_text` and `severity_number` fields of a log record, we add a `log` context block within `log_statements`. This configuration extracts the `level` value from the log body, maps it to `severity_text`, and assigns the corresponding `severity_number` based on the log level:

```yaml
      - context: log                   # Log Context
        statements:                    # Transform Statements Array
          - set(cache, ParseJSON(body)) where IsMatch(body, "^\\{")  # Parse JSON log body into a cache object
          - flatten(cache, "")                                        # Flatten nested JSON structure
          - merge_maps(attributes, cache, "upsert")                   # Merge cache into attributes, updating existing keys
          - set(severity_text, attributes["level"])                   # Set severity_text from the "level" attribute
          - set(severity_number, 1) where severity_text == "TRACE"    # Map severity_text to severity_number
          - set(severity_number, 5) where severity_text == "DEBUG"
          - set(severity_number, 9) where severity_text == "INFO"
          - set(severity_number, 13) where severity_text == "WARN"
          - set(severity_number, 17) where severity_text == "ERROR"
          - set(severity_number, 21) where severity_text == "FATAL"
```

The `merge_maps` function is used to combine two maps (dictionaries) into one. In this case, it merges the `cache` object (containing parsed JSON data from the log body) into the `attributes` map.  

- **Parameters**:  
  - `attributes`: The target map where the data will be merged.  
  - `cache`: The source map containing the parsed JSON data.  
  - `"upsert"`: This mode ensures that if a key already exists in the `attributes` map, its value will be updated with the value from `cache`. If the key does not exist, it will be inserted.  

This step is crucial because it ensures that all relevant fields from the log body (e.g., `level`, `message`, etc.) are added to the `attributes` map, making them available for further processing or exporting.

**Summary of Key Transformations**:

- **Parse JSON**: Extracts structured data from the log body.
- **Flatten JSON**: Converts nested JSON objects into a flat structure.
- **Merge Attributes**: Integrates extracted data into log attributes.
- **Map Severity Text**: Assigns severity_text from the log’s level attribute.
- **Assign Severity Numbers**: Converts severity levels into standardized numerical values.

You should have a **single** `transform` processor containing two context blocks: one whose context is for `resource` and one whose context is for `log`.

This configuration ensures that log severity is correctly extracted, standardized, and structured for efficient processing.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
This method of mapping all JSON fields to top-level attributes should only be used for **testing and debugging OTTL**. It will result in high cardinality in a production scenario.
{{% /notice %}}

**Update the `logs` pipeline**: Add the `transform/logs:` processor into the `logs:` pipeline:

```yaml
    logs:
      receivers:
      - otlp
      - filelog/quotes
      processors:
      - memory_limiter
      - resourcedetection
      - resource/add_mode
      - transform/logs                 # Transform logs processor
      - batch
      exporters:
      - debug
      - otlphttp
```

{{% /notice %}}

Validate the agent configuration using [**https://otelbin.io**](https://otelbin.io/). For reference, the `logs:` section of your pipelines will look similar to this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      REC2(filelog<br>fa:fa-download<br>quotes):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resourcedetection<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO4(transform<br>fa:fa-microchip<br>logs):::processor
      PRO5(batch<br>fa:fa-microchip):::processor
      EXP1(otlphttp<br>fa:fa-upload):::exporter
      EXP2(&ensp;&ensp;debug&ensp;&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-logs
    subgraph " "
      subgraph subID1[**Logs**]
      direction LR
      REC1 --> PRO1
      REC2 --> PRO1
      PRO1 --> PRO2
      PRO2 --> PRO3
      PRO3 --> PRO4
      PRO4 --> PRO5
      PRO5 --> EXP2
      PRO5 --> EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-logs stroke:#34d399,stroke-width:1px, color:#34d399,stroke-dasharray: 3 3;
```
