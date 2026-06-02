---
title: 3. スパンのドロップ
linkTitle: 3. スパンのドロップ
time: 5 minutes
weight: 5
---

このセクションでは、[**Filter Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md) を使用して、特定の条件に基づいてスパンを選択的にドロップする方法を確認します。

具体的には、スパン名に基づいてトレースをドロップします。これは、ヘルスチェックや内部通信トレースなど、不要なスパンをフィルタリングするためによく使用されます。今回のケースでは、`"/_healthz"` を含むスパンをフィルタリングします。これは通常、ヘルスチェックリクエストに関連しており、一般的に非常に「**ノイジー**」です。

{{% exercise title="`3-dropping-spans` ディレクトリのセットアップ" %}}

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `3-dropping-spans` ディレクトリに変更し、`clear` コマンドを実行してください。**

`2-building-resilience` ディレクトリから `*.yaml` を `3-dropping-spans` にコピーします。更新後のディレクトリ構造は次のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /exercise %}}

次に、**filter processor** と関連するパイプラインを設定します。
