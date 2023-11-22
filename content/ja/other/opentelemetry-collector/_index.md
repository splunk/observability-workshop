---
title: OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する
linkTitle: OpenTelemetry Collector
weight: 10
alwaysopen: false
description: OpenTelemetry Collectorのコンセプトを学び、Splunk Observability Cloudにデータを送信する方法を理解しましょう。
---

## 概要

OpenTelemetry を使い始める場合は、バックエンドに直接データを送ることから始めるかもしれません。最初のステップとしてはよいですが、OpenTelemetry Collector をオブザーバビリティのアーキテクチャとして使用するのは多くの利点があり、本番環境では Collector を使ったデプロイを推奨しています。

このワークショップでは、OpenTelemetry Collector を使用することに焦点を当て、Splunk Observability Cloud で使用するためのレシーバー、プロセッサー、エクスポーターを定義し、実際にテレメトリデータを送信するためのパイプラインを設定することで、環境に合わせて Collector を活用を学びます。また、分散プラットフォームのビジネスニーズに対応するための、カスタムコンポーネントを追加できるようになるまでの道のりを進むことになります。

### Ninja セクション

ワークショップの途中には、展開できる {{% badge style=primary icon=user-ninja %}}Ninja セクション{{% /badge %}} があります。これらはより実践的で、ワークショップ中、もしくは自分の時間を使って、さらに技術的な詳細に取り組むことができます。

OpenTelemetry プロジェクトは頻繁に開発されているため、Ninjaセクションの内容が古くなる可能性があることに注意してください。コンテンツが古い場合には更新のリクエストを出すこともできますので、必要なものを見つけた場合はお知らせください。

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** をテストして！{{% /badge %}}" %}}
**このワークショップを完了すると、正式に OpenTelemetry Collector ニンジャになります！**
{{% /expand %}}

---

## 対象者

このワークショップは、OpenTelemetry Collector のアーキテクチャとデプロイメントについてさらに学びたいと考えている開発者やシステム管理者を対象としています。

## 前提条件
- データ収集に関する基本的な理解
- コマンドラインとvim/viの経験
- Ubuntu 20.04 LTSまたは22.04 LTSが稼働するインスタンス/ホスト/VM
  - 最小要件はAWS/EC2 t2.micro（1 CPU、1GB RAM、8GBストレージ）

## 学習目標

このセッションの終わりまでに、参加者は以下を行うことができるようになります：

- OpenTelemetry のコンポーネントを理解する
- レシーバー、プロセッサー、エクスポーターを使用してデータを収集・分析する
- OpenTelemetry を使用する利点を特定する
- 自分たちのビジネスニーズに対応するカスタムコンポーネントを構築する

## OpenTelemetry のアーキテクチャー

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
