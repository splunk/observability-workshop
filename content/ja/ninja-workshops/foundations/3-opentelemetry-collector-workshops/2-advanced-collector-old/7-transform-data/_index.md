---
title: 7. Transform Data
linkTitle: 7. Transform Data
time: 10 minutes
weight: 9
---

[**Transform Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) は、ログ、メトリクス、トレースといったテレメトリーデータがパイプラインを流れる際に、それらを変更できるプロセッサーです。**OpenTelemetry Transformation Language (OTTL)** を使用することで、アプリケーションコードに手を加えることなく、データのフィルタリング、エンリッチ、変換をリアルタイムに実行できます。

この演習では、`agent.yaml` を更新して、以下の処理を行う **Transform Processor** を追加します。

- ログのリソース属性を **Filter** します。
- JSON 形式の構造化ログデータを属性に **Parse** します。
- ログメッセージの本文に基づいてログの重要度レベルを **Set** します。

これまでのログでは、`SeverityText` や `SeverityNumber` といったフィールドが未定義になっていることに気づいたかもしれません。これは `filelog` レシーバーで一般的な動作です。しかし、重要度はログ本文の中に埋め込まれています。

```text
<snip>
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
</snip>
```

ログには、JSON でエンコードされた構造化データがログ本文の中に含まれていることがよくあります。これらのフィールドを属性として抽出することで、インデックス作成、フィルタリング、クエリの効率が向上します。下流のシステムで JSON を手動でパースする代わりに、OTTL を使えばテレメトリーパイプラインのレベルで自動的に変換できます。

{{% notice title="Exercise" style="green" icon="running" %}}

- `[WORKSHOP]` ディレクトリ内に、`7-transform-data` という名前の新しいサブディレクトリを作成します。
- 次に、`6-sensitve-data` ディレクトリから `*.yaml` を `7-transform-data` にコピーします。

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `[WORKSHOP]/7-transform-data` ディレクトリに変更してください。**

更新後のディレクトリ構成は次のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
