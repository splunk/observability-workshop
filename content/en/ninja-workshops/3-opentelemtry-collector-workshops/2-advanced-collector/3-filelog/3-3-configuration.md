---
title: 3.3 Filelog Configuration
linkTitle: 3.3 Filelog Configuration
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}
Move to the **Agent** terminal window and change into the `[WORKSHOP]/3-filelog` directory.  Open the `agent.yaml` copied across earlier and in your editor add the `filelog` receiver to the `agent.yaml`.

**Create the `filelog` receiver and name it `quotes`**: The **FileLog** receiver reads log data from a file and includes custom resource attributes in the log data:

```yaml
  filelog/quotes:                      # Receiver Type/Name
    include: ./quotes.log              # The file to read log data from
    include_file_path: true            # Include file path in the log data
    include_file_name: false           # Exclude file name from the log data
    resource:                          # Add custom resource attributes
      com.splunk.source: ./quotes.log  # Source of the log data
      com.splunk.sourcetype: quotes    # Source type of the log data
```

**Add `filelog/quotes` receiver**: In the `logs:` pipeline only, add the `filelog/quotes:` receiver.

```yaml
    logs:
      receivers:
      - otlp                      # OTLP Receiver
      - filelog/quotes            # Filelog Receiver reading quotes.log
      processors:
      - memory_limiter            # Memory Limiter Processor
      - resourcedetection         # Adds system attributes to the data
      - resource/add_mode         # Adds collector mode metadata
      - batch                     # Batch Processor, groups data before send
      exporters:
      - debug                     # Debug Exporter
      - otlphttp                  # OTLP/HTTP EXporter
```

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `logs:` section of your pipelines will look similar to this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      REC2(filelog<br>fa:fa-download<br>quotes):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resourcedetection<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO4(batch<br>fa:fa-microchip):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
      EXP2(otlphttp<br>fa:fa-upload):::exporter
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
      PRO4 --> EXP1
      PRO4 --> EXP2
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-logs stroke:#34d399,stroke-width:1px, color:#34d399,stroke-dasharray: 3 3;
```
