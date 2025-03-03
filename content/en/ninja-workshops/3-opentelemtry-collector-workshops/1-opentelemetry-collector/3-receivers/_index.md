---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Receivers
weight: 3
---

Welcome to the receiver portion of the workshop! This is the starting point of the data pipeline of the OpenTelemetry Collector. Let's dive in.

A receiver, which can be push or pull based, is how data gets into the Collector. Receivers may support one or more data sources. Generally, a receiver accepts data in a specified format, translates it into the internal format and passes it to processors and exporters defined in the applicable pipelines.

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
