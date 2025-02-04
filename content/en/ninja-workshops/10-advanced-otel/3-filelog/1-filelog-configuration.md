---
title: Filelog Receiver Configuration
linkTitle: 3.1 Filelog Configuration
weight: 1
---

Check that you are in the `[WORKSHOP]/3-filelog` directory.  Open the `agent.yaml` copied across earlier and in your editor and add the `filelog` receiver to the `agent.yaml`.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Add the `filelog` receiver**: The Filelog receiver reads log data from a file and includes custom resource attributes in the log data:

  ```yaml
    # Define a filelog receiver named "quotes"
    filelog/quotes:
      # Specifies the file to read log data from (quotes.log)
      include: ./quotes.log
      # Includes the full file path in the log data
      include_file_path: true
      # Excludes the file name from the log data
      include_file_name: false
      # Add custom resource attributes to the log data
      resource:
        # Sets the source of the log data to "quotes.log"
        com.splunk.source: ./quotes.log
        # Sets the sourcetype for the log data to "quotes"
        com.splunk.sourcetype: quotes
  ```

- Add `filelog/quotes` receiver to the `receivers` array in the `logs` section of the pipelines.  (make sure it also contains `otlp`)

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**, the results for the `Logs` pipeline should look like this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      REC2(filelog<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resourcedetection<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip):::processor
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
classDef sub-logs stroke:#34d399,stroke-width:2px, color:#34d399,stroke-dasharray: 5 5;
```

<!--![otelbin-f-3-1-logs](../../images/filelog-3-1-logs.png)-->
