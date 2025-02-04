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
graph LR
  subgraph box[Logs]
    direction LR
    %% Nodes
      A[otlp<br>fa:fa-download]:::receiver
      C[filelog<br>fa:fa-download]:::receiver
      D[memory_limiter<br>fa:fa-microchip]:::processor
      E[resource<br>fa:fa-microchip]:::processor
      F[resourcedetection<br>fa:fa-microchip]:::processor      
      J[batch<br>fa:fa-microchip]:::processor
      L[debug<br>fa:fa-upload]:::exporter
      N[otlphttp<br>fa:fa-upload]:::exporter

    end
    %% Links
      A --> D
      C --> D
      D --> F
      F --> E
      E --> J
      J --> L
      J --> N

classDef receiver fill:#8b5cf6,stroke:#333,stroke-width:2px,padding-left:110px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:2px,padding-left:110px,color:#fff;
classDef exporter fill:#8b5cf6,stroke:#333,stroke-width:2px, padding-left:110px,color:#fff;
style box stroke:#333,stroke-width:2px,fill:#f9a9a9a;
```
<!--
![otelbin-f-3-1-logs](../../images/filelog-3-1-logs.png)
-->
