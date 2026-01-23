---
title: 1.1 Gateway 設定の確認
linkTitle: 1.1 Gateway Configuration
weight: 1
---

**OpenTelemetry Gateway** は、テレメトリーデータの受信、処理、エクスポートのための中央ハブとして機能します。テレメトリーソース（アプリケーションやサービスなど）と Splunk Observability Cloud のようなオブザーバビリティバックエンドの間に位置します。

テレメトリートラフィックを集中化することで、Gateway はデータのフィルタリング、エンリッチメント、変換、および1つ以上の宛先へのルーティングなどの高度な機能を実現します。個々のサービスからテレメトリー処理をオフロードすることで負担を軽減し、分散システム全体で一貫した標準化されたデータを確保します。

これにより、オブザーバビリティパイプラインの管理、スケーリング、分析が容易になります。特に複雑なマルチサービス環境では効果的です。

{{% notice title="Exercise" style="green" icon="running" %}}

2つ目のターミナルウィンドウを開くか作成し、**Gateway** と名前を付けます。最初の演習ディレクトリ `[WORKSHOP]/1-agent-gateway` に移動し、`gateway.yaml` ファイルの内容を確認します。

このファイルは、**Gateway** モードでデプロイされた OpenTelemetry Collector のコア構造を示しています。

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

### Gateway 設定の理解

このワークショップで **Gateway** モードの OpenTelemetry Collector がどのように設定されているかを定義する `gateway.yaml` ファイルを確認しましょう。この **Gateway** は、**Agent** からテレメトリーを受信し、処理してから検査または転送のためにエクスポートする役割を担います。

* **OTLP Receiver（カスタムポート）**

  ```yaml
  receivers:
    otlp:
      protocols:
        http:
          endpoint: "0.0.0.0:5318"
  ```

  ポート `5318` は **Agent** 設定の `otlphttp` Exporter と一致しており、**Agent** が送信するすべてのテレメトリーデータが **Gateway** で受け入れられることを保証します。

> [!NOTE]
> このポートの分離により、競合を回避し、Agent と Gateway の役割間の責任を明確に保ちます。

* **File Exporter**

  **Gateway** は3つの File Exporter を使用して、テレメトリーデータをローカルファイルに出力します。これらの Exporter は以下のように定義されています

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

  各 Exporter は、特定のシグナルタイプを対応するファイルに書き込みます。

  これらのファイルは Gateway が起動すると作成され、Agent がデータを送信すると実際のテレメトリーが書き込まれます。これらのファイルをリアルタイムで監視して、パイプラインを通過するテレメトリーの流れを観察できます。
