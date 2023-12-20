---
title: OpenTelemetry Collector プロセッサー
linkTitle: 4. プロセッサー
weight: 4
---


[**プロセッサー**](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/README.md)は、レシーバーとエクスポーターとの間で、データに対して実行される処理です。プロセッサーはオプションですが、いくつかは推奨されています。OpenTelemetry Collector Contrib には[多数のプロセッサー](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor)が含まれています。

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
    style Processors fill:#e20082,stroke:#333,stroke-width:4px,color:#fff
    subgraph Receivers
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
