---
title: OpenTelemetry Collector Exporters
linkTitle: 5. Exporters
weight: 5
---

Exporterはプッシュ型またはプル型で、1つ以上のバックエンド/宛先にデータを送信する方法です。Exporterは1つ以上のデータソースをサポートできます。

このワークショップでは、[**otlphttp**](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) Exporterを使用します。OpenTelemetry Protocol（OTLP）は、テレメトリデータを送信するためのベンダーニュートラルな標準化されたプロトコルです。OTLP Exporterは、OTLPプロトコルを実装するサーバーにデータを送信します。OTLP Exporterは [**gRPC**](https://grpc.io/) と [**HTTP**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)/[**JSON**](https://www.json.org/json-en.html) の両方のプロトコルをサポートしています。

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
