---
title: 2.1 Start Gateway
linkTitle: 2.1 Start Gateway
weight: 1
---

The configuration for the `gateway` does not need any additional configuration changes to function. This has been done to save time and focus on the core concepts of the **Gateway**.

Validate the `gateway` configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `logs:` section of your pipelines will look similar to this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO3(batch<br>fa:fa-microchip):::processor
      EXP1(&ensp;file&ensp;<br>fa:fa-upload<br>logs):::exporter
      EXP2(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-logs
    subgraph " "
      subgraph subID1[**Logs**]
      direction LR
      REC1 --> PRO1
      PRO1 --> PRO2
      PRO2 --> PRO3
      PRO3 --> EXP2
      PRO3 --> EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-logs stroke:#34d399,stroke-width:1px, color:#34d399,stroke-dasharray: 3 3;
```

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**:

1. Find your **Gateway terminal** window.
2. Navigate to the`[WORKSHOP]/2-gateway` directory.
3. Run the following command to start the `gateway`:

```sh {title="Gateway"}
../otelcol --config=gateway.yaml
```

If everything is configured correctly, the first and last lines of the output should look like:

```text
2025/01/15 15:33:53 settings.go:478: Set config to [gateway.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

{{% /notice %}}

Next, we will configure the `agent` to send data to the newly created `gateway`.
