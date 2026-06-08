---
title: OpenTelemetry Collector エクスポーター
linkTitle: 5. Exporters
weight: 5
---

エクスポーターは、プッシュ型またはプル型があり、1つ以上のバックエンド/宛先にデータを送信する方法です。エクスポーターは1つ以上のデータソースをサポートする場合があります。

このワークショップでは、[**otlphttp**](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) エクスポーターを使用します。OpenTelemetry Protocol (OTLP) は、テレメトリデータを送信するためのベンダー中立で標準化されたプロトコルです。OTLP エクスポーターは、OTLP プロトコルを実装するサーバーにデータを送信します。OTLP エクスポーターは、[**gRPC**](https://grpc.io/) と [**HTTP**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)/[**JSON**](https://www.json.org/json-en.html) の両方のプロトコルをサポートしています。

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
