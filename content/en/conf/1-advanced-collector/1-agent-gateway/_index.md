---
title: 1. Agent Configuration
linkTitle: 1. Agent/Gateway Config


time: 10 minutes
weight: 3
---
Welcome! In this section, we’ll begin with a fully functional OpenTelemetry setup that includes both an Agent and a Gateway.

We’ll start by quickly reviewing their configuration files to get familiar with the overall structure and to highlight key sections that control the telemetry pipeline.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Throughout the workshop, you’ll work with multiple terminal windows. To keep things organized, give each terminal a unique name or color. This will help you easily recognize and switch between them during the exercises.

We will refer to these terminals as: **Agent**, **Gateway**, **Spans**, **Logs**, and **Tests**.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

1. Open or create your first terminal window and name it **Agent**.
Then, navigate to the directory for the first exercise `[WORKSHOP]/1-agent-gateway` and verify that the required files are generated:

    ```bash
    cd 1-agent-gateway
    ls -l
    ```
  
2. You should see the following files in the directory.
If not, re-run the `setup-workshop.sh` script as described in the **Pre-requisites** section:

    ```text { title="Directory Structure" }
    .
    ├── agent.yaml
    └── gateway.yaml
    ```

3. Next, check the contents of the **agent.yaml** file.
This file outlines the core structure of the OpenTelemetry Collector as deployed in agent mode:

    ```bash
        cat ./agent.yaml
    ```

You should see a pre-configured setup tailored for this workshop.:

```yaml
###########################            This section holds all the
## Configuration section ##            configurations that can be 
###########################            used in this OpenTelemetry Collector
extensions:                            # Array of Extensions
  health_check:                        # Configures the health check extension
    endpoint: 0.0.0.0:13133            # Endpoint to collect health check data

receivers:                             # Array of Receivers
  hostmetrics:                         # Receiver Type
    collection_interval: 3600s         # Scrape metrics every hour
    scrapers:                          # Array of hostmetric scrapers
      cpu:                             # Scraper for cpu metrics
  otlp:                                # Receiver Type
    protocols:                         # list of Protocols used 
      http:                            # This wil enable the HTTP Protocol
        endpoint: "0.0.0.0:4318"       # Endpoint for incoming telemetry data 
  filelog/quotes:                      # Receiver Type/Name
    include: ./quotes.log              # The file to read log data from
    include_file_path: true            # Include file path in the log data
    include_file_name: false           # Exclude file name from the log data
    resource:                          # Add custom resource attributes
      com.splunk.source: ./quotes.log  # Source of the log data
      com.splunk.sourcetype: quotes    # Source type of the log data

exporters:                             # Array of Exporters
  debug:                               # Exporter Type
    verbosity: detailed                # Enabled detailed debug output
  otlphttp:                            # Exporter Type
    endpoint: "http://localhost:5318"  # Gateway OTLP endpoint  
  file:                                # Exporter Type
    path: "./agent.out"                # Save path (OTLP JSON)
    append: false                      # Overwrite the file each time
processors:                            # Array of Processors
  memory_limiter:                      # Limits memory usage by Collectors pipeline
    check_interval: 2s                 # Interval to check memory usage
    limit_mib: 512                     # Memory limit in MiB
  resourcedetection:                   # Processor Type
    detectors: [system]                # Detect system resource information
    override: true                     # Overwrites existing attributes
  resource/add_mode:                   # Processor Type/Name
    attributes:                        # Array of attributes and modifications
    - action: insert                   # Action is to insert a key
      key: otelcol.service.mode        # Key name
      value: "agent"                   # Key value

###########################            This section controls what
### Activation Section  ###            configurations will be used
###########################            by this OpenTelemetry Collector
service:                               # Services configured for this Collector
  extensions:                          # Enabled extensions
  - health_check
  pipelines:                           # Array of configured pipelines
    traces:
      receivers:
      - otlp
      processors:
      - memory_limiter                 # Memory Limiter processor
      - resourcedetection              # Adds system attributes to the data
      - resource/add_mode              # Adds collector mode metadata
      exporters:
      - debug
      - file
      - otlphttp
    metrics:
      receivers:
      - hostmetrics                    # Hostmetric reciever (cpu only)
      - otlp
      processors:
      - memory_limiter                 # Memory Limiter processor
      - resourcedetection              # Adds system attributes to the data
      - resource/add_mode              # Adds collector mode metadata
      exporters:
      - debug
      - file
      - otlphttp
    logs:
      receivers:
      - otlp
      - filelog/quotes                 # Filelog Receiver
      processors:
      - memory_limiter                 # Memory Limiter processor
      - resourcedetection              # Adds system attributes to the data
      - resource/add_mode              # Adds collector mode metadata
      exporters:
      - debug
      - file
      - otlphttp
```

{{% /notice %}}

### Understanding the Agent Configuration

Let’s review the key components of the agent.yaml file used in this workshop. We’ve made some important additions to support traces, metrics, and logs.

#### Receivers

The `receivers` section defines how the agent ingests telemetry data. In this setup, we’ve enabled three types of receivers:

* **Host Metrics Receiver**

  ```yaml
  hostmetrics:                         # Host Metrics Receiver
    collection_interval: 3600s         # Collection Interval (1hr)
    scrapers:
      cpu:                             # CPU Scraper
  ```

  Collects CPU usage from the local system every hour. We’ll use this to generate example metric data.

* **OTLP Receiver (HTTP protocol)**

  ```yaml
  otlp:                                # OTLP Receiver
    protocols:
      http:                            # Configure HTTP protocol
        endpoint: "0.0.0.0:4318"       # Endpoint to bind to
  ```

This enables the agent to receive spans, metrics, and logs over HTTP on port 4318.  We use this to send data to the collector in our exercises.

* **FileLog Receiver**

  ```yaml
  filelog/quotes:                      # Receiver Type/Name
    include: ./quotes.log              # The file to read log data from
    include_file_path: true            # Include file path in the log data
    include_file_name: false           # Exclude file name from the log data
    resource:                          # Add custom resource attributes
      com.splunk.source: ./quotes.log  # Source of the log data
      com.splunk.sourcetype: quotes    # Source type of the log data
  ```

This allows the agent to tail a local log file (`quotes.log`) and convert it to structured log events, enriched with metadata such as `source` and `sourceType`.

#### Exporters

* The `exporters` section controls where the collected telemetry data is sent:

  ```yaml
  exporters:                             # Array of Exporters
    debug:                               # Exporter Type
      verbosity: detailed                # Enabled detailed debug output
    otlphttp:                            # Exporter Type
      endpoint: "http://localhost:5318"  # Gateway OTLP endpoint  
  ```

  The **debug:** exporter prints data to the console for visibility and debugging during the workshop while the **otlphttp:** exporter forwards all telemetry to a local Gateway instance.

{{% notice title="Info" style="info" %}}
This dual-export strategy ensures you can see the raw data locally while also sending it downstream for further processing and export.
{{% /notice %}}
