---
title: 3. Spanのドロップ
linkTitle: 3. Spanのドロップ
time: 5 minutes
weight: 5
---

このセクションでは、[**Filter Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md) を使用して、特定の条件に基づいてSpanを選択的にドロップする方法を説明します。

具体的には、Span名に基づいてトレースをドロップします。これは、ヘルスチェックや内部通信トレースなどの不要なSpanをフィルタリングするために一般的に使用されます。ここでは、`"/_healthz"` を含むSpanをフィルタリングします。これはヘルスチェックリクエストに関連するもので、通常非常に「**ノイジー**」です。

{{% exercise title="`3-dropping-spans` ディレクトリのセットアップ" %}}

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `3-dropping-spans` ディレクトリに変更し、`clear` コマンドを実行してください。**

`2-building-resilience` ディレクトリから `3-dropping-spans` に `*.yaml` をコピーします。更新後のディレクトリ構造は以下のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /exercise %}}

次に、**filter processor** と対応するパイプラインを設定します。
