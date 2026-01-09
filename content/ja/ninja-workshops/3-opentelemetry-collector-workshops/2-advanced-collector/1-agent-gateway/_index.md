---
title: 1. Agent 設定の確認
linkTitle: 1. Agent Configuration


time: 15 minutes
weight: 3
---
ようこそ！このセクションでは、**Agent** と **Gateway** の両方を含む完全に機能する OpenTelemetry セットアップから始めます。

まず、設定ファイルを簡単に確認して、全体的な構造に慣れ、テレメトリーパイプラインを制御する重要なセクションを確認します。

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
ワークショップを通じて、複数のターミナルウィンドウを使用します。整理しやすくするために、各ターミナルに固有の名前または色を付けてください。これにより、演習中にターミナルを簡単に識別して切り替えることができます。

これらのターミナルを **Agent**、**Gateway**、**Loadgen**、**Test** と呼びます。
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

1. 最初のターミナルウィンドウを作成し、**Agent** と名前を付けます。最初の演習用ディレクトリ `[WORKSHOP]/1-agent-gateway` に移動し、必要なファイルが生成されていることを確認します：

    ```bash
    cd 1-agent-gateway
    ls -l
    ```

2. ディレクトリに以下のファイルが表示されるはずです。表示されない場合は、**前提条件** セクションで説明されている `setup-workshop.sh` スクリプトを再実行してください：

    ```text { title="Directory Structure" }
    .
    ├── agent.yaml
    └── gateway.yaml
    ```
<!--
3. **agent.yaml** ファイルの内容を確認します。このファイルは、**Agent** モードでデプロイされた OpenTelemetry Collector のコア構造を示しています：

    ```bash
        cat ./agent.yaml
    ```

4. このワークショップ用に事前設定されたセットアップが表示されます：

    ```yaml { title="agent.yaml" }
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
-->
{{% /notice %}}

### Agent 設定の理解

このワークショップで使用する `agent.yaml` ファイルの主要なコンポーネントを確認しましょう。メトリクス、トレース、ログをサポートするために重要な追加が行われています。

#### Receiver

`receivers` セクションは、**Agent** がテレメトリーデータを取り込む方法を定義します。このセットアップでは、3種類の Receiver が設定されています：

* **Host Metrics Receiver**

  ```yaml
  hostmetrics:                         # Host Metrics Receiver
    collection_interval: 3600s         # Collection Interval (1hr)
    scrapers:
      cpu:                             # CPU Scraper
  ```

  ローカルシステムから1時間ごとに CPU 使用率を収集します。これを使用してサンプルメトリクスデータを生成します。

* **OTLP Receiver（HTTP プロトコル）**

  ```yaml
  otlp:                                # OTLP Receiver
    protocols:
      http:                            # Configure HTTP protocol
        endpoint: "0.0.0.0:4318"       # Endpoint to bind to
  ```

  Agent がポート `4318` で HTTP 経由でメトリクス、トレース、ログを受信できるようにします。これは、今後の演習で Collector にデータを送信するために使用されます。

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

  Agent がローカルログファイル（`quotes.log`）を tail し、`source` や `sourceType` などのメタデータで強化された構造化ログイベントに変換できるようにします。

#### Exporter

* **Debug Exporter**

  ```yaml
    debug:                               # Exporter Type
      verbosity: detailed                # Enabled detailed debug output
  ```

* **OTLPHTTP Exporter**

  ```yaml
    otlphttp:                            # Exporter Type
      endpoint: "http://localhost:5318"  # Gateway OTLP endpoint
  ```

  `debug` Exporter はワークショップ中の可視性とデバッグのためにデータをコンソールに送信し、`otlphttp` Exporter はすべてのテレメトリーをローカルの **Gateway** インスタンスに転送します。

  **このデュアルエクスポート戦略により、生データをローカルで確認しながら、さらなる処理とエクスポートのためにダウンストリームに送信することができます。**
