---
title: OpenTelemetry Collector レシーバー
linkTitle: 3. レシーバー
weight: 3
---

レシーバーワークショップへようこそ！OpenTelemetry Collectorのデータパイプラインのスタート地点です。さあ、始めましょう。

レシーバーはデータをCollectorに取り込む方法で、プッシュベースとプルベースのものがあります。レシーバーは1つ以上のデータソースをサポートします。一般的に、レシーバーは指定されたフォーマットでデータを受け入れ、内部フォーマットに変換し、該当するパイプラインで定義されたプロセッサやエクスポータにデータを渡します。

プッシュまたはプルベースのレシーバは、データをCollectorに取り込む方法です。レシーバは1つまたは複数のデータソースをサポートします。通常、レシーバは指定されたフォーマットでデータを受け入れ、内部フォーマットに変換し、該当するパイプラインで定義されたプロセッサーやエクスポーターにデータを渡します。

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
    subgraph Receivers
    A[OTLP]--> M(Receivers)
    B[JAEGER]--> M(Receivers)
    C[Prometheus]--> M(Receivers)
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
