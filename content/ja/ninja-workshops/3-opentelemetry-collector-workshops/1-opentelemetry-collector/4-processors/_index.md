---
title: OpenTelemetry Collector Processors
linkTitle: 4. Processors
weight: 4
---

[**Processors**](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/README.md) は、データを受信してからエクスポートするまでの間に実行されます。Processors はオプションですが、一部は推奨されています。OpenTelemetry contrib Collector には [**多数の Processors**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor) が含まれています。

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
