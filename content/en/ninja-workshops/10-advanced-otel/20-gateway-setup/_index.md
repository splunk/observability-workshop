---
title: Route data though a gateway  
linkTitle: 2. Gateway Setup
time: 10 minutes
weight: 2
---

### Gateway Setup

On your machine, navigate to the directory where you're running the workshop. Create a new subdirectory called `2-gateway`, then copy the latest versions of `agent.yaml` and `trace.json` from `1-agent` into this new directory.

Next, move into the `[WORKSHOP]/2-gateway` directory and create a file named `gateway.yaml`. Copy the following starting configuration into this file.

```yaml
###########################  This section holds all the
## Configuration section ##  configurations that can be 
###########################  used in this OpenTelemetry Collector
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:5318"  # Port changed to prevent conflict with agent
        include_metadata: true    # Needed for token pass through mode

processors:
  memory_limiter:
    check_interval: 2s
    limit_mib: 512
  batch:
    metadata_keys:                # Include token in batches
    - X-SF-Token                  # Batch data grouped by Token
  resource/add_mode:              # Processor Type/Name
    attributes:                   # Array of Attributes and modifications 
    - action: upsert              # Action taken is to `insert' or 'update' a key 
      key: otelcol.service.mode   # key Name
      value: "gateway"            # Key Value

exporters:
  debug:
    verbosity: detailed

###########################  This section controls what
### Activation Section  ###  configuration  will be used  
###########################  by the OpenTelemetry Collector
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter]
      exporters: [ debug]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter]
      exporters: [ debug]
    logs:
      receivers: [otlp]
      processors: [memory_limiter]
      exporters: [ debug]
```

{{% tab title="Updated Directory Structure" %}}

```text
[WORKSHOP]
├── 1-agent             # Module directory
├── 2-gateway           # Module directory
│   └── agent.yaml      # OpenTelemetry Collector configuration file
│   └── gateway.yaml    # OpenTelemetry Collector configuration file
│   └── trace.json      # Sample trace data
└── otelcol             # OpenTelemetry Collector binary
```

{{% /tab %}}

The [**batch processor**](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md) groups spans, metrics, or logs into batches, improving compression and reducing outgoing connections. It supports batching based on size and time.

It’s recommended to use the batch processor in every collector, placing it after the `memory_limiter` and sampling processors to ensure batching occurs after any data drops like sampling.

Let's extend the `gateway.yaml` file we just created to seperate data to different files  

{{% notice title="Exercise" style="green" icon="running" %}}

- **Configure File Exporters**: Separate exporters need to be configured for traces, metrics, and logs. Below is the YAML configuration for traces:

  ```yaml
    file/traces:                       # Exporter Type/Name
      path: "./gateway-traces.out"     # Path where trace data will be saved in OTLP json format
      append: false                    # Overwrite the file each time
  ```

- **Create similar exporters for metrics and logs**: Using the above example, set the exporter names appropriately and update the file paths to `./gateway-metrics.out` for metrics and `./gateway-logs.out` for logs.
- **Update the Pipelines Section**: Add each newly created exporter to its corresponding pipeline in the service configuration. Also, add the `batch` processor to each pipeline.

  ```yaml
      traces:                                # Trace Pipeline
        receivers: [otlp]                    # Array of Trace Receivers 
        processors: [memory_limiter, batch]  # Array of Processors
        exporters: [file/traces, debug]      # Array of Trace Exporters
      # Metric pipeline
      # Logs Pipeline  
  ```

{{% /notice %}}

Verify the `gateway.yaml` file at **[otelbin.io](https://www.otelbin.io/)**. If configured correctly, your sections should resemble the following example for logs:

![otelbin-logs](../images/gateway-2-1-logs.png?width=50vw)
