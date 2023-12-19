---
title: OpenTelemetry Collector Exporters
linkTitle: 5. Exporters
weight: 5
---

An exporter, which can be push or pull-based, is how you send data to one or more backends/destinations. Exporters may support one or more data sources.

For this workshop, we will be using the [**otlphttp**](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) exporter. The OpenTelemetry Protocol (OTLP) is a vendor-neutral, standardised protocol for transmitting telemetry data. The OTLP exporter sends data to a server that implements the OTLP protocol. The OTLP exporter supports both [**gRPC**](https://grpc.io/) and [**HTTP**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)/[**JSON**](https://www.json.org/json-en.html) protocols.

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
    style Exporters fill:#e20082,stroke:#333,stroke-width:4px,color:#fff
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
