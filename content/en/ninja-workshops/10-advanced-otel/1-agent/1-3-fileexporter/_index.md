---
title: 1.3 File Exporter
linkTitle: 1.3. File Exporter
weight: 2
---

To capture more than just debug output on the screen, we also want to generate output during the export phase of the pipeline. For this, we'll add a **File Exporter** to write OTLP data to files for comparison. The difference between the OpenTelemetry **debug exporter** and the **file exporter** lies in their purpose and output destination:

| Feature             | Debug Exporter                  | File Exporter                 |
|---------------------|---------------------------------|-------------------------------|
| **Output Location** | Console/Log                     | File on disk                  |
| **Purpose**         | Real-time debugging             | Persistent offline analysis   |
| **Best for**        | Quick inspection during testing | Temporary storage and sharing |
| **Production Use**  | No                              | Rare, but possible            |
| **Persistence**     | No                              | Yes                           |

In summary, the **Debug Exporter** is great for real-time, in-development troubleshooting, while the **File Exporter** is better suited for storing telemetry data locally for later use.

{{% notice title="Exercise" style="green" icon="running" %}}

Find your **Agent** terminal window, and stop the running collector by pressing `Ctrl-C`. Once the **Agent** has stopped, open the `agent.yaml` and configure the **File Exporter**:

- **Configuring a `file` exporter**: The [**File Exporter**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/fileexporter/README.md) writes telemetry data to files on disk.

  ```yaml
    file:                           # Exporter Type
      path: "./agent.out"           # Save path (OTLP JSON)
      append: false                 # Overwrite the file each time
  ```

- **Update the Pipelines Section**: Add the `file` exporter to the `metrics`, `traces` and `logs` pipelines (leave debug as the first in the array).

  ```yaml
      metrics:
        receivers:
        - otlp                      # OTLP Receiver
        processors:
        - memory_limiter            # Memory Limiter Processor
        exporters:
        - debug                     # Debug Exporter
        - file                      # File Exporter
  ```

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**:

```mermaid
flowchart LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
      EXP2(&ensp;&ensp;file&ensp;&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1[**Traces/Metrics/Logs**]
      direction LR
      REC1 --> PRO1
      PRO1 --> EXP1
      PRO1 --> EXP2
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fff,stroke-width:1px, color:#fff,stroke-dasharray: 3 3;
```
