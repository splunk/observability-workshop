---
title: 6.2 パイプラインの設定
linkTitle: 6.2 パイプライン設定
weight: 2
---

{{% exercise title="ルーティングパイプラインの接続" %}}

**既存の `traces` パイプラインを routing を使用するように更新します**:

1. `routing` を有効にするには、既存の `traces` パイプラインのエクスポーターを `routing` のみに更新します。これにより、すべてのスパンデータが **Routing Connector** を通じて評価され、接続されたパイプラインに転送されます。また、**すべての** プロセッサーを削除し、空の配列（`[]`）に置き換えます。プロセッサーの処理は `traces/route1-regular` と `traces/route2-security` パイプラインで行われるようになり、各ルートごとにカスタム動作が可能になります。`traces:` の設定は次のようになります:

    ```yaml
    traces:                       # Traces pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors: []              # Processors for traces
      exporters:
      - routing
    ```

**既存の `traces` パイプラインの下に `route1-regular` と `route2-security` の両方の traces パイプラインを追加します**:

1. **Route1-regular パイプラインの設定**: このパイプラインは、コネクターのルーティングテーブルに**一致しない**すべてのスパンを処理します。このパイプラインは `routing` のみをレシーバーとして使用し、元の traces パイプラインからの `connection` を通じてデータを受信します。

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

2. **route2-security パイプラインの追加**: このパイプラインは、ルーティングルールの `"[deployment.environment"] == "security-applications"` に一致するすべてのスパンを処理します。このパイプラインも `routing` をレシーバーとして使用します。このパイプラインを `traces/route1-regular` の下に追加してください。

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

**[otelbin.io](https://www.otelbin.io/)** を使用してエージェントの設定を検証します。参考として、パイプラインの `traces:` セクションは次のようになります:

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
