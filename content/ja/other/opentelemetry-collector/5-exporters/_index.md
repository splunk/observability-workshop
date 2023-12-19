---
title: OpenTelemetry Collector エクスポーター
linkTitle: 5. エクスポーター
weight: 5
---

エクスポーターは、プッシュまたはプルベースであり、一つ以上のバックエンド/デスティネーションにデータを送信する方法です。エクスポーターは、一つまたは複数のデータソースをサポートすることがあります。

このワークショップでは、[**otlphttp**](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) エクスポーターを使用します。OpenTelemetry Protocol (OTLP) は、テレメトリーデータを伝送するためのベンダーニュートラルで標準化されたプロトコルです。OTLP エクスポーターは、OTLP プロトコルを実装するサーバーにデータを送信します。OTLP エクスポーターは、[**gRPC**](https://grpc.io/) および [**HTTP**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)/[**JSON**](https://www.json.org/json-en.html) プロトコルの両方をサポートします。


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
