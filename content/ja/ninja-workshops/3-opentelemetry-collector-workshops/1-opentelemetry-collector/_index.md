---
title: OpenTelemetry でオブザーバビリティをクラウドネイティブに
linkTitle: OpenTelemetry Collector の基本概念
weight: 1
description: OpenTelemetry Collector の概念と、Splunk Observability Cloud へデータを送信する方法を学びます。
authors: ["Robert Castley"]
time: 1 hour
---

## 概要

OpenTelemetry を始めたばかりの組織では、まずオブザーバビリティバックエンドに直接データを送信することから始めることが多いでしょう。これは初期テストには有効ですが、OpenTelemetry Collector をオブザーバビリティアーキテクチャの一部として使用することで多くのメリットがあり、本番環境へのデプロイには推奨されています。

このワークショップでは、OpenTelemetry Collector の使用に焦点を当て、Splunk Observability Cloud で使用するための Receiver、Processor、Exporter の設定の基本から始めます。参加者は初心者から、分散プラットフォームのビジネスオブザーバビリティニーズを解決するためのカスタムコンポーネントを追加できるレベルまで到達します。

### Ninja セクション

ワークショップを通じて、展開可能な {{% badge style=primary icon=user-ninja %}}**Ninja** セクション{{% /badge %}} があります。これらはより実践的で、ワークショップ中または自分の時間に探求できる詳細な技術情報を提供します。

OpenTelemetry プロジェクトは頻繁に開発が行われているため、これらのセクションの内容が古くなる可能性があることに注意してください。詳細が同期していない場合はリンクが提供されます。更新が必要な箇所を見つけた場合はお知らせください。

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** テストしてみよう！{{% /badge %}}" %}}
**このワークショップを完了すると、正式に OpenTelemetry Collector Ninja になれます！**
{{% /expand %}}

---

## 対象者

このインタラクティブなワークショップは、OpenTelemetry Collector のアーキテクチャとデプロイについて詳しく学びたい開発者およびシステム管理者を対象としています。

## 前提条件

- データ収集の基本的な理解があること
- コマンドラインと vim/vi の経験があること
- Ubuntu 20.04 LTS または 22.04 LTS を実行しているインスタンス/ホスト/VM があること
  - 最小要件は AWS/EC2 t2.micro（1 CPU、1GB RAM、8GB ストレージ）です

## 学習目標

このワークショップを終えると、参加者は以下ができるようになります

- OpenTelemetry のコンポーネントを理解する
- Receiver、Processor、Exporter を使用してデータを収集・分析する
- OpenTelemetry を使用するメリットを理解する
- ビジネスニーズを解決するカスタムコンポーネントを構築する

## OpenTelemetry アーキテクチャ

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
