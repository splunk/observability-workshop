---
title: 5. データの変換
linkTitle: 5. データの変換
time: 10 minutes
weight: 7
---

[**Transform Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) を使用すると、パイプラインを流れるテレメトリデータ（ログ、メトリクス、トレース）を変更できます。 **OpenTelemetry Transformation Language（OTTL）** を使用して、アプリケーションコードを変更することなく、データのフィルタリング、エンリッチメント、変換をリアルタイムで行えます。

この演習では、`gateway.yaml`を更新して、以下を行う **Transform Processor** を追加します。

- ログリソース属性の **フィルタリング**
- JSON構造化ログデータの属性への **パース**
- ログメッセージ本文に基づくログ重大度レベルの **設定**

以前のログで`SeverityText`や`SeverityNumber`などのフィールドが未定義であることに気づいたかもしれません。これは`filelog` Receiverの典型的な動作です。しかし、重大度はログ本文に埋め込まれています。例えば以下のようになっています。

```text
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
```

ログには、ログ本文内にJSONとしてエンコードされた構造化データが含まれていることがよくあります。これらのフィールドを属性として抽出することで、インデックス作成、フィルタリング、クエリの効率が向上します。下流のシステムで手動でJSONを解析する代わりに、OTTLを使用してテレメトリパイプラインレベルで自動的に変換を行うことができます。

{{% exercise title="`5-transform-data` ディレクトリのセットアップ" %}}

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウで `5-transform-data` ディレクトリに移動し、`clear` コマンドを実行してください。**

`4-sensitve-data`ディレクトリから`5-transform-data`に`*.yaml`をコピーします。更新後のディレクトリ構造は以下のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /exercise %}}
