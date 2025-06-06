---
title: 1. Agent & Gateway Configuration
linkTitle: 1. Agent/Gateway Setup
time: 10 minutes
weight: 3
---

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
During this workshop, you will be using multiple terminal windows simultaneously. To stay organized, consider customizing each terminal or shell with unique names and colors. This will help you quickly identify and switch between them as needed.

We will refer to these terminals as: **Agent**, **Gateway**, **Spans**, **Logs** and **Tests**.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

1. Open or create your first terminal window and name it  **Agent terminal**. In the Terminal, change into the `[WORKSHOP]/1-agent-gateway` folder and check if the initial workshop files are present. 

    ```bash
    cd 1-agent-gateway
    ls -l
    ```

3. You should have the following files in your folder:

```text { title="Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

3. Check the content of the  `agent.yaml`. This file defines the basic structure of an OpenTelemetry Collector configuration.

4. Copy and paste the following initial configuration into `agent.yaml`:

    ```yaml
    # Extensions
    extensions:
      health_check:                        # Health Check Extension
        endpoint: 0.0.0.0:13133            # Health Check Endpoint

    # Receivers
    receivers:
      hostmetrics:                         # Host Metrics Receiver
        collection_interval: 3600s         # Collection Interval (1hr)
        scrapers:
          cpu:                             # CPU Scraper
      otlp:                                # OTLP Receiver
        protocols:
          http:                            # Configure HTTP protocol
            endpoint: "0.0.0.0:4318"       # Endpoint to bind to

    # Exporters
    exporters:
      debug:                               # Debug Exporter
        verbosity: detailed                # Detailed verbosity level

    # Processors
    processors:
      memory_limiter:                      # Limits memory usage
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

    # Connectors
    #connectors:                           # leave this commented out; we will uncomment in an upcoming exercise

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
    .
 
```text { title="Directory Structure" }
.
├── agent.yaml
├── gateway.yaml
└── quotes.yaml
```

{{% /notice %}}
