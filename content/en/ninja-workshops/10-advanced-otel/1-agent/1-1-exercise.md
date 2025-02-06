---
title: 1.1 Exercise
linkTitle: 1.1 Exercise
weight: 1
---
Let's walk through a few modifications to our agent configuration to get things started:

{{% notice title="Exercise" style="green" icon="running" %}}

- **Add an `otlp` receiver**: The [**OTLP receiver**](https://docs.splunk.com/observability/en/gdi/opentelemetry/components/otlp-receiver.html) will listen for incoming telemetry data over HTTP (or gRPC).

  ```yaml
    otlp:                           # Receiver Type
      protocols:                    # list of Protocols used 
        http:                       # This wil enable the HTTP Protocol
          endpoint: "0.0.0.0:4318"  # Endpoint for incoming telemetry data
  ```

- **Add a `debug` exporter**: The [**Debug exporter**](https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/debugexporter/README.md) will output detailed debug information for every telemetry record.

  ```yaml  
    debug:                          # Exporter Type
      verbosity: detailed           # Enabled detailed debug output
  ```

- **Update Pipelines**: Ensure that the `otlp` receiver, `memory_limiter` processor, and `debug` exporter are added to the pipelines for `traces`, `metrics`, and `logs`. You can choose to use the format below or use array brackets `[memory_limiter]`:

  ```yaml
      traces:
        receivers:
        - otlp                      # OTLP Receiver 
        processors:
        - memory_limiter            # Memory Limiter Processor  
        exporters:
        - debug                     # Debug Exporter
  ```

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Pay close attention to the formatting, as the OpenTelemetry Collector configuration relies on proper YAML structure.
{{% /notice %}}

During the workshop we will be using the **[otelbin.io](https://www.otelbin.io/)** website for quickly validating YAML syntax and OpenTelemetry configuration correctness. This helps avoid errors before applying configurations in production.

{{% notice title="Usage" style="primary" icon="lightbulb" %}}
Open **[otelbin.io](https://www.otelbin.io/)** and replace the existing configuration by pasting your own YAML into the left pane.
  
At the top of the page, ensure that **Splunk OpenTelemetry Collector** is selected as the validation target.

Once your configuration is validated, refer to the image representation below to check if your pipelines are set up correctly. Usually we will show just the key pipeline,  however when all three pipelines (**Traces**, **Metrics**, and **Logs**) follow the same structure, we will indicate this as show below rather than displaying each one separately.

{{% /notice %}}

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
      subgraph subID1[**Traces**]
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
