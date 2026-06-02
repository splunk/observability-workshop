---
title: 6.2 Configuring the Pipelines
linkTitle: 6.2 Pipeline Configuration
weight: 2
---

{{% notice title="演習" style="green" icon="running" %}}

**元の `traces` パイプラインを更新してルーティングを使用します**:

1. `routing` を有効化するために、元の `traces` パイプラインを更新して `routing` を唯一の exporter として使用するようにします。これにより、すべてのスパンデータが **Routing Connector** を経由して評価され、その後接続されたパイプラインへ送られます。また、processors は **すべて** 削除し、空配列（`[]`）に置き換えてください。これは `traces/route1-regular` と `traces/route2-security` のパイプライン側で扱われるようになり、ルートごとにカスタム動作を実現できるためです。`traces:` の設定は次のようになります:

    ```yaml
    traces:                       # Traces pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors: []              # Processors for traces
      exporters:
      - routing
    ```

**既存の `traces` パイプラインの下に、`route1-regular` と `route2-security` の両方の traces パイプラインを追加します**:

1. **Route1-regular パイプラインの設定**: このパイプラインは、connector のルーティングテーブルで **どれにも一致しない** すべてのスパンを処理します。
このパイプラインは receiver として `routing` のみを使用し、`connection` を通じて元の traces パイプラインからデータを受け取ることに注目してください。

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

2. **route2-security パイプラインの追加**: このパイプラインは、ルーティングルール `"[deployment.environment"] == "security-applications"` に一致するすべてのスパンを処理します。このパイプラインも receiver として `routing` を使用します。`traces/route1-regular` の下にこのパイプラインを追加してください。

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

{{% /notice %}}

<!--
Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `traces:` section of your pipelines will look similar to this:

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
      REC1 -- > ROUTE1
      end
      subgraph subID2[**Traces/standard**]
      ROUTE1 -- > ROUTE2
      ROUTE2 -- > PRO1
      PRO1 -- > PRO3
      PRO3 -- > PRO5
      PRO5 -- > EXP1
      PRO5 -- > EXP2
      end
      subgraph subID3[**Traces/security**]
      ROUTE1 -- > ROUTE3
      ROUTE3 -- > PRO2
      PRO2 -- > PRO4
      PRO4 -- > PRO6
      PRO6 -- > EXP3
      PRO6 -- > EXP4
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
-->