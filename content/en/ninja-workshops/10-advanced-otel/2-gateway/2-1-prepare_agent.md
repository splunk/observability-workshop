---
title: 2.1 Test the gateway and prepare the agent
linkTitle: 2.1 Test Gateway & Configure Agent
weight: 1
---

### Test Gateway

Open a third terminal window, this one will be used to run the **Gateway** and navigate to the`[WORKSHOP]/2-gateway` directory and run the following command to test the gateway configuration:

```text
../otelcol --config=gateway.yaml
```

If everything is set up correctly, the first and last lines of the output should look like:

```text
2025/01/15 15:33:53 settings.go:478: Set config to [gateway.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

---

### Update Agent Configuration

Switch to your 'agent' terminal window and navigate to the `[WORKSHOP]/2-gateway` directory.
Open the `agent.yaml` file that you copied earlier in your editor. Replace the existing `file` exporter with an `otlphttp` exporter, as this is now the preferred exporter for Splunk Observability Cloud.

Next, enable the `hostmetric` receiver in the `metrics` pipeline so that you can capture and view system metrics.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Configure the `otlphttp` exporter**: Ensure the `endpoint` is set to the gateway endpoint and add the `X-SF-Token` header with a Splunk Access Token.

  ```yaml
    otlphttp:                       # Exporter Type
      endpoint: "http://localhost:5318" # Gateway endpoint
      headers:                      # Headers to add to the HTTP call 
        X-SF-Token: "ACCESS_TOKEN"  # New way to set an Splunk ACCESS_TOKEN Header
  ```

- **Add a batch processor to the agent**: since the agent can send data from different sources, and benefit from retries, adding a Batch processor is useful too:

  ```yaml
    batch:                          # Processor Type
      metadata_keys: [X-SF-Token]   # Array of metadata keys to batch 
  ```

- **Update Pipelines**: **replace** the `file:` exporter with the `otlphttp` exporter in the `traces`, `metrics`, and `logs` pipelines. Also, **add** the `hostmetrics` receiver to the `metrics` pipeline.

  ```yaml
      metrics:    
        receivers: 
        - otlp                        # OTLP Receiver
        - hostmetrics                 # Hostmetrics Receiver
        processors:
        - memory_limiter              # Memory Limiter Processor
        - resourcedetection           # Adds system attributes to the data
        - resource/add_mode           # Adds collector mode metadata
        - batch                       # Batch Processor, groups data before send
        exporters:
        - debug                       # Debug Exporter 
        - otlphttp                    # OTLP/HTTP EXporter used by Splunk O11Y
  ```

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `metrics:` section of your pipelines will look similar to this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(hostmetrics<br>fa:fa-download):::receiver
      REC2(&nbsp;&nbsp;&nbsp;&nbsp;otlp&nbsp;&nbsp;&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resourcedetection<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO4(batch<br>fa:fa-microchip):::processor
      EXP1(otlphttp<br>fa:fa-upload):::exporter
      EXP2(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-metrics
    subgraph " "
      subgraph subID1[**Metrics**]
      direction LR
      REC1 --> PRO1
      REC2 --> PRO1
      PRO1 --> PRO2
      PRO2 --> PRO3
      PRO3 --> PRO4
      PRO4 --> EXP2
      PRO4 --> EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-metrics stroke:#38bdf8,stroke-width:1px, color:#38bdf8,stroke-dasharray: 3 3;
```
