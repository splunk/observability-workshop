---
title: 6. データのルーティング
linkTitle: 6. データのルーティング
time: 10 minutes
weight: 8
---

OpenTelemetry の [**Routing Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) は、特定の条件に基づいてデータ（`traces`、`metrics`、`logs`）を異なるパイプラインや宛先に振り分けることができる強力な機能です。これは、テレメトリーデータのサブセットに対して異なる処理やエクスポートロジックを適用したい場合に特に役立ちます。

例えば、*production* のデータを 1 つのエクスポーターに送信しつつ、*test* や *development* のデータを別のエクスポーターに振り分けることができます。同様に、サービス名、環境、スパン名などの属性に基づいて特定のスパンをルーティングし、カスタムの処理や保存ロジックを適用することも可能です。

{{% exercise title="`6-routing-data` ディレクトリのセットアップ" %}}

> [!IMPORTANT]
> ***すべての* ターミナルウィンドウで `6-routing-data` ディレクトリに移動し、`clear` コマンドを実行してください。**

`5-transform-data` ディレクトリから `*.yaml` を `6-routing-data` にコピーします。更新されたディレクトリ構造は次のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /exercise %}}

次に、routing connector とそれぞれのパイプラインを設定していきます。
