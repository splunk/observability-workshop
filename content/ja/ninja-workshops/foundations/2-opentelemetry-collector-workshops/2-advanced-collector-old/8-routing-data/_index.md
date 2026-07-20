---
title: 8. Routing Data
linkTitle: 8. Routing Data
time: 10 minutes
weight: 10
---

OpenTelemetryの [**Routing Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) は、特定の条件に基づいてデータ（`traces`、`metrics`、`logs`）を異なるパイプラインに振り分けることができる強力な機能です。これは、テレメトリデータのサブセットに対して異なる処理やエクスポートロジックを適用したい場合に特に有用です。

例えば、*本番* データを一つのExporterに送信し、*テスト* や *開発* データを別のExporterに振り分けることができます。同様に、サービス名、環境、Span名などの属性に基づいて特定のSpanをルーティングし、カスタム処理やストレージロジックを適用することもできます。

{{% notice title="Exercise" style="green" icon="running" %}}

- `[WORKSHOP]` ディレクトリ内に、`8-routing-data` という名前の新しいサブディレクトリを作成します。
- 次に、`7-transform-data` ディレクトリから `*.yaml` を `8-routing-data` にコピーします。
- **すべての** ターミナルウィンドウを `[WORKSHOP]/8-routing-data` ディレクトリに変更します。

更新後のディレクトリ構造は以下のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}

次に、Routing Connectorと対応するパイプラインを設定します。
