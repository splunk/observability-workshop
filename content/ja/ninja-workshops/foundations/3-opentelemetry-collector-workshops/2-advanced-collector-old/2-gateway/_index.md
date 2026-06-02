---
title: 2. Gateway の構成
linkTitle: 2. Gateway のセットアップ
time: 10 minutes
weight: 4
---

OpenTelemetry Gateway は、テレメトリーデータの受信・処理・エクスポートを行うように設計されています。テレメトリーソース（アプリケーションやサービスなど）と、バックエンド（Prometheus、Jaeger、Splunk Observability Cloud などの可観測性プラットフォーム）の間の中継役として動作します。

Gateway が有用なのは、テレメトリーデータの収集を一元化し、データのフィルタリング、変換、複数の宛先へのルーティングといった機能を実現できるためです。また、テレメトリー処理をオフロードすることで個々のサービスの負荷を軽減し、分散システム全体で一貫したデータフォーマットを保証します。これにより、複雑な環境でテレメトリーデータの管理、スケール、分析が容易になります。

{{% notice title="演習" style="green" icon="running" %}}

- **Gateway terminal** ウィンドウで `[WORKSHOP]` ディレクトリに移動し、`2-gateway` という名前のサブディレクトリを新規作成します。

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `[WORKSHOP]/2-gateway` ディレクトリに移動してください。**

- **Gateway terminal** ウィンドウに戻り、`1-agent` ディレクトリの `agent.yaml` を `2-gateway` にコピーします。
- `gateway.yaml` というファイルを作成し、以下の初期設定を追加します。

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

> [!NOTE]
> `gateway` を起動すると、`gateway-traces.out`、`gateway-metrics.out`、`gateway-logs.out` の 3 つのファイルが生成されます。これらのファイルには、最終的に Gateway が受信したテレメトリーデータが書き込まれます。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
