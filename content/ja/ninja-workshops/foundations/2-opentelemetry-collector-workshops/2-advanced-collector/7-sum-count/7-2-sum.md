---
title: 7.2 Sum Connectorでメトリクスを作成する
linkTitle: 7.2 Sum Connector
time: 10 minutes
weight: 2
---

このセクションでは、[**Sum Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/sumconnector) がSpanから値を抽出してメトリクスに変換する方法を探ります。

具体的には、ベースとなるSpanからクレジットカードの請求額を取得し、Sum Connectorを利用して合計請求額をメトリクスとして取得します。

このConnectorは、Span、Spanイベント、メトリクス、データポイント、ログレコードから属性値を収集（**sum**）するために使用できます。個々の値をキャプチャし、メトリクスに変換して送信します。ただし、これらのメトリクスとその属性を使用して計算やさらなる処理を行うのは **バックエンド** の役割です。

{{% exercise title="Sum Connectorを追加する" %}}

**Agent terminal** ウィンドウに切り替えて、エディタで `agent.yaml` ファイルを開きます。

- **Sum Connectorを追加する**  
設定のconnectorsセクションにSum Connectorを追加し、メトリクスカウンターを定義します

```yaml
  sum:
    spans:
       user.card-charge:
        source_attribute: payment.amount
        conditions:
          - attributes["payment.amount"] != "NULL"
        attributes:
          - key: user.name
    
```

{{% /exercise %}}

上記の例では、Span内の `payment.amount` 属性を確認します。有効な値がある場合、**Sum** Connectorは `user.card-charge` というメトリクスを生成し、`user.name` を属性として含めます。これにより、バックエンドは請求サイクルなどの長期間にわたるユーザーの合計請求額を追跡・表示できます。

以下のパイプライン設定では、ConnectorのExporterがtracesセクションに追加され、ConnectorのReceiverがmetricsセクションに追加されています。

{{% exercise title="Connectorをパイプラインに接続する" %}}

- **Count Connectorをパイプラインに設定する**

```yaml
  pipelines:
    traces:
      receivers:
      - otlp
      processors:
      - memory_limiter
      - attributes/update              # Update, hash, and remove attributes
      - redaction/redact               # Redact sensitive fields using regex
      - resourcedetection
      - resource/add_mode
      - batch
      exporters:
      - debug
      - file
      - otlphttp
      - sum                            # Sum connector which aggregates payment.amount from spans and sends to metrics pipeline
    metrics:
      receivers:
      - sum                            # Receives metrics from the sum exporter in the traces pipeline
      - count                          # Receives count metric from logs count exporter in logs pipeline. 
      - otlp
      #- hostmetrics                   # Host Metrics Receiver
      processors:
      - memory_limiter
      - resourcedetection
      - resource/add_mode
      - batch
      exporters:
      - debug
      - otlphttp
    logs:
      receivers:
      - otlp
      - filelog/quotes
      processors:
      - memory_limiter
      - resourcedetection
      - resource/add_mode
      - transform/logs                 # Transform logs processor
      - batch
      exporters:
      - count                          # Count Connector that exports count as a metric to metrics pipeline.
      - debug
      - otlphttp
```

- **[otelbin.io](https://www.otelbin.io/)** を使用してエージェント設定を **検証** します。参考として、パイプラインの `traces` と `metrics:` セクションは以下のようになります

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
    REC1(otlp<br>fa:fa-download<br> ):::receiver
    REC3(otlp<br>fa:fa-download<br> ):::receiver
    PRO1(memory_limiter<br>fa:fa-microchip<br> ):::processor
    PRO2(memory_limiter<br>fa:fa-microchip<br> ):::processor
    PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
    PRO4(resource<br>fa:fa-microchip<br>add_mode):::processor
    PRO5(batch<br>fa:fa-microchip<br> ):::processor
    PRO6(batch<br>fa:fa-microchip<br> ):::processor
    PRO7(resourcedetection<br>fa:fa-microchip<br> ):::processor
    PRO8(resourcedetection<br>fa:fa-microchip<br>):::processor

    PROA(attributes<br>fa:fa-microchip<br>redact):::processor
    PROB(redaction<br>fa:fa-microchip<br>update):::processor
    EXP1(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload<br> ):::exporter
    EXP2(&emsp;&emsp;file&emsp;&emsp;<br>fa:fa-upload<br> ):::exporter
    EXP3(&nbsp;&ensp;debug&nbsp;&ensp;<br>fa:fa-upload<br> ):::exporter
    EXP4(&emsp;&emsp;otlphttp&emsp;&emsp;<br>fa:fa-upload<br> ):::exporter
    EXP5(&emsp;&emsp;otlphttp&emsp;&emsp;<br>fa:fa-upload<br> ):::exporter
    ROUTE1(&nbsp;sum&nbsp;<br>fa:fa-route<br> ):::con-export
    ROUTE2(&nbsp;count&nbsp;<br>fa:fa-route<br> ):::con-receive
    ROUTE3(&nbsp;sum&nbsp;<br>fa:fa-route<br> ):::con-receive

    %% Links
    subgraph wrapper[" "]
      direction LR
      subgraph subID1["`**Traces**`"]
        direction LR
        REC1 --> PRO1
        PRO1 --> PROA
        PROA --> PROB
        PROB --> PRO7
        PRO7 --> PRO3
        PRO3 --> PRO5
        PRO5 --> EXP1
        PRO5 --> EXP2
        PRO5 --> EXP5
        PRO5 --> ROUTE1
      end

      subgraph subID2["`**Metrics**`"]
        direction LR
        ROUTE1 --> ROUTE3
        ROUTE3 --> PRO2
        ROUTE2 --> PRO2
        REC3 --> PRO2
        PRO2 --> PRO8
        PRO8 --> PRO4
        PRO4 --> PRO6
        PRO6 --> EXP3
        PRO6 --> EXP4
      end
    end
    class subID1 sub-traces
    class subID2 sub-metrics

classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-logs stroke:#34d399,stroke-width:1px,color:#34d399,stroke-dasharray: 3 3;
classDef sub-traces stroke:#fbbf24,stroke-width:1px,color:#fbbf24,stroke-dasharray: 3 3;
classDef sub-metrics stroke:#38bdf8,stroke-width:1px,color:#38bdf8,stroke-dasharray: 3 3;
```

{{% /exercise %}}
