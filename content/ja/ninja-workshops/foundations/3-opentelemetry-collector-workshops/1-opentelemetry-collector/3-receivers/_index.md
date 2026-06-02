---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Receivers
weight: 3
---

ワークショップの receiver パートへようこそ！ここは OpenTelemetry Collector におけるデータパイプラインの起点となる部分です。さっそく見ていきましょう。

receiver は push 型または pull 型のいずれかで動作し、Collector にデータを取り込む仕組みです。receiver は 1 つ以上のデータソースをサポートできます。一般的に、receiver は指定されたフォーマットでデータを受け取り、それを内部フォーマットに変換したうえで、該当するパイプラインに定義された processor や exporter へ受け渡します。

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
