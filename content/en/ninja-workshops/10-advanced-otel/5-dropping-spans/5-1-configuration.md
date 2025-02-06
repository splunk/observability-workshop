---
title: 5.1 Configuration
linkTitle: 5.1 Configuration
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

Switch to your **Gateway** terminal window. Navigate to the `[WORKSHOP]/5-dropping-spans` directory and open the `gateway.yaml` and add the following configuration to the `processors` section:

- **Add a `filter` processor**: Configure the OpenTelemetry Collector to drop spans with the name `"/_healthz"`:

  ```yaml
    
    filter/health:                 # Defines a filter processor
      error_mode: ignore           # Ignore errors
      traces:                      # Filtering rules for traces
        span:                      # Exclude spans named "/_healthz"  
          - 'name == "/_healthz"'
  ```

- **Add the `filter` processor**: Make sure you add the filter to the `traces` pipeline. Filtering should be applied as early as possible, ideally *right after the* memory_limiter and *before* the batch processor.

  ```yaml
  traces:
    receivers:              # Data input sources
      - otlp
    processors:             # Processing steps in the pipeline
      - memory_limiter      # Manage memory usage
      - resourcedetection   # Add system attributes
      - resource/add_mode   # Add metadata about collector mode
      - filter/health
      - batch
    exporters:              # Output destinations
      - debug
      - file
  ```

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `traces:` section of your pipelines will look similar to this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resourcedetection<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip):::processor
      PRO4(filter<br>fa:fa-microchip):::processor
      PRO5(batch<br>fa:fa-microchip):::processor
      PRO6(attributes<br>fa:fa-microchip):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
      EXP2(&ensp;&ensp;file&ensp;&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1[**Traces**]
      direction LR
      REC1 --> PRO1
      PRO1 --> PRO6
      PRO6 --> PRO2
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
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
