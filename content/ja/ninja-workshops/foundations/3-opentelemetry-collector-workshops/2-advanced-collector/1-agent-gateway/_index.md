---
title: 1. エージェント設定の確認
linkTitle: 1. エージェント設定
time: 15 minutes
weight: 3
---
ようこそ！ このセクションでは、**Agent** と **Gateway** の両方を含む完全に動作する OpenTelemetry のセットアップから始めます。

まずは設定ファイルをざっと確認し、全体の構造を把握するとともに、テレメトリパイプラインを制御する重要なセクションに注目していきます。

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
ワークショップ全体を通して、複数のターミナルウィンドウを使用します。整理しやすくするために、各ターミナルに固有の名前や色を付けてください。これにより、演習中にターミナルを簡単に識別して切り替えられるようになります。

これらのターミナルは、**Agent**、**Gateway**、**Loadgen**、**Test** と呼びます。
{{% /notice %}}

{{% exercise title="エージェントファイルの確認" %}}

1. 最初のターミナルウィンドウを作成し、**Agent** という名前を付けます。最初の演習用のディレクトリ `[WORKSHOP]/1-agent-gateway` に移動し、必要なファイルが生成されていることを確認します。

    ```bash
    cd 1-agent-gateway
    ls -l
    ```
  
2. ディレクトリ内に以下のファイルが表示されるはずです。表示されない場合は、**Pre-requisites** セクションの説明に従って `setup-workshop.sh` スクリプトを再実行してください。

    ```text { title="Directory Structure" }
    .
    ├── agent.yaml
    └── gateway.yaml
    ```

{{% /exercise %}}

## エージェント設定の理解

このワークショップで使用する `agent.yaml` ファイルの主要なコンポーネントを確認しましょう。メトリクス、トレース、ログをサポートするためにいくつかの重要な追加を行っています。

### Receivers

`receivers` セクションでは、**Agent** がどのようにテレメトリデータを取り込むかを定義します。このセットアップでは、3 種類のレシーバーが設定されています。

* **Host Metrics Receiver**

  ```yaml
  hostmetrics:                         # Host Metrics Receiver
    collection_interval: 3600s         # Collection Interval (1hr)
    scrapers:
      cpu:                             # CPU Scraper
  ```

  ローカルシステムから 1 時間ごとに CPU 使用率を収集します。これを使ってメトリクスデータのサンプルを生成します。

* **OTLP Receiver (HTTP protocol)**

  ```yaml
  otlp:                                # OTLP Receiver
    protocols:
      http:                            # Configure HTTP protocol
        endpoint: "0.0.0.0:4318"       # Endpoint to bind to
  ```

  エージェントがポート `4318` で HTTP 経由でメトリクス、トレース、ログを受信できるようにします。これは今後の演習でコレクターにデータを送信するために使用されます。

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

  エージェントがローカルのログファイル (`quotes.log`) を tail し、`source` や `sourceType` などのメタデータで強化された構造化ログイベントに変換できるようにします。

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

  `debug` エクスポーターは、ワークショップ中の可視化とデバッグのためにコンソールにデータを送信し、`otlphttp` エクスポーターはすべてのテレメトリをローカルの **Gateway** インスタンスに転送します。

  **この二重エクスポート戦略により、ローカルで生データを確認しながら、下流に送信してさらなる処理とエクスポートを行うことができます。**
