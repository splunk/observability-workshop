---
title: OpenTelemetry でオブザーバビリティをクラウドネイティブに
linkTitle: OpenTelemetry Collector の概念
weight: 1
description: OpenTelemetry Collector の概念と、Splunk Observability Cloud にデータを送信するための使い方を学びます。
authors: ["Robert Castley"]
time: 1 hour
---

## 概要

OpenTelemetry を使い始める組織は、まずオブザーバビリティバックエンドにデータを直接送信することから着手するかもしれません。これは初期テストには適していますが、オブザーバビリティアーキテクチャの一部として OpenTelemetry collector を利用すると多くのメリットがあり、本番環境のデプロイメントには推奨されるアプローチです。

このワークショップでは、OpenTelemetry collector の利用に焦点を当て、Splunk Observability Cloud で利用するための receivers、processors、exporters の設定の基礎から始めます。このワークショップを通じて、参加者は初心者から、分散プラットフォームのビジネス上のオブザーバビリティニーズを解決するためにカスタムコンポーネントを追加できるレベルへと成長することができます。

### Ninja セクション

ワークショップ全体を通じて、展開可能な {{% badge style=primary icon=user-ninja %}}**Ninja** セクション{{% /badge %}}が用意されています。これらはより実践的で、さらに踏み込んだ技術的な詳細について解説しており、ワークショップ中またはご自身のお時間に合わせて探求していただけます。

OpenTelemetry プロジェクトは頻繁に開発が進められているため、これらのセクションの内容は古くなっている可能性がある点にご注意ください。詳細が同期していない場合に備えてリンクを提供しますので、更新が必要な箇所を見つけた場合はお知らせください。

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** 自分を試そう！{{% /badge %}}" %}}
**このワークショップを完了すれば、あなたは正式に OpenTelemetry Collector の Ninja です！**
{{% /expand %}}

---

## 対象者

このインタラクティブなワークショップは、OpenTelemetry Collector のアーキテクチャとデプロイメントについてさらに学びたい開発者およびシステム管理者を対象としています。

## 前提条件

- 参加者はデータ収集について基本的な理解があること
- コマンドラインおよび vim/vi の経験があること
- Ubuntu 20.04 LTS または 22.04 LTS が動作するインスタンス/ホスト/VM
  - 最小要件は AWS/EC2 t2.micro（1 CPU、1GB RAM、8GB ストレージ）

## 学習目標

このワークショップを終えるまでに、参加者は以下のことができるようになります：

- OpenTelemetry のコンポーネントを理解する
- receivers、processors、exporters を使用してデータを収集・分析する
- OpenTelemetry を使用するメリットを把握する
- ビジネスニーズを解決するためのカスタムコンポーネントを構築する

## OpenTelemetry のアーキテクチャ

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
