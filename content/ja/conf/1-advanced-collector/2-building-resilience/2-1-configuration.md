---
title: 2.1 File Storage Configuration
linkTitle: 2.1 Configuration
weight: 1
---

この演習では、`agent.yaml` ファイルの `extensions:` セクションを更新します。このセクションは OpenTelemetry の構成 YAML の一部で、OpenTelemetry Collector の動作を拡張または変更するオプションコンポーネントを定義します。

これらのコンポーネントはテレメトリーデータを直接処理するわけではありませんが、Collector の機能を向上させるための有用な機能やサービスを提供します。

{{% notice title="Exercise" style="green" icon="running" %}}

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウで `2-building-resilience` ディレクトリに移動し、`clear` コマンドを実行してください。**

ディレクトリ構造は以下のようになります:

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

**`agent.yaml` の更新**: **Agent ターミナル** ウィンドウで、既存の `health_check` エクステンションの下に `file_storage` エクステンションを追加します:

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

**エクスポーターへの `file_storage` の追加**: `otlphttp` エクスポーターを変更してリトライおよびキューイング機構を構成し、障害が発生した場合でもデータが保持され、再送されるようにします。`endpoint: "http://localhost:5318"` の下に以下を追加し、インデントが `endpoint` と一致していることを確認してください:

```yaml
    retry_on_failure:
      enabled: true                    # Enable retry on failure
    sending_queue:                     # 
      enabled: true                    # Enable sending queue
      num_consumers: 10                # No. of consumers
      queue_size: 10000                # Max. queue size
      storage: file_storage/checkpoint # File storage extension
```

**`services` セクションの更新**: 既存の `extensions:` セクションに `file_storage/checkpoint` エクステンションを追加します。構成は以下のようになります:

```yaml
service:
  extensions:
  - health_check
  - file_storage/checkpoint            # Enabled extensions for this collector
```

**`metrics` パイプラインの更新**: この演習では、デバッグやログのノイズを減らすために、Metric パイプラインから `hostmetrics` レシーバーをコメントアウトします。同様に、構成は以下のようになります:

```yaml
    metrics:
      receivers:
      # - hostmetrics                    # Hostmetric reciever (cpu only)
      - otlp
```

{{% /notice %}}

<!-- Validate the **Agent** configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `metrics:` section of your pipelines will look similar to this:

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
      REC1 -- > PRO1
      PRO1 -- > PRO2
      PRO2 -- > PRO3
      PRO3 -- > PRO4
      PRO4 -- > EXP1
      PRO4 -- > EXP2
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-metrics stroke:#38bdf8,stroke-width:1px, color:#38bdf8,stroke-dasharray: 3 3;
``` -->
