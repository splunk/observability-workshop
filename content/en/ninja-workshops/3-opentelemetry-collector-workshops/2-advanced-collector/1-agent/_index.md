---
title: 1. Agent Configuration
linkTitle: 1. Agent Setup
time: 10 minutes
weight: 1
---

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
During this workshop, you will be using up to four terminal windows simultaneously. To stay organized, consider customizing each terminal or shell with unique names and colors. This will help you quickly identify and switch between them as needed.

We will refer to these terminals as: **Agent**, **Gateway**, **Spans** and **Logs**.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

1. In the **Agent terminal** window, change into the `[WORKSHOP]` directory and create a new subdirectory named `1-agent`.

    ```bash
    mkdir 1-agent && \
    cd 1-agent
    ```

2. Create a file named `agent.yaml`. This file will define the basic structure of an OpenTelemetry Collector configuration.

3. Copy and paste the following initial configuration into `agent.yaml`:

    ```yaml
    # Extensions
    extensions:
      health_check:                        # Health Check Extension
        endpoint: 0.0.0.0:13133            # Health Check Endpoint

    # Receivers Pipeline
    receivers:
      hostmetrics:                         # Host Metrics Receiver
        collection_interval: 3600s         # Collection Interval (1hr)
        scrapers:
          cpu:                             # CPU Scraper
      otlp:                                # OTLP Receiver
        protocols:
          http:                            # Configure HTTP protocol
            endpoint: "0.0.0.0:4318"       # Endpoint to bind to

    # Exporters Pipeline
    exporters:
      debug:                               # Debug Exporter
        verbosity: detailed                # Detailed verbosity level

    # Processors Pipeline
    processors:
      memory_limiter:                      # Limits memory usage by Collectors pipeline
        check_interval: 2s                 # Check interval
        limit_mib: 512                     # Memory limit in MiB
      resourcedetection:                   # Resource Detection Processor
        detectors: [system]                # Detect system resources
        override: true                     # Overwrites existing attributes
      resource/add_mode:                   # Resource Processor
        attributes:
        - action: insert                   # Action to perform
          key: otelcol.service.mode        # Key name
          value: "agent"                   # Key value

    # Connectors Pipeline

    # Service Section - Enabled Pipelines
    service:
      extensions:
      - health_check                       # Health Check Extension
      pipelines:
        traces:
          receivers:
          - otlp                           # OTLP Receiver
          processors:
          - memory_limiter                 # Memory Limiter processor
          - resourcedetection              # Add system attributes to the data
          - resource/add_mode              # Add collector mode metadata
          exporters:
          - debug                          # Debug Exporter
        metrics:
          receivers:
          - otlp
          processors:
          - memory_limiter
          - resourcedetection
          - resource/add_mode
          exporters:
          - debug
        logs:
          receivers:
          - otlp
          processors:
          - memory_limiter
          - resourcedetection
          - resource/add_mode
          exporters:
          - debug
    ```

4. Your directory structure should now look like this:

    ```text
    [WORKSHOP]
    └── 1-agent
       └── agent.yaml  # OpenTelemetry Collector configuration file
    ```

{{% /notice %}}
