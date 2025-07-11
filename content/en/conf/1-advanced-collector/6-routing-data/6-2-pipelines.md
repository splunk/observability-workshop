---
title: 6.2 Configuring the Pipelines
linkTitle: 6.2 Pipeline Configuration
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Update the original `traces` pipeline to use routing**:

1. To enable `routing`, update the original `traces:` pipeline to use `routing` as the only exporter. This ensures all span data is sent through the **Routing Connector** for evaluation and then onwards to connected pipelines. Also, remove **all** processors and replace it with an empty array (`[]`) as this will now behandeld in the `traces/route1-regular` and `traces/route2-security` pipelines, allowing for custom behaviour for each route.  Your `traces:` configuration should look like this:

    ```yaml
    traces:                       # Traces pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors: []              # Processors for traces
      exporters:
      - routing
    ```

**Add both the `route1-regular` and `route2-security` traces pipelines** below the existing `traces:` pipeline:

1. **Configure Route1-regular pipeline**: This pipeline will handle all spans that have  **no match** in the routing table in the connector.
Notice this uses `routing` as its only receiver and will recieve data thought its `connection` from the original traces pipeline. 

    ```yaml
        traces/route1-regular:         # Default pipeline for unmatched spans
          receivers: 
          - routing                    # Receive data from the routing connector
          processors:
          - memory_limiter             # Memory Limiter Processor
          - resource/add_mode          # Adds collector mode metadata
          - batch
          exporters:
          - debug                      # Debug Exporter 
          - file/traces/route1-regular # File Exporter for unmatched spans 
    ```

2. **Add the route2-security pipeline**: This pipeline processes all spans that do match our rule "[deployment.environment"] == "security-applications" in the  the routing rule. This pipeline is also using `routing` as its receiver. Add this  pipline below the `traces/route1-regular` one.

    ```yaml
        traces/route2-security:         # Default pipeline for unmatched spans
          receivers: 
          - routing                     # Receive data from the routing connector
          processors:
          - memory_limiter              # Memory Limiter Processor
          - resource/add_mode           # Adds collector mode metadata
          - batch
          exporters:
          - debug                       # Debug exporter
          - file/traces/route2-security # File exporter for unmatched spans
    ```

{{% /notice %}}

<!--
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
      REC1 -- > ROUTE1
      end
      subgraph subID2[**Traces/standard**]
      ROUTE1 -- > ROUTE2
      ROUTE2 -- > PRO1
      PRO1 -- > PRO3
      PRO3 -- > PRO5
      PRO5 -- > EXP1
      PRO5 -- > EXP2
      end
      subgraph subID3[**Traces/security**]
      ROUTE1 -- > ROUTE3
      ROUTE3 -- > PRO2
      PRO2 -- > PRO4
      PRO4 -- > PRO6
      PRO6 -- > EXP3
      PRO6 -- > EXP4
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
-->