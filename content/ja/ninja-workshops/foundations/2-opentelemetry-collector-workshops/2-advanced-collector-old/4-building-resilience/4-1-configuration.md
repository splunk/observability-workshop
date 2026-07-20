---
title: 4.1 File Storage の設定
linkTitle: 4.1 設定
weight: 1
---

この演習では、`agent.yaml` ファイルの `extensions:` セクションを更新します。このセクションはOpenTelemetry設定YAMLの一部であり、OpenTelemetry Collectorの動作を拡張または変更するオプションコンポーネントを定義します。

これらのコンポーネントはテレメトリデータを直接処理しませんが、Collectorの機能を向上させる有用な機能とサービスを提供します。

{{% notice title="演習" style="green" icon="running" %}}

**`agent.yaml` を更新**: **Agent ターミナル** ウィンドウで、`file_storage` extension を追加し、`checkpoint` と名前を付けます。

```yaml
  file_storage/checkpoint:             # Extension Type/Name
    directory: "./checkpoint-dir"      # Define directory
    create_directory: true             # Create directory
    timeout: 1s                        # Timeout for file operations
    compaction:                        # Compaction settings
      on_start: true                   # Start compaction at Collector startup
      # Define compaction directory
      directory: "./checkpoint-dir/tmp"
      max_transaction_size: 65536      # Max. size limit before compaction occurs
```

**既存の `otlphttp` Exporter に `file_storage` を追加**: `otlphttp:` Exporter を変更して、リトライとキューイングメカニズムを設定し、障害が発生した場合にデータが保持され再送信されるようにします。

```yaml
  otlphttp: 
    endpoint: "http://localhost:5318"
    retry_on_failure:
      enabled: true                    # Enable retry on failure
    sending_queue:                     # 
      enabled: true                    # Enable sending queue
      num_consumers: 10                # No. of consumers
      queue_size: 10000                # Max. queue size
      storage: file_storage/checkpoint # File storage extension
```

**`services` セクションを更新**: 既存の `extensions:` セクションに `file_storage/checkpoint` extension を追加します。これにより、extension が有効になります。

```yaml
service:
  extensions:
  - health_check
  - file_storage/checkpoint            # Enabled extensions for this collector
```

**`metrics` パイプラインを更新**: この演習では、デバッグとログのノイズを減らすために、Metricパイプラインから `hostmetrics` Receiver を削除します。

```yaml
    metrics:
      receivers:
      - otlp
      # - hostmetrics                  # Hostmetrics Receiver
```

{{% /notice %}}

**[otelbin.io](https://www.otelbin.io/)** を使用して `agent` の設定を検証します。参考として、パイプラインの `metrics:` セクションは以下のようになります。

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resourcedetection<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO4(batch<br>fa:fa-microchip):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
      EXP2(otlphttp<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-metrics
    subgraph " "
      subgraph subID1["`**Metrics**`"]
      direction LR
      REC1 --> PRO1
      PRO1 --> PRO2
      PRO2 --> PRO3
      PRO3 --> PRO4
      PRO4 --> EXP1
      PRO4 --> EXP2
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-metrics stroke:#38bdf8,stroke-width:1px, color:#38bdf8,stroke-dasharray: 3 3;
```
