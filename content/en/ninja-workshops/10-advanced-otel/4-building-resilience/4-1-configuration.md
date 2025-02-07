---
title: 4.1 File Storage Configuration
linkTitle: 4.1 Configuration
weight: 1
---

In this exercise, we will update the `extensions:` section of the `agent.yaml` file. This section is part of the OpenTelemetry configuration YAML and defines optional components that enhance or modify the OpenTelemetry Collector’s behavior.

While these components do not process telemetry data directly, they provide valuable capabilities and services to improve the Collector’s functionality.

{{% notice title="Exercise" style="green" icon="running" %}}

**Update the `agent.yaml`**: Add the `file_storage` extension and name it `checkpoint`:

```yaml
  file_storage/checkpoint:         # Extension Type/Name
    directory: "./checkpoint-dir"  # Define directory
    create_directory: true         # Create directory
    timeout: 1s                    # Timeout for file operations
    compaction:                    # Compaction settings
      on_start: true               # Start compaction at Collector startup
      # Define compaction directory
      directory: "./checkpoint-dir/tmp"
      # Max. size limit before compaction occurs
      max_transaction_size: 65536
```

**Add `file_storage` to existing `otlphttp` exporter**: Modify the `otlphttp:` exporter to configure retry and queuing mechanisms, ensuring data is retained and resent if failures occur:

```yaml
  otlphttp:                       # Exporter Type
    endpoint: "http://localhost:5318" # Gateway OTLP endpoint
    headers:                      # Headers to add to the HTTPcall 
      X-SF-Token: "ACCESS_TOKEN"  # Splunk ACCESS_TOKEN header
    retry_on_failure:             # Retry on failure settings
      enabled: true               # Enables retrying
    sending_queue:                # Sending queue settings
      enabled: true               # Enables Sending queue
      num_consumers: 10           # Number of consumers
      queue_size: 10000           # Maximum queue size
      # File storage extension
      storage: file_storage/checkpoint
```

**Update the `services` section**: Add the `file_storage/checkpoint` extension to the existing `extensions:` section. This will cause the extension to be enabled:

```yaml
service:
  extensions:
  - health_check
  - file_storage/checkpoint       # Enabled extensions for this collector
```

**Update the `metrics` pipeline**: For this exercise we are going to remove the `hostmetrics` receiver from the Metric pipeline to reduce debug and log noise:

```yaml
  metrics:
    receivers: 
    - otlp                        # OTLP Receiver
    # - hostmetrics               # Hostmetrics Receiver
```

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `logs:` section of your pipelines will look similar to this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
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
