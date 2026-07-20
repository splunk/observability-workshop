---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Receivers
weight: 3
---

ワークショップのReceiverセクションへようこそ！ここはOpenTelemetry Collectorのデータパイプラインの出発点です。さっそく始めましょう。

Receiverはプッシュまたはプルベースで、Collectorにデータを取り込む方法です。Receiverは1つ以上のデータソースをサポートできます。一般的に、Receiverは指定されたフォーマットでデータを受け取り、内部フォーマットに変換し、該当するパイプラインで定義されたProcessorとExporterにデータを渡します。

{{< mermaid >}}
%%{
  init:{
    "themeVariables": {
      "primaryColor": "#ffffff",
      "clusterBkg": "#eff2fb",
      "defaultLinkColor": "#333333"
    }
  }
}%%

flowchart LR;
    style M fill:#e20082,stroke:#333,stroke-width:4px,color:#fff
    subgraph Collector
    A[OTLP] --> M(Receivers)
    B[JAEGER] --> M(Receivers)
    C[Prometheus] --> M(Receivers)
    end
    subgraph Processors
    M(Receivers) --> H(Filters, Attributes, etc)
    E(Extensions)
    end
    subgraph Exporters
    H(Filters, Attributes, etc) --> S(OTLP)
    H(Filters, Attributes, etc) --> T(JAEGER)
    H(Filters, Attributes, etc) --> U(Prometheus)
    end
{{< /mermaid >}}
