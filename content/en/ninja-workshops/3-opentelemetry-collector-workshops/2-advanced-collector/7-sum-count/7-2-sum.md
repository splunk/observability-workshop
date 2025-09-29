---
title: 7.2 Create metrics with Sum Connector
linkTitle: 7.2 Sum Connector
time: 10 minutes
weight: 2
---

In this section, we’ll explore how the [**Sum Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/sumconnector) can extract values from spans and convert them into metrics.  

We’ll specifically use the credit card charges from our base spans and leverage the Sum Connector to retrieve the total charges as a metric.

The connector can be used to collect (**sum**) attribute values from spans, span events, metrics, data points, and log records. It captures each individual value, transforms it into a metric, and passes it along. However, it’s the **backend’s** job to use these metrics and their attributes for calculations and further processing.

{{% notice title="Exercise" style="green" icon="running" %}}

Switch to your **Agent terminal** window and open the `agent.yaml` file in your editor.

- **Add the Sum Connector**  
Include the Sum Connector in the connectors section of your configuration and define the metrics counters:

```yaml
  sum:
    spans:
       user.card-charge:
        source_attribute: payment.amount
        conditions:
          - attributes["payment.amount"] != "NULL"
        attributes:
          - key: user.name
    
```

{{% /notice %}}

In the example above, we check for the `payment.amount` attribute in spans. If it has a valid value, the **Sum** connector generates a metric called `user.card-charge` and includes the `user.name` as an attribute. This enables the backend to track and display a user’s total charges over an extended period, such as a billing cycle.

In the pipeline configuration below, the connector exporter is added to the traces section, while the connector receiver is added to the metrics section.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Configure the Count Connector in the pipelines**

```yaml
  pipelines:
    traces:
      receivers:
      - otlp
      processors:
      - memory_limiter
      - attributes/update              # Update, hash, and remove attributes
      - redaction/redact               # Redact sensitive fields using regex
      - resourcedetection
      - resource/add_mode
      - batch
      exporters:
      - debug
      - file
      - otlphttp
      - sum                            # Sum connector which aggregates payment.amount from spans and sends to metrics pipeline
    metrics:
      receivers:
      - sum                            # Receives metrics from the sum exporter in the traces pipeline
      - count                          # Receives count metric from logs count exporter in logs pipeline. 
      - otlp
      #- hostmetrics                   # Host Metrics Receiver
      processors:
      - memory_limiter
      - resourcedetection
      - resource/add_mode
      - batch
      exporters:
      - debug
      - otlphttp
    logs:
      receivers:
      - otlp
      - filelog/quotes
      processors:
      - memory_limiter
      - resourcedetection
      - resource/add_mode
      - transform/logs                 # Transform logs processor
      - batch
      exporters:
      - count                          # Count Connector that exports count as a metric to metrics pipeline.
      - debug
      - otlphttp
```

- **Validate** the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `traces` and `metrics:` sections of your pipelines will look like this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
    REC1(otlp<br>fa:fa-download<br> ):::receiver
    REC3(otlp<br>fa:fa-download<br> ):::receiver
    PRO1(memory_limiter<br>fa:fa-microchip<br> ):::processor
    PRO2(memory_limiter<br>fa:fa-microchip<br> ):::processor
    PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
    PRO4(resource<br>fa:fa-microchip<br>add_mode):::processor
    PRO5(batch<br>fa:fa-microchip<br> ):::processor
    PRO6(batch<br>fa:fa-microchip<br> ):::processor
    PRO7(resourcedetection<br>fa:fa-microchip<br> ):::processor
    PRO8(resourcedetection<br>fa:fa-microchip<br>):::processor

    PROA(attributes<br>fa:fa-microchip<br>redact):::processor
    PROB(redaction<br>fa:fa-microchip<br>update):::processor
    EXP1(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload<br> ):::exporter
    EXP2(&emsp;&emsp;file&emsp;&emsp;<br>fa:fa-upload<br> ):::exporter
    EXP3(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload<br> ):::exporter
    EXP4(&emsp;&emsp;otlphttp&emsp;&emsp;<br>fa:fa-upload<br> ):::exporter
    EXP5(&emsp;&emsp;otlphttp&emsp;&emsp;<br>fa:fa-upload<br> ):::exporter
    ROUTE1(&nbsp;sum&nbsp;<br>fa:fa-route<br> ):::con-export
    ROUTE2(&nbsp;count&nbsp;<br>fa:fa-route<br> ):::con-receive
    ROUTE3(&nbsp;sum&nbsp;<br>fa:fa-route<br> ):::con-receive

    %% Links
    subID1:::sub-traces
    subID2:::sub-metrics
    subgraph " " 
      direction LR
      subgraph subID1[**Traces**]
      direction LR
      REC1 --> PRO1
      PRO1 --> PROA
      PROA --> PROB
      PROB --> PRO7
      PRO7 --> PRO3
      PRO3 --> PRO5 
      PRO5 --> EXP1
      PRO5 --> EXP2
      PRO5 --> EXP5
      PRO5 --> ROUTE1
      end
      
      subgraph subID2[**Metrics**]
      direction LR
      ROUTE1 --> ROUTE3
      ROUTE3 --> PRO2       
      ROUTE2 --> PRO2
      REC3 --> PRO2
      PRO2 --> PRO8
      PRO8 --> PRO4
      PRO4 --> PRO6
      PRO6 --> EXP3
      PRO6 --> EXP4
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-logs stroke:#34d399,stroke-width:1px, color:#34d399,stroke-dasharray: 3 3;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
classDef sub-metrics stroke:#38bdf8,stroke-width:1px, color:#38bdf8,stroke-dasharray: 3 3;
```

{{% /notice %}}
