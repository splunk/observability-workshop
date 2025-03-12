---
title: 2. Gateway Configuration
linkTitle: 2. Gateway Setup
time: 10 minutes
weight: 2
---

The OpenTelemetry Gateway is designed to receive, process, and export telemetry data. It acts as an intermediary between telemetry sources (e.g. applications, services) and backends (e.g., observability platforms like Prometheus, Jaeger, or Splunk Observability Cloud).

The gateway is useful because it centralizes telemetry data collection, enabling features like data filtering, transformation, and routing to multiple destinations. It also reduces the load on individual services by offloading telemetry processing and ensures consistent data formats across distributed systems. This makes it easier to manage, scale, and analyze telemetry data in complex environments.

{{% notice title="Exercise" style="green" icon="running" %}}

- In the **Gateway terminal** window, change into the `[WORKSHOP]` directory and create a new subdirectory named `2-gateway`.

> [!IMPORTANT]
> **Change _ALL_ terminal windows to the `[WORKSHOP]/2-gateway` directory.**

- Next, copy `agent.yaml` from the `1-agent` directory into `2-gateway`.
- Create a file called `gateway.yaml` and add the following initial configuration:

```yaml { title="gateway.yaml" }
###########################         This section holds all the
## Configuration section ##         configurations that can be 
###########################         used in this OpenTelemetry Collector
extensions:                       # List of extensions
  health_check:                   # Health check extension
    endpoint: 0.0.0.0:14133       # Custom port to avoid conflicts

receivers:
  otlp:                           # OTLP receiver
    protocols:
      http:                       # HTTP protocol
        endpoint: "0.0.0.0:5318"  # Custom port to avoid conflicts
        include_metadata: true    # Required for token pass-through

exporters:                        # List of exporters
  debug:                          # Debug exporter
    verbosity: detailed           # Enable detailed debug output
  file/traces:                    # Exporter Type/Name
    path: "./gateway-traces.out"  # Path for OTLP JSON output
    append: false                 # Overwrite the file each time
  file/metrics:                   # Exporter Type/Name
    path: "./gateway-metrics.out" # Path for OTLP JSON output
    append: false                 # Overwrite the file each time
  file/logs:                      # Exporter Type/Name
    path: "./gateway-logs.out"    # Path for OTLP JSON output
    append: false                 # Overwrite the file each time

connectors:

processors:                       # List of processors
  memory_limiter:                 # Limits memory usage
    check_interval: 2s            # Memory check interval
    limit_mib: 512                # Memory limit in MiB
  batch:                          # Batches data before exporting
    metadata_keys:                # Groups data by token
    - X-SF-Token
  resource/add_mode:              # Adds metadata
    attributes:
    - action: upsert              # Inserts or updates a key
      key: otelcol.service.mode   # Key name
      value: "gateway"            # Key value

###########################
### Activation Section  ###
###########################
service:                          # Service configuration
  telemetry:
    metrics:
      level: none                 # Disable metrics
  extensions: [health_check]      # Enabled extensions
  pipelines:                      # Configured pipelines
    traces:                       # Traces pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors:                 # Processors for traces
      - memory_limiter
      - resource/add_mode
      - batch
      exporters:
      - debug                     # Debug exporter
      - file/traces
    metrics:                      # Metrics pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors:                 # Processors for metrics
      - memory_limiter
      - resource/add_mode
      - batch
      exporters:
      - debug                     # Debug exporter
      - file/metrics
    logs:                         # Logs pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors:                 # Processors for logs
      - memory_limiter
      - resource/add_mode
      - batch
      exporters:
      - debug                     # Debug exporter
      - file/logs
```

```text { title="Updated Directory Structure" }
[WORKSHOP]
└── 2-gateway
    └── agent.yaml
    └── gateway.yaml
```

{{% /notice %}}
