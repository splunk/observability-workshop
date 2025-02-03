---
title: File Exporter
linkTitle: 1.2. File Exporter
weight: 2
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

Let's configure and add the `FileExporter`:

{{% notice title="Exercise" style="green" icon="running" %}}

- **Configuring a `file` exporter**: Add the following under the `exporters` section of your `agent.yaml`:

  ```yaml
    file:                  # Exporter Type
      path: "./agent.out"  # Path where data will be saved in OTLP json format
      append: false        # Overwrite the file each time
  ```

- **Update the Pipelines Section**: Add the `file` exporter to the `metrics`, `traces` and `logs` pipelines (leave debug as the first in the array). Also, add the `hostmetrics` receiver to the `metrics` pipeline.

  ```yaml
     #traces:
      metrics:                    # Metrics Pipeline
        receivers: [otlp, hostmetrics]         # Array of Metric Receivers
        processors:               # Array of Metric Processors
        - memory_limiter          # Handles memory limits for this Pipeline
        exporters: [debug, file]  # Array of Metric Exporters
     #logs:
  ```

{{% /notice %}}

### Validating your agent.yaml Configuration

To ensure your updated `agent.yaml` is correct, validate it using [**otelbin.io**](https://www.otelbin.io/).
As an example, the `Traces:` section of your pipelines should look similar to this in **otelbin.io**:

![otelbin-a-1-2-w](../../../images/agent-1-2-metrics.png?width=25vw)

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If **otelbin.io** flags a warning regarding the append entry in the exporter you added, check the validation target at the top of the screen. Ensure you’ve selected the Splunk OpenTelemetry Collector as the target.

{{% /notice %}}
