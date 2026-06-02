---
title: OpenTelemetry Collector Exporters
linkTitle: 5. Exporters
weight: 5
---

エクスポーターは、push 型または pull 型のいずれかで動作し、データを 1 つ以上のバックエンドや宛先へ送信する仕組みです。エクスポーターは 1 つまたは複数のデータソースに対応します。

このワークショップでは、[**otlphttp**](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) エクスポーターを使用します。OpenTelemetry Protocol (OTLP) は、テレメトリデータを送信するためのベンダー中立で標準化されたプロトコルです。OTLP エクスポーターは、OTLP プロトコルを実装したサーバーへデータを送信します。OTLP エクスポーターは [**gRPC**](https://grpc.io/) と [**HTTP**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)/[**JSON**](https://www.json.org/json-en.html) の両方のプロトコルをサポートしています。

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
