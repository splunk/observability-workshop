---
title: 1. Agent設定の確認
linkTitle: 1. Agent設定
time: 15 minutes
weight: 3
---
ようこそ！このセクションでは、 **Agent** と **Gateway** の両方を含む、完全に機能するOpenTelemetryセットアップから始めます。

まず、設定ファイルを簡単に確認して、全体の構造に慣れ、テレメトリパイプラインを制御する重要なセクションを把握します。

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
ワークショップを通じて、複数のターミナルウィンドウを使用します。整理するために、各ターミナルに固有の名前や色を付けてください。これにより、演習中にターミナルを簡単に識別して切り替えることができます。

これらのターミナルを **Agent** 、 **Gateway** 、 **Loadgen** 、 **Test** と呼びます。
{{% /notice %}}

{{% exercise title="Agentファイルの確認" %}}

1. 最初のターミナルウィンドウを作成し、 **Agent** と名前を付けます。最初の演習のディレクトリ `[WORKSHOP]/1-agent-gateway` に移動し、必要なファイルが生成されていることを確認します。

    ```bash
    cd 1-agent-gateway
    ls -l
    ```
  
2. ディレクトリに以下のファイルが表示されます。表示されない場合は、 **Pre-requisites** セクションに記載されている `setup-workshop.sh` スクリプトを再実行してください。

    ```text { title="Directory Structure" }
    .
    ├── agent.yaml
    └── gateway.yaml
    ```

{{% /exercise %}}

## Agent設定の理解

このワークショップで使用する `agent.yaml` ファイルの主要なコンポーネントを確認しましょう。メトリクス、トレース、ログをサポートするためにいくつかの重要な追加が行われています。

### Receivers

`receivers` セクションは、 **Agent** がテレメトリデータを取り込む方法を定義します。このセットアップでは、3種類のReceiverが設定されています。

* **Host Metrics Receiver**

  ```yaml
  hostmetrics:                         # Host Metrics Receiver
    collection_interval: 3600s         # Collection Interval (1hr)
    scrapers:
      cpu:                             # CPU Scraper
  ```

  ローカルシステムからCPU使用率を1時間ごとに収集します。これを使用してメトリクスデータの例を生成します。

* **OTLP Receiver（HTTPプロトコル）**

  ```yaml
  otlp:                                # OTLP Receiver
    protocols:
      http:                            # Configure HTTP protocol
        endpoint: "0.0.0.0:4318"       # Endpoint to bind to
  ```

  Agentがポート `4318` でHTTP経由のメトリクス、トレース、ログを受信できるようにします。これは今後の演習でCollectorにデータを送信するために使用されます。

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

  Agentがローカルログファイル（`quotes.log`）をtailし、 `source` や `sourceType` などのメタデータで強化された構造化ログイベントに変換できるようにします。

### Exporters

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

  `debug` Exporterはワークショップ中の可視性とデバッグのためにデータをコンソールに送信し、 `otlphttp` Exporterはすべてのテレメトリをローカルの **Gateway** インスタンスに転送します。

  **このデュアルエクスポート戦略により、ローカルで生データを確認しながら、さらなる処理とエクスポートのために下流に送信できます。**
