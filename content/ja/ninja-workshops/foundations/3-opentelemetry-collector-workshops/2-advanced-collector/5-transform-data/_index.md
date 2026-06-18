---
title: 5. Transform Data
linkTitle: 5. Transform Data
time: 10 minutes
weight: 7
---

[**Transform Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) を使用すると、パイプラインを流れるテレメトリデータ（ログ、メトリクス、トレース）を変更できます。**OpenTelemetry Transformation Language (OTTL)** を使用することで、アプリケーションコードを変更せずにデータのフィルタリング、エンリッチメント、変換をリアルタイムで行えます。

この演習では、`gateway.yaml` を更新して、以下の処理を行う **Transform Processor** を追加します

- ログリソース属性の**フィルタリング**
- JSON 構造化ログデータの属性への**パース**
- ログメッセージ本文に基づくログ重大度レベルの**設定**

前のログで `SeverityText` や `SeverityNumber` が未定義だったことにお気づきかもしれません。これは `filelog` レシーバーの典型的な動作です。ただし、重大度はログ本文内に埋め込まれています。例

```text
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
```

ログには、ログ本文内に JSON としてエンコードされた構造化データが含まれていることがよくあります。これらのフィールドを属性として抽出することで、インデックス作成、フィルタリング、クエリの効率が向上します。ダウンストリームシステムで手動で JSON をパースする代わりに、OTTL を使用するとテレメトリパイプラインレベルで自動変換が可能になります。

{{% exercise title="`5-transform-data` ディレクトリのセットアップ" %}}

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `5-transform-data` ディレクトリに移動し、`clear` コマンドを実行してください。**

`4-sensitve-data` ディレクトリから `*.yaml` を `5-transform-data` にコピーします。更新後のディレクトリ構造は次のようになります

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /exercise %}}
