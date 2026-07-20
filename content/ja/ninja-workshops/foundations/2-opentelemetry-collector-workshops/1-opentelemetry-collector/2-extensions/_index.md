---
title: OpenTelemetry Collector Extensions
linkTitle: 2. Extensions
weight: 2
---

OpenTelemetry Collectorのインストールが完了したので、OpenTelemetry CollectorのExtensionを見ていきましょう。Extensionはオプションであり、主にテレメトリデータの処理を伴わないタスクに使用されます。Extensionの例としては、ヘルスモニタリング、サービスディスカバリ、データ転送などがあります。

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
