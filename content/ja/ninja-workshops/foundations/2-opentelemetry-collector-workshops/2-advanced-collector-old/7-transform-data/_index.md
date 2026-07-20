---
title: 7. データの変換
linkTitle: 7. データの変換
time: 10 minutes
weight: 9
---

[**Transform Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) を使用すると、パイプラインを流れるテレメトリデータ（ログ、メトリクス、トレース）を変更できます。**OpenTelemetry Transformation Language (OTTL)** を使用して、アプリケーションコードを変更することなく、データのフィルタリング、エンリッチメント、変換をリアルタイムで行うことができます。

この演習では、`agent.yaml` を更新して、以下を行う **Transform Processor** を追加します。

- ログリソース属性の **フィルタリング**
- JSON構造化ログデータの属性への **パース**
- ログメッセージ本文に基づくログ重大度レベルの **設定**

以前のログで、`SeverityText`や`SeverityNumber`のようなフィールドが未定義であったことに気づいたかもしれません。これは`filelog` Receiverの典型的な動作です。しかし、重大度はログ本文に埋め込まれています。

```text
<snip>
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
</snip>
```

ログにはJSON形式の構造化データがログ本文に含まれていることがよくあります。これらのフィールドを属性として抽出することで、インデックス作成、フィルタリング、クエリの効率が向上します。下流システムでJSONを手動でパースする代わりに、OTTLを使用してテレメトリパイプラインレベルで自動変換を行うことができます。

{{% notice title="演習" style="green" icon="running" %}}

- `[WORKSHOP]` ディレクトリ内に、`7-transform-data` という名前の新しいサブディレクトリを作成します。
- 次に、`6-sensitve-data` ディレクトリから `*.yaml` を `7-transform-data` にコピーします。

> [!IMPORTANT]
> **すべてのターミナルウィンドウを `[WORKSHOP]/7-transform-data` ディレクトリに変更してください。**

更新後のディレクトリ構造は以下のようになります。

```text { title="更新後のディレクトリ構造" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
