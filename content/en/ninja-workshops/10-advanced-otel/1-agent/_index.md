---
title: 1. Agent Configuration
linkTitle: 1. Agent Setup
time: 10 minutes
weight: 1
---

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
During this workshop, you will be using up to four terminal windows simultaneously. To stay organized, consider customizing each terminal or shell with unique names and colors. This will help you quickly identify and switch between them as needed.

We will refer to these terminals as: **Agent**, **Gateway**, **Tests** and **Log-gen**.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}
In your `[WORKSHOP]` directory, create a subdirectory called `1-agent` and change into that directory.

```text
cd [WORKSHOP]
mkdir 1-agent
cd 1-agent
```

In the `1-agent` directory, create a file named `agent.yaml`. This file will define the basic structure of an OpenTelemetry Collector configuration.

Copy and paste the following initial configuration into `agent.yaml`:

```yaml { title="agent.yaml" }
###########################        This section holds all the
## Configuration section ##        configurations that can be 
###########################        used in this OpenTelemetry Collector
extensions:                       # Array of Extensions
  health_check:                   # Configures the health check extension
    endpoint: 0.0.0.0:13133       # Endpoint to collect health check data

receivers:                        # Array of Receivers
  hostmetrics:                    # Receiver Type
    collection_interval: 3600s    # Scrape metrics every hour
    scrapers:                     # Array of hostmetric scrapers
      cpu:                        # Scraper for cpu metrics
  otlp:                           # Receiver Type
    protocols:                    # List of Protocols used 
      http:                       # HTTP Protocol
        endpoint: "0.0.0.0:4318"  # Endpoint for incoming telemetry data

exporters:                        # Array of Exporters
  debug:                          # Exporter Type
    verbosity: detailed           # Enabled detailed debug output

processors:                       # Array of Processors
  memory_limiter:                 # Limits memory usage by Collectors pipeline
    check_interval: 2s            # Interval to check memory usage
    limit_mib: 512                # Memory limit in MiB
  resourcedetection:              # Processor Type
    detectors: [system]           # Detect system resource information
    override: true                # Overwrites existing attributes
  resource/add_mode:              # Processor Type/Name
    attributes:                   # Array of attributes and modifications
    - action: insert              # Action is to insert a key
      key: otelcol.service.mode   # Key name
      value: "agent"              # Key value

###########################         This section controls what
### Activation Section  ###         configurations will be used
###########################         by this OpenTelemetry Collector
service:                          # Services configured for this Collector
  extensions:                     # Enabled extensions
  - health_check
  pipelines:                      # Array of configured pipelines
    traces:
      receivers:
      - otlp                      # OTLP Receiver
      processors:
      - memory_limiter            # Memory Limiter processor
      exporters:
      - debug                     # Debug Exporter
    metrics:
      receivers:
      - otlp                      # OTLP Receiver
      processors:
      - memory_limiter            # Memory Limiter processor
      exporters:
      - debug                     # Debug Exporter
    logs:
      receivers:
      - otlp                      # OTLP Receiver
      processors:
      - memory_limiter            # Memory Limiter processor
      exporters:
      - debug                     # Debug Exporter
```

```text { title="Updated Directory Structure" }
[WORKSHOP]
├── 1-agent         # Module directory
│   └── agent.yaml  # OpenTelemetry Collector configuration file
└── otelcol         # OpenTelemetry Collector binary
```

{{% /notice %}}
