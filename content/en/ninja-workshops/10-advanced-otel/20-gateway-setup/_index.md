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
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:5318" # Port changed to prevent conflict with agent
        include_metadata: true # Enable token pass through mode

processors:
  memory_limiter:
    check_interval: 2s
    limit_mib: 512
  batch:
    X-SF-Token: # Include metadata in batches

exporters:
  debug:
    verbosity: detailed

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

{{% notice title="Exercise" style="green" icon="running" %}}

- **Configure File Exporters**: Separate exporters need to be configured for traces, metrics, and logs. Below is the YAML configuration for traces:

  ```yaml
  exporters:
    file/traces:                    # Exporter Type/Name
      path: "./gateway-traces.out"  # Path where trace data will be saved
      rotation:                     # Rotation settings for trace file
        max_megabytes: 2            # Maximum file size in MB before rotation
        max_backups: 2              # Maximum number of backups to keep
  ```

- **Create similar exporters for metrics and logs**: Using the above example, set the exporter names appropriately and update the file paths to `./gateway-metrics.out` for metrics and `./gateway-logs.out` for logs.
- **Update the Pipelines Section**: Add each newly created exporter to its corresponding pipeline in the service configuration.

  ```yaml
  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter]
        exporters: [file/traces, debug]
  ```

{{% /notice %}}

Verify the `gateway.yaml` file at **[otelbin.io](https://www.otelbin.io/)**. If configured correctly, your sections should resemble the following example for logs:

![otelbin-logs](../images/gateway-2-1-logs.png?width=50vw)
