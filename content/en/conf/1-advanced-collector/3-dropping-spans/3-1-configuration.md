---
title: 3.1 Configuration
linkTitle: 3.1 Configuration
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

Switch to your **Gateway terminal** window and open the `gateway.yaml` file. Update the `processors` section with the following configuration:

1. **Add a `filter` processor**:  
   Configure the gateway to exclude spans with the name `/_healthz`. The `error_mode: ignore` directive ensures that any errors encountered during filtering are ignored, allowing the pipeline to continue running smoothly. The `traces` section defines the filtering rules, specifically targeting spans named `/_healthz` for exclusion.

   ```yaml
     filter/health:                       # Defines a filter processor
       error_mode: ignore                 # Ignore errors
       traces:                            # Filtering rules for traces
         span:                            # Exclude spans named "/_healthz"
          - 'name == "/_healthz"'
   ```

2. **Add the `filter` processor to the `traces` pipeline**:  
   Include the `filter/health` processor in the `traces` pipeline. For optimal performance, place the filter as early as possible—right after the `memory_limiter` and before the `batch` processor. Here’s how the configuration should look:

   ```yaml
   traces:
     receivers:
       - otlp
     processors:
       - memory_limiter
       - filter/health             # Filters data based on rules
       - resource/add_mode
       - batch
     exporters:
       - debug
       - file/traces
   ```

This setup ensures that health check related spans (`/_healthz`) are filtered out early in the pipeline, reducing unnecessary noise in your telemetry data.

{{% /notice %}}

<!--Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `traces:` section of your pipelines will look similar to this:-->

<!--
```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO4(filter<br>fa:fa-microchip<br>health):::processor
      PRO5(batch<br>fa:fa-microchip):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
      EXP2(&ensp;&ensp;file&ensp;&ensp;<br>fa:fa-upload<br>traces):::exporter
    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1[**Traces**]
      direction LR
      REC1 -- > PRO1
      PRO1 -- > PRO4
      PRO4 -- > PRO3
      PRO3 -- > PRO5
      PRO5 -- > EXP1
      PRO5 -- > EXP2
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
-->