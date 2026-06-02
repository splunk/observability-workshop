---
title: 1. Agent Configuration
linkTitle: 1. Agent Setup
time: 10 minutes
weight: 3
---

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
このワークショップでは、最大 5 つのターミナルウィンドウを同時に使用します。整理しやすくするため、各ターミナルやシェルにそれぞれ固有の名前と色を設定することをお勧めします。これにより、必要に応じて素早く識別し、切り替えることができます。

これらのターミナルは、**Agent**、**Gateway**、**Spans**、**Logs**、**Tests** と呼びます。
{{% /notice %}}

{{% notice title="演習" style="green" icon="running" %}}

1. **Agent ターミナル**ウィンドウで `[WORKSHOP]` ディレクトリに移動し、`1-agent` という名前の新しいサブディレクトリを作成します。

    ```bash
    mkdir 1-agent && \
    cd 1-agent
    ```

2. `agent.yaml` という名前のファイルを作成します。このファイルでは、OpenTelemetry Collector 設定の基本構造を定義します。

3. 以下の初期設定をコピーして `agent.yaml` に貼り付けます。

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

4. ディレクトリ構造は次のようになっているはずです。

    ```text
    .
    └── agent.yaml  # OpenTelemetry Collector configuration file
    ```

{{% /notice %}}
