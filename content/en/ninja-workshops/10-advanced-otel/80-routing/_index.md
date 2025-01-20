---
title: Routing
linkTitle: 8. Routing
time: 10 minutes
weight: 8
---

The routing processor allows you to route data to different destinations based on the attributes of the data. The routing processor can be used to send data to different backends based on the attributes of the data. For example, you can use the routing processor to send data to different backends based on the service name or the environment.

![Routing Processor](../images/routing.png)

Directory structure testing:

```text
your_project/
├── checkpoint-folder/
├── otel-collector-config.yaml  # Configuration file
├── agent-standard.out         # Trace export file
├── agent-security.out         # Security trace export file
```

In this workshop, you'll configure the routing connector in OpenTelemetry to route traces based on specific attributes, enabling you to handle traces differently based on their contents. You will also learn how to manage data checkpointing, apply various processors, and configure multiple exporters. By the end of this workshop, you will have a complete OpenTelemetry Collector configuration that processes and routes trace data efficiently.

## Overview of the Configuration

In this workshop, we’ll be using the following key components defined in the YAML configuration:

Extensions: File storage for checkpointing.
Receivers: Collecting trace data using the OTLP protocol.
Exporters: Exporting data to different locations including files and a remote OTLP endpoint.
Connectors: Routing traces based on attributes.
Processors: Enhancing data with resource detection, batching, and memory limiting.
Service Pipelines: Defining data flow for traces, metrics, and logs.
Let's dive into each section of the YAML configuration and learn how to use it.

Step 1: Setting Up the Directory Structure
First, ensure you have the required directory structure for the checkpoint folder and log files:

```bash
your_project/
├── checkpoint-folder/           # Directory for checkpoint files
├── agent-standard.out           # Output file for standard traces
├── agent-security.out           # Output file for security traces
└── otel-collector-config.yaml   # OpenTelemetry Collector config file
```

Step 2: Understanding the Key Configuration Sections

2.1 Extensions
The file_storage/checkpoint extension is used to manage checkpoint data. This ensures that data is written reliably, even in the case of failures or restarts.

```yaml
extensions:
  file_storage/checkpoint:
    directory: ./checkpoint-folder  # Where checkpoint data is stored
    create_directory: true          # Create the directory if it doesn’t exist
    timeout: 1s                     # Timeout for checkpoint operations
    compaction:
      on_start: true                # Enable compaction at start
      directory: ./checkpoint-folder  # Where to store compacted data
      max_transaction_size: 65_536  # Max size for each transaction
```

Compaction: Helps in managing large files and keeping data manageable by breaking large transactions into smaller chunks.

2.2 Receivers
The otlp receiver is used to accept incoming traces over HTTP. By default, the endpoint is configured to listen on 0.0.0.0:4318.

```yaml
Copy
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:4318"   # Receives OTLP traces over HTTP
```

You can also configure a filelog receiver to read log data from files, but this is currently commented out.

2.3 Exporters
There are multiple exporters configured:

Debug Exporter: Outputs trace data in detailed verbosity for debugging.
File Exporters: Writes trace data to files with rotation policies.
OTLP Gateway Exporter: Sends trace data to a remote OTLP endpoint with queuing and retry options.

```yaml
exporters:
  debug:
    verbosity: detailed   # Enables detailed debug logs
  file/standard:
    path: ./agent-standard.out
    rotation:
      max_megabytes: 2    # Maximum file size before rotation
      max_backups: 2      # Max number of backup files
  file/security:
    path: ./agent-security.out
    rotation:
      max_megabytes: 2
      max_backups: 2
  otlp/gateway:
    endpoint: "localhost:5317"
    tls:
      insecure: true      # Allows insecure TLS connections (not recommended for production)
    retry_on_failure:
      enabled: true       # Enables retries on failure
    sending_queue:
      enabled: true
      num_consumers: 10   # Number of consumers
      queue_size: 10000   # Size of the sending queue
      storage: file_storage/checkpoint
    timeout: 5s
    headers:
      X-SF-Token: "123456"  # Custom header for authentication
```

2.4 Connectors: Routing

The routing connector routes traces based on attributes. Here, traces with the attribute deployment.environment == "security_applications" are routed to a separate pipeline, traces/security.

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

Generate or simulate trace data with the attribute deployment.environment = security_applications.
Verify that the traces are routed to the traces/security pipeline by checking the agent-security.out file.
You can also check agent-standard.out to ensure that other traces are routed to the standard pipeline.

Step 5: Checkpoint Management

The checkpoint extension ensures that data is reliably stored and managed. Check the checkpoint-folder directory for checkpoint files created during operation.
Compaction: Large transactions will be compacted into smaller chunks, which helps in managing large data volumes.

Conclusion
In this workshop, you've learned how to configure the OpenTelemetry Collector to route traces based on attributes. You’ve also explored checkpointing, batching, resource detection, and the export of trace data to different destinations. You can extend this setup by adding more routing rules, processing options, and exporters as needed for your use case.
