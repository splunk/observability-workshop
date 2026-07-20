---
title: 8.2 パイプラインの設定
linkTitle: 8.2 パイプライン設定
weight: 2
---

{{% notice title="演習" style="green" icon="running" %}}

**`traces` パイプラインを更新してルーティングを使用する**:

1. `routing`を有効にするために、`routing`を唯一のExporterとして使用するように元の `traces:` パイプラインを更新します。これにより、すべてのSpanデータが評価のためにrouting connectorを通じて送信されます。
2. すべてのProcessorを削除し、空の配列（`[]`）に置き換えます。これらは `traces/standard` および `traces/security` パイプラインで定義されるようになりました。

    ```yaml
      pipelines:
        traces:                           # Original traces pipeline
          receivers: 
          - otlp                          # OTLP Receiver
          processors: []
          exporters: 
          - routing                       # Routing Connector
    ```

**`standard` と `security` の両方のTracesパイプラインを追加する**:

1. **Securityパイプラインの設定**: このパイプラインは、`security`のルーティングルールに一致するすべてのSpanを処理します。
これはReceiverとして `routing` を使用します。既存の `traces:` パイプラインの下に配置します。

    ```yaml
        traces/security:              # New Security Traces/Spans Pipeline
          receivers: 
          - routing                   # Receive data from the routing connector
          processors:
          - memory_limiter            # Memory Limiter Processor
          - resource/add_mode         # Adds collector mode metadata
          - batch
          exporters:
          - debug                     # Debug Exporter 
          - file/traces/security      # File Exporter for spans matching rule
    ```

2. **Standardパイプラインの追加**: このパイプラインは、ルーティングルールに一致しないすべてのSpanを処理します。
このパイプラインもReceiverとして `routing` を使用します。`traces/security` の下に追加します。

    ```yaml
        traces/standard:              # Default pipeline for unmatched spans
          receivers: 
          - routing                   # Receive data from the routing connector
          processors:
          - memory_limiter            # Memory Limiter Processor
          - resource/add_mode         # Adds collector mode metadata
          - batch
          exporters:
          - debug                     # Debug exporter
          - file/traces/standard      # File exporter for unmatched spans
    ```

{{% /notice %}}

**[otelbin.io](https://www.otelbin.io/)** を使用してエージェント設定を検証します。参考として、パイプラインの `traces:` セクションは以下のようになります。

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
      subgraph subID2[**Traces/standard**]
      ROUTE1 --> ROUTE2
      ROUTE2 --> PRO1
      PRO1 --> PRO3
      PRO3 --> PRO5
      PRO5 --> EXP1
      PRO5 --> EXP2
      end
      subgraph subID3[**Traces/security**]
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
