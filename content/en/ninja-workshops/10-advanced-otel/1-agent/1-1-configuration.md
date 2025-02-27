---
title: 1.1 Validate Configuration
linkTitle: 1.1 Validate Configuration
weight: 1
---

In this workshop, we’ll use [**otelbin.io**](https://otelbin.io) to quickly validate YAML syntax and ensure your OpenTelemetry configurations are accurate. This step helps avoid errors before running tests during the session.

Here’s how to validate your configuration:

1. Open **otelbin.io** and replace the existing configuration by pasting your YAML into the left pane.  
2. At the top of the page, make sure **Splunk OpenTelemetry Collector** is selected as the validation target.  
3. Once validated, refer to the image representation below to confirm your pipelines are set up correctly.  

In most cases, we’ll display only the **key pipeline**. However, if all three pipelines (Traces, Metrics, and Logs) share the same structure, we’ll note this instead of showing each one individually.

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1[**Traces/Metrics/Logs**]
      direction LR
      REC1 --> PRO1
      PRO1 --> EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fff,stroke-width:1px, color:#fff,stroke-dasharray: 3 3;
```
