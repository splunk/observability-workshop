---
title: OpenTelemetry Collector エクステンション
linkTitle: 2. エクステンション
weight: 2
---

さて、OpenTelemetry Collector はインストールできました。次は OpenTelemetry Collector のエクステンション（拡張機能）を見てみましょう。エクステンションはオプションで、主にテレメトリーデータの処理を伴わないタスクで使用できます。例としては、ヘルスモニタリング、サービスディスカバリ、データ転送などがあります。

{{< mermaid >}}
%%{
  init:{
    "theme": "base",
    "themeVariables": {
      "primaryColor": "#ffffff",
      "clusterBkg": "#eff2fb",
      "defaultLinkColor": "#333333"
    }
  }
}%%

flowchart LR;
    style E fill:#e20082,stroke:#333,stroke-width:4px,color:#fff
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
