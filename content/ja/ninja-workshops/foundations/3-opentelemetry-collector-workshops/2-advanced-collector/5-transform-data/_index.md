---
title: 5. Transform Data
linkTitle: 5. Transform Data
time: 10 minutes
weight: 7
---

[**Transform Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) を使うと、ログ、メトリクス、トレースなどのテレメトリーデータがパイプラインを流れる際に変更できます。**OpenTelemetry Transformation Language (OTTL)** を使用することで、アプリケーションコードに触れることなく、データのフィルタリング、エンリッチメント、変換をその場で実行できます。

この演習では、`gateway.yaml` を更新して **Transform Processor** を組み込み、以下の処理を行います。

- ログのリソース属性を**フィルタリング**します。
- JSON 構造化ログデータを**パース**して属性に変換します。
- ログメッセージ本文に基づいてログのシビリティレベルを**設定**します。

これまでのログでは、`SeverityText` や `SeverityNumber` といったフィールドが未定義になっていることに気づいたかもしれません。これは `filelog` レシーバーの典型的な挙動です。ただし、シビリティはログ本文の中に埋め込まれています。例えば次のような形式です。

```text
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
```

ログには、ログ本文内に JSON としてエンコードされた構造化データが含まれていることがよくあります。これらのフィールドを属性として抽出することで、インデックス作成、フィルタリング、クエリの効率が向上します。下流システムで JSON を手作業でパースする代わりに、OTTL を使えばテレメトリーパイプラインレベルで自動的に変換できます。

{{% exercise title="Set up the `5-transform-data` directory" %}}

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウで `5-transform-data` ディレクトリに移動し、`clear` コマンドを実行してください。**

`4-sensitve-data` ディレクトリから `*.yaml` を `5-transform-data` にコピーします。更新後のディレクトリ構造は次のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /exercise %}}
