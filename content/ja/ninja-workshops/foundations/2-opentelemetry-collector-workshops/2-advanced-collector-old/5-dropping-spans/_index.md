---
title: 5. Spanのドロップ
linkTitle: 5. Spanのドロップ
time: 10 minutes
weight: 7
---

このセクションでは、[**Filter Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md) を使用して、特定の条件に基づいてSpanを選択的にドロップする方法を説明します。

具体的には、Span名に基づいてトレースをドロップします。これは、ヘルスチェックや内部通信トレースなどの不要なSpanをフィルタリングするためによく使用されます。ここでは、名前が `"/_healthz"` のSpanをフィルタリングします。これはヘルスチェックリクエストに関連するもので、通常非常に **「ノイジー」** です。

{{% notice title="Exercise" style="green" icon="running" %}}

- `[WORKSHOP]` ディレクトリ内に、`5-dropping-spans` という名前の新しいサブディレクトリを作成します。
- 次に、`4-resilience` ディレクトリから `*.yaml` を `5-dropping-spans` にコピーします。

> [!IMPORTANT]
> **すべてのターミナルウィンドウを `[WORKSHOP]/5-dropping-spans` ディレクトリに変更してください。**

更新されたディレクトリ構造は以下のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}

次に、**filter processor** と対応するパイプラインを設定します。
