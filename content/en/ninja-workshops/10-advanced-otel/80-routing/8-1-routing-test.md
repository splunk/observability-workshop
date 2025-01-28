---
title: Test our Routing Connector
linkTitle: 8.1 Testing Routing
weight: 1
---

## WORK IN PROGRESS

Step 1: Setting Up the Directory Structure
First, ensure you have the required directory structure for the checkpoint folder and log files:

```bash
your_project/
├── checkpoint-folder/           # Directory for checkpoint files
├── agent-standard.out           # Output file for standard traces
├── agent-security.out           # Output file for security traces
└── otel-collector-config.yaml   # OpenTelemetry Collector config file
```

 Also, configure a Filelog receiver to read log data from files, but this is currently commented out.

2.3 Exporters
There are multiple exporters configured:

Debug Exporter: Outputs trace data in detailed verbosity for debugging.
File Exporters: Writes trace data to files with rotation policies.
OTLP Gateway Exporter: Sends trace data to a remote OTLP endpoint with queuing and retry options.

2.4 Connectors: Routing

The routing connector routes traces based on attributes. Here, traces with the attribute `deployment.environment == "security_applications"` are routed to a separate pipeline, `traces/security`:

```yaml
connectors:
  routing:
    default_pipelines: [traces/standard]  # Default pipeline for traces
    error_mode: ignore                    # Ignore errors during routing
    table:
      - statement: route() where attributes["deployment.environment"] == "security_applications"
        pipelines: [traces/security]
```

You can add additional routing rules by specifying different attribute conditions. The second routing rule is commented out but could be used to delete a specific key from the attributes before routing the data.

2.5 Processors
Processors allow you to manipulate and enrich data before exporting it:

Batch Processor: Batches data to improve performance.
Memory Limiter: Ensures that the collector doesn’t consume too much memory.
Resource Detection: Adds system resource attributes to the traces.
Resource Mode: Adds custom attributes to traces.

```yaml
processors:
  batch:
    metadata_keys:
      - X-SF-Token   # Include metadata in batches
  memory_limiter:
    check_interval: 2s
    limit_mib: 512   # Limits memory usage to 512 MB
  resourcedetection:
    detectors: [system]
    override: true    # Overrides existing resource detection
  resource/add_mode:
    attributes:
      - action: insert
        value: "agent"
        key: otelcol.service.mode
```

2.6 Service Pipelines
The service section defines how the traces, logs, and metrics will flow through the system, from receivers to processors and exporters.

```yaml
service:
  extensions: [file_storage/checkpoint]
  pipelines:
    traces:
      receivers: [otlp]               # Receives traces via OTLP
      exporters: [routing, debug]      # Routes and debugs traces
    traces/standard:
      receivers: [routing]            # Receives routed traces
      processors:
        - memory_limiter
        - batch
        - resourcedetection
        - resource/add_mode
      exporters: [file/standard]       # Exports to standard file
    traces/security:
      receivers: [routing]            # Receives routed security traces
      processors:
        - memory_limiter
        - batch
        - resourcedetection
        - resource/add_mode
      exporters: [file/security]       # Exports to security file
    metrics:
      receivers: [otlp]
      processors:
        - memory_limiter
        - batch
        - resourcedetection
      exporters: [file/standard, debug]
    logs:
      receivers: [otlp]
      processors:
        - memory_limiter
        - batch
        - resourcedetection
      exporters: [file/standard, debug]
traces/standard: Default pipeline for traces that do not match the routing condition.
traces/security: Pipeline for security-related traces routed by the connector.
```

Step 3: Running OpenTelemetry Collector

Create the configuration file: Copy the YAML configuration into a file named otel-collector-config.yaml.

Start the OpenTelemetry Collector:

```bash
otelcol --config=otel-collector-config.yaml
```

Verify that the Collector is running: Check the logs for any errors. If there are no errors, traces should be flowing through the collector.

Step 4: Testing the Routing
To test the routing:

Generate or simulate trace data with the attribute `deployment.environment = security_applications`.
Verify that the traces are routed to the traces/security pipeline by checking the `agent-security.out` file.
You can also check `agent-standard.out` to ensure that other traces are routed to the standard pipeline.

Step 5: Checkpoint Management

The checkpoint extension ensures that data is reliably stored and managed. Check the checkpoint-folder directory for checkpoint files created during operation.
Compaction: Large transactions will be compacted into smaller chunks, which helps in managing large data volumes.

Conclusion
In this section, you've learned how to configure the OpenTelemetry Collector to route traces based on attributes. You’ve also explored checkpointing, batching, resource detection, and the export of trace data to different destinations. You can extend this setup by adding more routing rules, processing options, and exporters as needed for your use case.
