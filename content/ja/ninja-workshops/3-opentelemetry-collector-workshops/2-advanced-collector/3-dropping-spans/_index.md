---
title: 3. Spanのドロップ
linkTitle: 3. Spanのドロップ
time: 5 minutes
weight: 5
---

このセクションでは、[**Filter Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md) を使用して、特定の条件に基づいてSpanを選択的にドロップする方法を説明します。

具体的には、Span名に基づいてトレースをドロップします。これは、ヘルスチェックや内部通信トレースなどの不要なSpanをフィルタリングするためによく使用されます。今回は、ヘルスチェックリクエストに関連付けられることが多く、通常は非常に「**ノイジー**」な `"/_healthz"` を含むSpanをフィルタリングします。

{{% notice title="Exercise" style="green" icon="running" %}}

> [!IMPORTANT]
> **すべてのターミナルウィンドウを `3-dropping-spans` ディレクトリに移動し、`clear` コマンドを実行してください。**

`2-building-resilience` ディレクトリから `*.yaml` を `3-dropping-spans` にコピーします。更新後のディレクトリ構造は次のようになります：

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}

次に、**filter processor** と対応するパイプラインを設定します。
