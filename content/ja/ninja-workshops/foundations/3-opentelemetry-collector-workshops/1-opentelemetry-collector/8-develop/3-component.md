---
title: OpenTelemetry Collector Development
linkTitle: 8.3 コンポーネントの復習
weight: 11
---

## コンポーネントの復習

Jenkins からメトリクスを取得するために必要なコンポーネントの種類について、これまでの内容を振り返ります。

{{% tabs %}}
{{% tab title="Extension" %}}
extension が解決するビジネスユースケースは以下のとおりです。

1. ランタイム設定が必要な共有機能を提供する
1. Collector のランタイムを観測する間接的な手助けをする

詳細は [**Extensions Overview**](../2-extensions) を参照してください。
{{% /tab %}}
{{% tab title="Receiver" %}}
receiver が解決するビジネスユースケースは以下のとおりです。

- リモートソースからデータを取得する
- リモートソースからデータを受信する

これは一般的に _pull_ 型と _push_ 型のデータ収集と呼ばれ、詳細は [Receiver Overview](../3-receivers) で確認できます。
{{% /tab %}}
{{% tab title="Processor" %}}
processor が解決するビジネスユースケースは以下のとおりです。

- データ、フィールド、または値の追加や削除
- データを観測し、判断を行う
- バッファリング、キューイング、並び替え

ここで覚えておくべき点は、processor を流れるデータタイプは、下流のコンポーネントに同じデータタイプを転送する必要があるということです。詳細は [Processor Overview](../4-processors) を読んでください。

{{% /tab %}}
{{% tab title="Exporter" %}}
exporter が解決するビジネスユースケースは以下のとおりです。

- ツール、サービス、またはストレージにデータを送信する

OpenTelemetry Collector は「バックエンド」やオールインワンの可観測性スイートになることを目指していません。むしろ、OpenTelemetry が当初から掲げてきた原則、つまり「すべての人にベンダーニュートラルな可観測性を」という理念を守ることを重視しています。
詳細を改めて確認するには、[**Exporter Overview**](../5-exporters) を読んでください。

{{% /tab %}}
{{% tab title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Connectors{{% /badge %}}"  %}}

これは、Collector に比較的最近追加されたコンポーネントタイプであるため、本ワークショップでは触れていなかったものです。connector を理解する最良の方法は、異なるテレメトリータイプやパイプラインをまたいで使用できる processor のようなものだと考えることです。つまり、connector はログとしてデータを受け取ってメトリクスとして出力したり、あるパイプラインからメトリクスを受け取って観測したデータに基づくメトリクスを提供したりできます。

connector が解決するビジネスケースは以下のとおりです。

- 異なるテレメトリータイプ間の変換
  - logs から metrics へ
  - traces から metrics へ
  - metrics から logs へ
- 受信データを観測し、独自のデータを生成
  - メトリクスを受け取って、そのデータの分析メトリクスを生成する

[Processor Overview](../4-processors) の **Ninja** セクションで簡単な概要を紹介していますので、新しい connector コンポーネントの追加状況についてもプロジェクトを必ず確認してください。
{{% /tab %}}
{{% /tabs %}}

これらのコンポーネント概要から、Jenkins 用には pull 型の receiver を開発することが明らかです。
