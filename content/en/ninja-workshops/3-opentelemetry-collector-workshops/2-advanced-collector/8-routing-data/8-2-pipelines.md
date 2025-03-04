---
title: 8.2 Configuring the Pipelines
linkTitle: 8.2 Pipeline Configuration
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Add both the `standard` and `security` traces pipelines**:

1. **Add the Standard pipeline**: This pipeline processes all spans that do not match the routing rule.  
This pipeline is using `routing` as its receiver. Place it below the existing `traces:` pipeline, keeping its configuration unchanged for now:

    ```yaml
        traces/standard:              # Default pipeline for unmatched spans
          receivers: 
          - routing                   # Receive data from the routing connector
          processors:
          - memory_limiter            # Memory Limiter Processor
          - resource/add_mode         # Adds collector mode metadata
          - batch
          exporters:
          - debug                     # Debug exporter
          - file/traces/standard      # File exporter for unmatched spans
    ```

2. **Configure the Security pipeline**: This pipeline will handle all spans that match the routing rule.  
This also uses `routing` as its receiver. Add this below the Standard one:

    ```yaml
        traces/security:              # New Security Traces/Spans Pipeline
          receivers: 
          - routing                   # Routing Connector, Only receives data from Connector
          processors:
          - memory_limiter            # Memory Limiter Processor
          - resource/add_mode         # Adds collector mode metadata
          - batch
          exporters:
          - debug                     # Debug Exporter 
          - file/traces/security      # File Exporter for spans matching rule
    ```

**Update the `traces` pipeline to use routing**:

1. To enable `routing`, update the original `traces:` pipeline by using `routing` as the only exporter.  
This ensures all span data is sent through the routing connector for evaluation.
2. Remove all processors and replace it with an empty array (`[]`). These are now defined in the `traces/standard` and `traces/security` pipelines.

    ```yaml
      pipelines:
        traces:                           # Original traces pipeline
          receivers: 
          - otlp                          # OTLP Receiver
          processors: []
          exporters: 
          - routing                       # Routing Connector
    ```

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `traces:` section of your pipelines will look similar to this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;&nbsp;otlp&nbsp;&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(memory_limiter<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO4(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO5(batch<br>fa:fa-microchip):::processor
      PRO6(batch<br>fa:fa-microchip):::processor
      EXP1(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload):::exporter
      EXP2(&emsp;&emsp;file&emsp;&emsp;<br>fa:fa-upload<br>traces):::exporter
      EXP3(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload):::exporter
      EXP4(&emsp;&emsp;file&emsp;&emsp;<br>fa:fa-upload<br>traces):::exporter
      ROUTE1(&nbsp;routing&nbsp;<br>fa:fa-route):::con-export
      ROUTE2(&nbsp;routing&nbsp;<br>fa:fa-route):::con-receive
      ROUTE3(&nbsp;routing&nbsp;<br>fa:fa-route):::con-receive
    %% Links
    subID1:::sub-traces
    subID2:::sub-traces
    subID3:::sub-traces
    subgraph " "
    direction LR
      subgraph subID1[**Traces**]
      REC1 --> ROUTE1
      end
      subgraph subID2[**Traces/standard**]
      ROUTE1 --> ROUTE2
      ROUTE2 --> PRO1
      PRO1 --> PRO3
      PRO3 --> PRO5
      PRO5 --> EXP1
      PRO5 --> EXP2
      end
      subgraph subID3[**Traces/security**]
      ROUTE1 --> ROUTE3
      ROUTE3 --> PRO2
      PRO2 --> PRO4
      PRO4 --> PRO6
      PRO6 --> EXP3
      PRO6 --> EXP4
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```

Lets' test our configuration!
