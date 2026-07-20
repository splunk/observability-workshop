---
title: OpenTelemetryでオブザーバビリティをクラウドネイティブにする
linkTitle: OpenTelemetry Collectorの概念
weight: 1
description: OpenTelemetry Collectorの概念と、Splunk Observability Cloudにデータを送信するための使用方法を学びます。
authors: ["Robert Castley"]
time: 1 hour
---

## 概要

OpenTelemetryを使い始める組織は、最初にオブザーバビリティバックエンドに直接データを送信することから始めるかもしれません。これは初期テストには有効ですが、オブザーバビリティアーキテクチャの一部としてOpenTelemetry Collectorを使用することで多くのメリットが得られ、本番環境へのデプロイでは推奨されます。

このワークショップでは、OpenTelemetry Collectorの使用に焦点を当て、Splunk Observability Cloudで使用するためのReceiver、Processor、Exporterの設定の基礎から始めます。参加者は初心者から、分散プラットフォームのビジネスオブザーバビリティニーズを解決するためのカスタムコンポーネントを追加できるレベルまで進みます。

### Ninjaセクション

ワークショップ全体を通して、展開可能な {{% badge style=primary icon=star %}}**Ninja** セクション{{% /badge %}} があります。これらはより実践的で、ワークショップ内または自分の時間で探索できる、さらに詳しい技術的内容を含みます。

これらのセクションの内容は、OpenTelemetryプロジェクトの頻繁な開発により古くなる場合があることに注意してください。詳細が同期していない場合にはリンクが提供されます。更新が必要な箇所を見つけた場合はお知らせください。

{{% expand title="{{% badge style=primary icon=star %}}**Ninja:** Test Me!{{% /badge %}}" %}}
**このワークショップを完了すると、あなたは正式にOpenTelemetry Collector Ninjaになります！**
{{% /expand %}}

## 対象者

このインタラクティブなワークショップは、OpenTelemetry Collectorのアーキテクチャとデプロイについてさらに学びたい開発者やシステム管理者を対象としています。

## 前提条件

- データ収集の基本的な理解があること
- コマンドラインとvim/viの経験があること
- Ubuntu 20.04 LTSまたは22.04 LTSが動作するインスタンス/ホスト/VMがあること
  - 最小要件はAWS/EC2 t2.micro（1 CPU、1GB RAM、8GBストレージ）

## 学習目標

このワークショップを終了すると、参加者は以下のことができるようになります

- OpenTelemetryのコンポーネントを理解する
- Receiver、Processor、Exporterを使用してデータを収集・分析する
- OpenTelemetryを使用するメリットを理解する
- ビジネスニーズを解決するためのカスタムコンポーネントを構築する

## OpenTelemetryアーキテクチャ

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
