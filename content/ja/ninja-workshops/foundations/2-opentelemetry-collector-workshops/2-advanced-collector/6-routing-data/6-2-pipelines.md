---
title: 6.2 パイプラインの設定
linkTitle: 6.2 パイプラインの設定
weight: 2
---

{{% exercise title="ルーティングパイプラインの接続" %}}

**元の `traces` パイプラインを routing を使用するように更新します**:

1. `routing` を有効にするために、元の `traces` パイプラインで `routing` を唯一のExporterとして使用するように更新します。これにより、すべてのSpanデータが **Routing Connector** を通じて評価され、接続されたパイプラインに転送されます。また、**すべての** Processorを削除し、空の配列（`[]`）に置き換えます。これは `traces/route1-regular` と `traces/route2-security` パイプラインで処理されるようになり、各ルートにカスタム動作を設定できるようになります。`traces:` の設定は以下のようになります:

    ```yaml
    traces:                       # Traces pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors: []              # Processors for traces
      exporters:
      - routing
    ```

**既存の `traces` パイプラインの下に `route1-regular` と `route2-security` の両方のTracesパイプラインを追加します**:

1. **Route1-regularパイプラインの設定**: このパイプラインは、Connectorのルーティングテーブルで **一致しない** すべてのSpanを処理します。このパイプラインは `routing` を唯一のReceiverとして使用し、元のTracesパイプラインからの `connection` を通じてデータを受信します。

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

2. **route2-securityパイプラインの追加**: このパイプラインは、ルーティングルールで `"[deployment.environment"] == "security-applications"` に一致するすべてのSpanを処理します。このパイプラインも `routing` をReceiverとして使用します。`traces/route1-regular` の下にこのパイプラインを追加します。

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

**[otelbin.io](https://www.otelbin.io/)** を使用してエージェントの設定を検証します。参考として、パイプラインの `traces:` セクションは以下のようになります:

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
