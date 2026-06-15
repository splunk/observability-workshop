---
title: 6. Routing Data
linkTitle: 6. Routing Data
time: 10 minutes
weight: 8
---

OpenTelemetry の [**Routing Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) は、特定の条件に基づいてデータ（`traces`、`metrics`、または `logs`）を異なるパイプラインや宛先に振り分けることができる強力な機能です。これは、テレメトリデータのサブセットに対して異なる処理やエクスポートロジックを適用したい場合に特に便利です。

例えば、*本番環境* のデータをあるエクスポーターに送信し、*テスト* や *開発環境* のデータを別のエクスポーターに振り分けたい場合があります。同様に、サービス名、環境、スパン名などの属性に基づいて特定のスパンをルーティングし、カスタムの処理やストレージロジックを適用することもできます。

{{% exercise title="`6-routing-data` ディレクトリのセットアップ" %}}

> [!IMPORTANT]
> ***すべての* ターミナルウィンドウを `6-routing-data` ディレクトリに変更し、`clear` コマンドを実行してください。**

`5-transform-data` ディレクトリから `*.yaml` を `6-routing-data` にコピーします。更新後のディレクトリ構造は次のようになります:

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /exercise %}}

次に、routing connector と関連するパイプラインを設定します。
