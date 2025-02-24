---
title: 2. Gateway Configuration
linkTitle: 2. Gateway Setup
time: 10 minutes
weight: 2
---

The OpenTelemetry Gateway is designed to receive, process, and export telemetry data. It acts as an intermediary between telemetry sources (e.g. applications, services) and backends (e.g., observability platforms like Prometheus, Jaeger, or Splunk Observability Cloud).

The gateway is useful because it centralizes telemetry data collection, enabling features like data filtering, transformation, and routing to multiple destinations. It also reduces the load on individual services by offloading telemetry processing and ensures consistent data formats across distributed systems. This makes it easier to manage, scale, and analyze telemetry data in complex environments.

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `2-gateway`.
- Next, copy all contents from the `1-agent` directory into `2-gateway`.
- After copying, remove `agent.out`.
- Create a file called `gateway.yaml` and add the following initial configuration:
- Change **all** terminal windows to the `[WORKSHOP]/2-gateway` directory.

{{% tabs %}}
{{% tab title="gateway.yaml" %}}

```yaml
###########################         This section holds all the
## Configuration section ##         configurations that can be 
###########################         used in this OpenTelemetry Collector
extensions:                       # Array of Extensions
  health_check:                   # Configures the health check extension
    endpoint: 0.0.0.0:14133       # Port changed to prevent conflict with agent!!!

receivers:
  otlp:                           # Receiver Type
    protocols:                    # list of Protocols used
      http:                       # This wil enable the HTTP Protocol
        endpoint: "0.0.0.0:5318"  # Port changed to prevent conflict with agent!!!
        include_metadata: true    # Needed for token pass through mode

exporters:                        # Array of Exporters
  debug:                          # Exporter Type
    verbosity: detailed           # Enabled detailed debug output

processors:                       # Array of Processors
  memory_limiter:                 # Limits memory usage by Collectors pipeline
    check_interval: 2s            # Interval to check memory usage
    limit_mib: 512                # Memory limit in MiB
  batch:                          # Processor to Batch data before sending
    metadata_keys:                # Include token in batches
    - X-SF-Token                  # Batch data grouped by Token
  resource/add_mode:              # Processor Type/Name
    attributes:                   # Array of Attributes and modifications
    - action: upsert              # Action taken is to `insert' or 'update' a key
      key: otelcol.service.mode   # key Name
      value: "gateway"            # Key Value

###########################         This section controls what
### Activation Section  ###         configuration  will be used
###########################         by the OpenTelemetry Collector
service:                          # Services configured for this Collector
  extensions: [health_check]      # Enabled extensions for this collector
  pipelines:                      # Array of configured pipelines
    traces:
      receivers:
      - otlp                      # OTLP Receiver
      processors:
      - memory_limiter            # Memory Limiter processor
      - resource/add_mode         # Add metadata about collector mode
      - batch                     # Batch Processor, groups data before send                     
      exporters:
      - debug                     # Debug Exporter
    metrics:
      receivers:
      - otlp                      # OTLP Receiver
      processors:
      - memory_limiter            # Memory Limiter processor
      - resource/add_mode         # Add metadata about collector mode
      - batch                     # Batch Processor, groups data before send                     
      exporters:
      - debug                     # Debug Exporter
    logs:
      receivers:
      - otlp                      # OTLP Receiver
      processors:
      - memory_limiter            # Memory Limiter processor
      - resource/add_mode         # Add metadata about collector mode
      - batch                     # Batch Processor, groups data before send
      exporters:
      - debug                     # Debug Exporter
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}

```text { title="Updated Directory Structure" }
[WORKSHOP]
├── 1-agent             # Module directory
├── 2-gateway           # Module directory
│   └── agent.yaml      # OpenTelemetry Collector configuration file
│   └── gateway.yaml    # OpenTelemetry Collector configuration file
│   └── trace.json      # Sample trace data
└── otelcol             # OpenTelemetry Collector binary
```
