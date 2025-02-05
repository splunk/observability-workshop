---
title: 8.2 Configuring the Pipelines
linkTitle: 8.2 Pipeline Configuration
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

- **Add both the `standard` and `security` traces pipelines**:

  1. **Standard pipeline**: This pipeline will handle all spans that do not match the routing rule. Add it below the regular `traces:` pipeline, and leave the configuration unchanged for now.

  ```yaml
    pipelines:
      traces/standard:                # New Default Traces/Spans Pipeline    
        receivers: 
        - routing                     # Routing Connector, Only receives data from Connector
        processors:
        - memory_limiter              # Memory Limiter Processor
        - resource/add_mode           # Adds collector mode metadata
        exporters:
        - debug                       # Debug Exporter
        - file/traces/standard        # File Exporter for spans NOT matching rule
  ```

  - **Target pipeline**: This pipeline will handle all spans that match the routing rule.

  ```yaml
    pipelines:
      traces/security:                # New Security Traces/Spans Pipeline       
        receivers: 
        - routing                     # Routing Connector, Only receives data from Connector
        processors:
        - memory_limiter              # Memory Limiter Processor
        - resource/add_mode           # Adds collector mode metadata
        exporters:
        - debug                       # Debug Exporter 
        - file/traces/security        # File Exporter for spans matching rule
  ```

- **Update the `traces` pipeline to use routing**: To enable `routing`, update the original `traces:` pipeline by adding `routing` as an exporter. This ensures that all span data is sent through the routing connector for evaluation.

For clarity, we are removing the `debug` exporter from this pipeline, so that debug output is only shown from the new exporters behind the routing connector.

```yaml
  pipelines:
    traces:                           # Original traces pipeline
      receivers: 
      - otlp                          # Debug Exporter            
      exporters: 
      - routing                       # Routing Connector, Only exports data to Connector
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

Keep in mind that any existing processors have been removed from this pipeline. They are now handled by either the standard pipeline or the target pipelines, depending on the routing rules.

Additionally, the `batch` processor has been removed from the new pipelines. This ensures that `spans` are written immediately, rather than waiting for multiple spans to arrive before processing. This change speeds up the workshop and allows you to see results faster.
{{% /notice %}}

{{% /notice %}}

Again, validate the **Gateway** configuration using `otelbin.io` for spelling mistakes etc. Your `Traces:` pipeline should like this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;&nbsp;otlp&nbsp;&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(memory_limiter<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip):::processor
      PRO4(resource<br>fa:fa-microchip):::processor
      EXP1(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload):::exporter
      EXP2(&emsp;&emsp;file&emsp;&emsp;<br>fa:fa-upload):::exporter
      EXP3(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload):::exporter
      EXP4(&emsp;&emsp;file&emsp;&emsp;<br>fa:fa-upload):::exporter
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
      PRO3 --> EXP1
      PRO3 --> EXP2
      end
      subgraph subID3[**Traces/security**]
      ROUTE1 --> ROUTE3
      ROUTE3 --> PRO2
      PRO2 --> PRO4
      PRO4 --> EXP3
      PRO4 --> EXP4
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```

<!--![Routing Connector](../images/routing-8-1.png)-->

Lets' test our configuration!
