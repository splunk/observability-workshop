---
title: OpenTelemetry でオブザーバビリティをクラウドネイティブにする
linkTitle: OpenTelemetry Collector の概念
weight: 1
description: OpenTelemetry Collector の概念と、Splunk Observability Cloud にデータを送信するための使用方法を学びます。
authors: ["Robert Castley"]
time: 1 hour
---

## 概要

OpenTelemetry を始めたばかりの組織は、オブザーバビリティバックエンドにデータを直接送信することから始めるかもしれません。これは初期テストには適していますが、オブザーバビリティアーキテクチャの一部として OpenTelemetry Collector を使用することで多くのメリットが得られ、本番環境へのデプロイメントには推奨されています。

このワークショップでは、OpenTelemetry Collector の使用に焦点を当て、Splunk Observability Cloud で使用するための receivers、processors、exporters の設定の基礎から始めます。参加者は初心者から、分散プラットフォームのビジネスオブザーバビリティニーズを解決するためのカスタムコンポーネントを追加できるレベルまで到達します。

### Ninja セクション

ワークショップを通じて、展開可能な {{% badge style=primary icon=star %}}**Ninja** セクション{{% /badge %}} があります。これらはより実践的で、ワークショップ内または自分の時間に探索できる詳細な技術情報を提供します。

これらのセクションの内容は、OpenTelemetry プロジェクトの頻繁な開発により古くなる可能性があることにご注意ください。詳細が同期していない場合はリンクが提供されます。更新が必要な箇所を見つけた場合はお知らせください。

{{% expand title="{{% badge style=primary icon=star %}}**Ninja:** Test Me!{{% /badge %}}" %}}
**このワークショップを完了すると、正式に OpenTelemetry Collector Ninja になります！**
{{% /expand %}}

## 対象者

このインタラクティブなワークショップは、OpenTelemetry Collector のアーキテクチャとデプロイメントについてさらに学びたい開発者およびシステム管理者を対象としています。

## 前提条件

- データ収集の基本的な理解があること
- コマンドラインおよび vim/vi の経験があること
- Ubuntu 20.04 LTS または 22.04 LTS を実行するインスタンス/ホスト/VM があること
  - 最小要件は AWS/EC2 t2.micro（1 CPU、1GB RAM、8GB ストレージ）です

## 学習目標

このワークショップの終了時には、参加者は以下のことができるようになります

- OpenTelemetry のコンポーネントを理解する
- receivers、processors、exporters を使用してデータを収集・分析する
- OpenTelemetry を使用するメリットを特定する
- ビジネスニーズを解決するためのカスタムコンポーネントを構築する

## OpenTelemetry アーキテクチャ

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
