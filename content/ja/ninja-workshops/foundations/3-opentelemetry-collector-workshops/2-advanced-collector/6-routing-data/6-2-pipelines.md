---
title: 6.2 パイプラインの構成
linkTitle: 6.2 パイプラインの構成
weight: 2
---

{{% exercise title="ルーティングパイプラインを接続する" %}}

**元の `traces` パイプラインをルーティングを使用するように更新します**:

1. `routing` を有効にするため、元の `traces` パイプラインを更新して `routing` を唯一のエクスポーターとして使用します。これにより、すべてのスパンデータが評価のために **Routing Connector** を通過し、その後接続されたパイプラインへ送られます。また、**すべての** プロセッサーを削除し、空の配列（`[]`）に置き換えます。これらは `traces/route1-regular` および `traces/route2-security` パイプラインで処理され、それぞれのルートでカスタムの動作を実現できるようになります。`traces:` の構成は以下のようになります:

    ```yaml
    traces:                       # Traces pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors: []              # Processors for traces
      exporters:
      - routing
    ```

**既存の `traces` パイプラインの下に、`route1-regular` と `route2-security` の両方のトレースパイプラインを追加します**:

1. **Route1-regular パイプラインを構成する**: このパイプラインは、コネクター内のルーティングテーブルで **一致しなかった** すべてのスパンを処理します。
これは唯一のレシーバーとして `routing` を使用しており、元のトレースパイプラインから `connection` を通じてデータを受け取る点に注目してください。

    ```yaml
        traces/route1-regular:         # Default pipeline for unmatched spans
          receivers: 
          - routing                    # Receive data from the routing connector
          processors:
          - memory_limiter             # Memory Limiter Processor
          - resource/add_mode          # Adds collector mode metadata
          - batch
          exporters:
          - debug                      # Debug Exporter 
          - file/traces/route1-regular # File Exporter for unmatched spans 
    ```

2. **route2-security パイプラインを追加する**: このパイプラインは、ルーティングルール `"[deployment.environment"] == "security-applications"` に一致するすべてのスパンを処理します。このパイプラインもレシーバーとして `routing` を使用します。このパイプラインを `traces/route1-regular` の下に追加してください。

    ```yaml
        traces/route2-security:         # Default pipeline for unmatched spans
          receivers: 
          - routing                     # Receive data from the routing connector
          processors:
          - memory_limiter              # Memory Limiter Processor
          - resource/add_mode           # Adds collector mode metadata
          - batch
          exporters:
          - debug                       # Debug exporter
          - file/traces/route2-security # File exporter for unmatched spans
    ```

{{% /exercise %}}

エージェント構成を **[otelbin.io](https://www.otelbin.io/)** で検証します。参考として、パイプラインの `traces:` セクションは以下のようになります:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;&nbsp;otlp&nbsp;&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(memory_limiter<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO4(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO5(batch<br>fa:fa-microchip):::processor
      PRO6(batch<br>fa:fa-microchip):::processor
      EXP1(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload):::exporter
      EXP2(&emsp;&emsp;file&emsp;&emsp;<br>fa:fa-upload<br>traces):::exporter
      EXP3(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload):::exporter
      EXP4(&emsp;&emsp;file&emsp;&emsp;<br>fa:fa-upload<br>traces):::exporter
      ROUTE1(&nbsp;routing&nbsp;<br>fa:fa-route):::con-export
      ROUTE2(&nbsp;routing&nbsp;<br>fa:fa-route):::con-receive
      ROUTE3(&nbsp;routing&nbsp;<br>fa:fa-route):::con-receive
    %% Links
    subID1:::sub-traces
    subID2:::sub-traces
    subID3:::sub-traces
    subgraph " "
    direction LR
      subgraph subID1["`**Traces**`"]
      REC1 --> ROUTE1
      end
      subgraph subID2["`**Traces/route2-security**`"]
      ROUTE1 --> ROUTE2
      ROUTE2 --> PRO1
      PRO1 --> PRO3
      PRO3 --> PRO5
      PRO5 --> EXP1
      PRO5 --> EXP2
      end
      subgraph subID3["`**Traces/route1-regular**`"]
      ROUTE1 --> ROUTE3
      ROUTE3 --> PRO2
      PRO2 --> PRO4
      PRO4 --> PRO6
      PRO6 --> EXP3
      PRO6 --> EXP4
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
