---
title: 5. スパンの削除
linkTitle: 5. スパンの削除
time: 10 minutes
weight: 7
---

このセクションでは、[**Filter Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md) を使用して、特定の条件に基づいてスパンを選択的に削除する方法について説明します。

具体的には、スパン名に基づいてトレースを削除します。これは、ヘルスチェックや内部通信トレースなどの不要なスパンを除外するためによく使用されます。今回の例では、ヘルスチェックリクエストに関連付けられることが多く、通常は非常に「**ノイジー**」であるスパン名 `"/_healthz"` を除外します。

{{% notice title="演習" style="green" icon="running" %}}

- `[WORKSHOP]` ディレクトリ内に、`5-dropping-spans` という新しいサブディレクトリを作成します。
- 次に、`4-resilience` ディレクトリから `*.yaml` を `5-dropping-spans` にコピーします。

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `[WORKSHOP]/5-dropping-spans` ディレクトリに変更してください。**

更新後のディレクトリ構造は以下のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}

次に、**filter processor** とそれぞれのパイプラインを設定します。
