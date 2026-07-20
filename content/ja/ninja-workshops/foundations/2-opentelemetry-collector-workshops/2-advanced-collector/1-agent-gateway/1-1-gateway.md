---
title: 1.1 Gateway設定の確認
linkTitle: 1.1 Gateway設定
weight: 1
---

**OpenTelemetry Gateway** は、テレメトリデータの受信、処理、エクスポートを行う中央ハブとして機能します。アプリケーションやサービスなどのテレメトリソースと、Splunk Observability Cloudのようなオブザーバビリティバックエンドの間に位置します。

テレメトリトラフィックを集中管理することで、Gatewayはデータのフィルタリング、エンリッチメント、変換、1つまたは複数の宛先へのルーティングなどの高度な機能を実現します。個々のサービスからテレメトリ処理をオフロードして負担を軽減し、分散システム全体で一貫した標準化されたデータを確保します。

これにより、特に複雑なマルチサービス環境において、オブザーバビリティパイプラインの管理、スケーリング、分析が容易になります。

{{% exercise title="Gateway設定の確認" %}}

2つ目のターミナルウィンドウを開くか作成し、 **Gateway** と名前を付けます。最初の演習ディレクトリ `[WORKSHOP]/1-agent-gateway` に移動し、`gateway.yaml` ファイルの内容を確認します。

このファイルは、 **Gateway** モードでデプロイされたOpenTelemetry Collectorのコア構造を概説しています。

{{% /exercise %}}

## Gateway設定の理解

このワークショップでOpenTelemetry Collectorが **Gateway** モードでどのように設定されているかを定義する `gateway.yaml` ファイルを見ていきましょう。この **Gateway** は、 **Agent** からテレメトリを受信し、処理してエクスポートする役割を担います。

* **OTLP Receiver（カスタムポート）**

  ```yaml
  receivers:
    otlp:
      protocols:
        http:
          endpoint: "0.0.0.0:5318"
  ```

  ポート `5318` は **Agent** 設定の `otlphttp` Exporterと一致しており、 **Agent** から送信されるすべてのテレメトリデータが **Gateway** で受信されることを保証します。

  > [!NOTE]
  > このポートの分離により、競合を回避し、AgentとGatewayの役割間の責任を明確に保ちます。

* **File Exporter**

  **Gateway** は3つのFile Exporterを使用して、テレメトリデータをローカルファイルに出力します。これらのExporterは以下のように定義されています。

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

  各Exporterは特定のシグナルタイプを対応するファイルに書き込みます。

  これらのファイルはGatewayの起動時に作成され、Agentがデータを送信するにつれて実際のテレメトリが書き込まれます。これらのファイルをリアルタイムで監視して、パイプラインを通じたテレメトリの流れを観察できます。
