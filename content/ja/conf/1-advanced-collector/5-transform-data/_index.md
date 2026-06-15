---
title: 5. Transform Data
linkTitle: 5. Transform Data
time: 10 minutes
weight: 7
---

[**Transform Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) を使用すると、パイプラインを流れるテレメトリデータ（ログ、メトリクス、トレース）を変更できます。**OpenTelemetry Transformation Language (OTTL)** を使用することで、アプリケーションコードを変更することなく、データのフィルタリング、エンリッチメント、変換をリアルタイムで行うことができます。

この演習では、`gateway.yaml` を更新して、以下を行う **Transform Processor** を追加します

- ログリソース属性の**フィルタリング**
- JSON 構造化ログデータの属性への**パース**
- ログメッセージ本文に基づくログ重大度レベルの**設定**

以前のログで `SeverityText` や `SeverityNumber` などのフィールドが未定義であったことにお気づきかもしれません。これは `filelog` レシーバーの典型的な動作です。しかし、重大度はログ本文に埋め込まれています。例

```text
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
```

ログには、ログ本文内に JSON としてエンコードされた構造化データが含まれていることがよくあります。これらのフィールドを属性として抽出することで、インデックス作成、フィルタリング、クエリの効率が向上します。ダウンストリームシステムで手動で JSON をパースする代わりに、OTTL を使用するとテレメトリパイプラインレベルで自動変換が可能になります。

{{% notice title="演習" style="green" icon="running" %}}

> [!IMPORTANT]
> **_すべての_ターミナルウィンドウを `5-transform-data` ディレクトリに変更し、`clear` コマンドを実行してください。**

`4-sensitve-data` ディレクトリから `*.yaml` を `5-transform-data` にコピーしてください。更新後のディレクトリ構造は以下のようになります

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
