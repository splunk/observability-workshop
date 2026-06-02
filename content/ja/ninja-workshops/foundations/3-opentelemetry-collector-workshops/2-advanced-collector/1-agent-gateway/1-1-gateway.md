---
title: 1.1 Gateway 設定の確認
linkTitle: 1.1 Gateway 設定
weight: 1
---

**OpenTelemetry Gateway** は、テレメトリデータの受信、処理、エクスポートを行う中央ハブとして機能します。テレメトリのソース（アプリケーションやサービスなど）と、Splunk Observability Cloud のような可観測性バックエンドとの間に配置されます。

テレメトリトラフィックを集中管理することで、Gateway はデータのフィルタリング、エンリッチメント、変換、複数の宛先へのルーティングといった高度な機能を実現します。テレメトリ処理をオフロードすることで個々のサービスへの負荷を軽減し、分散システム全体で一貫した標準化されたデータを保証します。

これにより、特に複雑なマルチサービス環境において、可観測性パイプラインの管理、スケール、分析が容易になります。

{{% exercise title="Gateway 設定の確認" %}}

2 つ目のターミナルウィンドウを開くか作成し、**Gateway** という名前を付けます。最初の演習ディレクトリ `[WORKSHOP]/1-agent-gateway` に移動し、`gateway.yaml` ファイルの内容を確認します。

このファイルは、**Gateway** モードでデプロイされる OpenTelemetry Collector の中核構造を示しています。

{{% /exercise %}}

## Gateway 設定の理解

このワークショップで OpenTelemetry Collector を **Gateway** モードとして構成する `gateway.yaml` ファイルを見ていきましょう。この **Gateway** は **Agent** からテレメトリを受信し、検査または転送のために処理してエクスポートする役割を担います。

* **OTLP Receiver（カスタムポート）**

  ```yaml
  receivers:
    otlp:
      protocols:
        http:
          endpoint: "0.0.0.0:5318"
  ```

  ポート `5318` は **Agent** 設定の `otlphttp` エクスポーターと一致しており、**Agent** が送信するすべてのテレメトリデータが **Gateway** で受け付けられるようにしています。

  > [!NOTE]
  > このようにポートを分離することで、競合を回避し、Agent と Gateway の役割を明確に保ちます。

* **File Exporter**

  **Gateway** は 3 つの File Exporter を使用して、テレメトリデータをローカルファイルに出力します。これらのエクスポーターは次のように定義されています。

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

  各エクスポーターは、特定のシグナルタイプを対応するファイルに書き出します。

  これらのファイルは Gateway の起動時に作成され、Agent がデータを送信するにつれて実際のテレメトリで満たされていきます。これらのファイルをリアルタイムで監視することで、パイプラインを流れるテレメトリの動きを観察できます。
