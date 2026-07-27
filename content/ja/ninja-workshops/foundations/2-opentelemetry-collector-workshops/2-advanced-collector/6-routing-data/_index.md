---
title: 6. Routing Data
linkTitle: 6. Routing Data
time: 10 minutes
weight: 8
---

OpenTelemetry の [**Routing Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) は、特定の条件に基づいてデータ（`traces`、`metrics`、または `logs`）を異なるパイプライン/宛先に振り分けることができる強力な機能です。これは、テレメトリデータのサブセットに異なる処理やエクスポートロジックを適用したい場合に特に有用です。

例えば、*本番環境* のデータを1つのエクスポーターに送信し、*テスト* や *開発* のデータを別のエクスポーターに振り分けることができます。同様に、サービス名、環境、スパン名などの属性に基づいて特定のスパンをルーティングし、カスタムの処理やストレージロジックを適用することもできます。

{{% notice title="Exercise" style="green" icon="running" %}}

> [!IMPORTANT]
> **すべてのターミナルウィンドウを `6-routing-data` ディレクトリに移動し、`clear` コマンドを実行してください。**

`5-transform-data` ディレクトリから `*.yaml` を `6-routing-data` にコピーします。更新後のディレクトリ構造は次のようになります

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}

次に、Routing Connector とそれぞれのパイプラインを設定します。
