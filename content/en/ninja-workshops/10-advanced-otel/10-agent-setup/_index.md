---
title: Initial setup our agent config  
linkTitle: 1. Initial Agent Setup
time: 10 minutes
weight: 1
---

### Setup

In your `[WORKSHOP]` directory, create a subdirectory named 1-agent and navigate into it.

```text
mkdir -p [WORKSHOP]/1-agent
cd [WORKSHOP]/1-agent
```

Inside the `1-agent` directory, we will create a file containing the basic structure of an OpenTelemetry Collector configuration, defining the components you'll need to work with.

To do this, create a file called `agent.yaml` and paste the following starting configuration into it:

```yaml
receivers:

exporters:
    
processors:
  memory_limiter:
    check_interval: 2s
    limit_mib: 512
  
service:
  pipelines:

    traces:
      receivers: []
      processors: 
      -                                # You also could use []
      exporters: []

    metrics:
      receivers: []
      processors:                      # You also could use [] 
      -
      exporters: []

    logs: 
      receivers: []
      processors:                      # You also could use [] 
      - 
      exporters: []
```

{{% tab title="Initial Directory Structure" %}}

```text
[WORKSHOP]
├── 1-agent         # Module directory
│   └── agent.yaml  # OpenTelemetry Collector configuration file
└── otelcol         # OpenTelemetry Collector binary
```

{{%/tab%}}

{{% notice title="Exercise" style="green" icon="running" %}}
Let's walk through a few modifications to get things started.

For proper formatting, make sure to align the YAML structure, paying attention to indentation.

- **Add** an `otlp` **receiver**: Configure to use `http` as its `protocol`.

  ```yaml
  receivers:
    otlp:
      protocols:                    # list of Protocols used 
        http:                       # This wil enable the HTTP Protocol
          endpoint: "0.0.0.0:4318"  # The agent will listen for incoming telemetry data on this endpoint.
  ```

- **Add a `debug` exporter**:

  ```yaml
  exporters:
    debug:                         # Shows collected data in a human-readable format on the console.
      verbosity: detailed          # Set the detailed level for the output
  ```

- **Update Pipelines**: Ensure that the `otlp` receiver, `memory_limiter` processor, and `debug` exporter are added to the pipelines for traces, metrics, and logs.

  ```yaml
  service:
    pipelines:
      traces:                       # Traces Pipeline
        receivers: [otlp]           # Array of receivers in this pipeline
        processors:                 # Array of Processors in this pipeline            
        - memory_limiter            # You also could use [memory_limiter]
        exporter: [debug]           # Array of Exporters in this pipeline            

      # metrics: pipeline section.. .  
  ```



{{% /notice %}}

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
In the exercise above, we’ve provided all the key elements in YAML format, but it’s up to you to correct and complete them. Be mindful of the formatting, as the OpenTelemetry Collector configuration is YAML-based.

Going forward, we will build upon these changes and apply what you've learned.

If you’re ever unsure about the YAML format used, you can refer to otelbin.io, which will display the default agent configuration when first accessed.
{{% /notice %}}

By using [**otelbin.io**](https://otelbin.io) to validate your `agent.yaml` file, you can quickly identify spelling or configuration errors. If everything is set up correctly, your configuration for all pipelines should look like this (click the image to enlarge):

<!--![otelbin-a-1-1-all](../images/agent-1-1-all.png)-->
![agent-traces](../images/agent-traces.png?classes=inline&width=20vw)
![agent-metrics](../images/agent-metrics.png?classes=inline&width=20vw)
![agent-logs](../images/agent-logs.png?classes=inline&width=20vw)

Let's test our config.
