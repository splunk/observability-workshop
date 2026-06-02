---
title: 8. データのルーティング
linkTitle: 8. データのルーティング
time: 10 minutes
weight: 10
---

OpenTelemetry の [**Routing Connector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) は、特定の条件に基づいてデータ（`traces`、`metrics`、`logs`）を異なるパイプラインに振り分けることができる強力な機能です。これは、テレメトリーデータのサブセットに対して異なる処理やエクスポートのロジックを適用したい場合に特に有用です。

例えば、*production* のデータを 1 つの Exporter に送信し、*test* や *development* のデータを別の Exporter に送る、といった使い方ができます。同様に、サービス名、環境、Span 名などの属性に基づいて特定の Span をルーティングし、カスタムの処理やストレージのロジックを適用することも可能です。

{{% notice title="演習" style="green" icon="running" %}}

- `[WORKSHOP]` ディレクトリ内に `8-routing-data` という新しいサブディレクトリを作成します。
- 次に、`7-transform-data` ディレクトリから `*.yaml` を `8-routing-data` にコピーします。
- **すべての** ターミナルウィンドウを `[WORKSHOP]/8-routing-data` ディレクトリに変更します。

更新後のディレクトリ構造は以下のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}

次に、Routing Connector とそれぞれのパイプラインを設定します。
