---
title: File Exporter
linkTitle: 1.2. File Exporter
weight: 2
mermaidZoom: true
---

To capture more than just debug output on the screen, we also want to generate output during the export phase of the pipeline. For this, we'll add a **File Exporter** to write OTLP data to files for comparison.

The difference between the OpenTelemetry **debug exporter** and the **file exporter** lies in their purpose and output destination:

| Feature             | Debug Exporter                  | File Exporter                 |
|---------------------|---------------------------------|-------------------------------|
| **Output Location** | Console/Log                     | File on disk                  |
| **Purpose**         | Real-time debugging             | Persistent offline analysis   |
| **Best for**        | Quick inspection during testing | Temporary storage and sharing |
| **Production Use**  | No                              | Rare, but possible            |
| **Persistence**     | No                              | Yes                           |

In summary, the **debug exporter** is great for real-time, in-development troubleshooting, while the **file exporter** is better suited for storing telemetry data locally for later use.

Find your `Agent` terminal window, and stop the running collector by pressing `Ctrl-C`. Once the `agent` has stopped, open the `agent.yaml` and configure the `FileExporter`:

{{% notice title="Exercise" style="green" icon="running" %}}

- **Configuring a `file` exporter**: Add the following under the `exporters` section of your `agent.yaml`:

  ```yaml
    file:                           # Exporter Type
      path: "./agent.out"           # Path where data will be saved in OTLP json format
      append: false                 # Overwrite the file each time
  ```

- **Update the Pipelines Section**: Add the `file` exporter to the `metrics`, `traces` and `logs` pipelines (leave debug as the first in the array).

  ```yaml
      #traces:       
      metrics:
        receivers:
        - otlp                      # OTLP Receiver
        processors:
        - memory_limiter            # Memory Limiter Processor
        exporters:
        - debug                     # Debug Exporter
        - file                      # File Exporter
      #logs:
  ```

{{% /notice %}}

To verify that your updated `agent.yaml` file is correct, validate it using [**otelbin.io**](https://www.otelbin.io/).

For reference, the `traces:` section of your pipelines should look similar to this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
      EXP2(&ensp;file&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1[Traces/Metrics/Logs]
      direction LR
      REC1 --> PRO1
      PRO1 --> EXP1
      PRO1 --> EXP2
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fff,stroke-width:2px, color:#fff,stroke-dasharray: 5 5;
```

<!--
![otelbin-a-1-2-w](../../images/agent-1-2-metrics.png?width=25vw)
-->

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If **otelbin.io** shows a warning regarding the `scraper` or`append` keys, check the validation target at the top of the page. Make sure the **Splunk OpenTelemetry Collector** is selected as the validation target.
{{% /notice %}}
