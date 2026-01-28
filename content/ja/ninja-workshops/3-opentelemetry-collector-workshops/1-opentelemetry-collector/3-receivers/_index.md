---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Receivers
weight: 3
---

ワークショップの Receiver セクションへようこそ！ここは OpenTelemetry Collector のデータパイプラインの出発点です。早速始めましょう。

Receiver は、プッシュベースまたはプルベースであり、データを Collector に取り込む方法です。Receiver は1つ以上のデータソースをサポートできます。一般的に、Receiver は指定された形式でデータを受け取り、内部形式に変換してから、該当するパイプラインで定義された Processor と Exporter に渡します。

{{< mermaid >}}
%%{
  init:{
    "theme":"base",
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
