---
title: 1.1 Verify Gateway Configuration
linkTitle: 1.1 Gateway Configuration
weight: 1
---

The **OpenTelemetry Gateway** serves as a central hub for receiving, processing, and exporting telemetry data. It sits between your telemetry sources (such as applications and services) and your observability backends like Splunk Observability Cloud.

By centralizing telemetry traffic, the gateway enables advanced features such as data filtering, enrichment, transformation, and routing to one or more destinations. It helps reduce the burden on individual services by offloading telemetry processing and ensures consistent, standardized data across distributed systems.

This makes your observability pipeline easier to manage, scale, and analyze—especially in complex, multi-service environments.

{{% notice title="Exercise" style="green" icon="running" %}}

Open or create your second terminal window and name it **Gateway**. Navigate to the first exercise directory `[WORKSHOP]/1-agent-gateway`
then check the contents of the `gateway.yaml` file.

This file outlines the core structure of the OpenTelemetry Collector as deployed in **Gateway** mode.

<!--
```bash
 cat ./gateway.yaml
```

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

# Connectors
#connectors:                      # leave this commented out; we will uncomment in an upcoming exercise

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
-->
{{% /notice %}}

### Understanding the Gateway Configuration

Let’s explore the `gateway.yaml` file that defines how the OpenTelemetry Collector is configured in **Gateway** mode during this workshop. This **Gateway** is responsible for receiving telemetry from the **Agent**, then processing and exporting it for inspection or forwarding.

* **OTLP Receiver (Custom Port)**

  ```yaml
  receivers:
    otlp:
      protocols:
        http:
          endpoint: "0.0.0.0:5318"
  ```

  The port `5318` matches the `otlphttp` exporter in the **Agent** configuration, ensuring that all telemetry data sent by the **Agent** is accepted by the **Gateway**.

> [!NOTE]
> This separation of ports avoids conflicts and keeps responsibilities clear between agent and gateway roles.

* **File Exporters**

  The **Gateway** uses three file exporters to output telemetry data to local files. These exporters are defined as:

  ```yaml
  exporters:                        # List of exporters
    debug:                          # Debug exporter
      verbosity: detailed           # Enable detailed debug output
    file/traces:                    # Exporter Type/Name
      path: "./gateway-traces.out"  # Path for OTLP JSON output for traces
      append: false                 # Overwrite the file each time
    file/metrics:                   # Exporter Type/Name
      path: "./gateway-metrics.out" # Path for OTLP JSON output for metrics
      append: false                 # Overwrite the file each time
    file/logs:                      # Exporter Type/Name
      path: "./gateway-logs.out"    # Path for OTLP JSON output for logs
      append: false                 # Overwrite the file each time
  ```

  Each exporter writes a specific signal type to its corresponding file.

  These files are created once the gateway is started and will be populated with real telemetry as the agent sends data. You can monitor these files in real time to observe the flow of telemetry through your pipeline.
