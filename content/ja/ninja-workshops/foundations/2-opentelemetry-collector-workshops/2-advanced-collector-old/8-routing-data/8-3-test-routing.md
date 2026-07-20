---
title: 8.3 Routing Connector のテスト
linkTitle: 8.3 Routing Connector のテスト
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

このセクションでは、**Gateway** に設定した `routing` ルールをテストします。期待される結果は、`loadgen` が生成した `span` が `gateway-traces-security.out` ファイルに送信されることです。

**Gateway の起動**: **Gateway ターミナル** ウィンドウで `gateway` を起動します。

```bash
../otelcol --config gateway.yaml
```

**Agent の起動**: **Agent ターミナル** ウィンドウで `agent` を起動します。

```bash
../otelcol --config agent.yaml
```

**通常の Span を送信**: **Spans ターミナル** ウィンドウで `loadgen` を使用して通常の Span を送信します。

```bash
../loadgen -count 1
```

`agent` と `gateway` の両方にデバッグ情報が表示されます。Gateway は新しい `gateway-traces-standard.out` ファイルも生成します。これは通常の Span の送信先として指定されたファイルです。

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
`gateway-traces-standard.out` を確認すると、`loadgen` が送信した `span` が含まれています。また、空の `gateway-traces-security.out` ファイルも表示されます。これは、ルーティング設定が一致する Span がまだ処理されていなくても、出力ファイルを即座に作成するためです。
{{% /notice %}}

**セキュリティ Span を送信**: **Spans ターミナル** ウィンドウで `security` フラグを使用してセキュリティ Span を送信します。

```bash
../loadgen -security -count 1
```

再び、`agent` と `gateway` の両方に、送信した Span を含むデバッグ情報が表示されます。今回は、`gateway` が `gateway-traces-security.out` ファイルに行を書き込みます。このファイルは、`deployment.environment` リソース属性が `"security-applications"` に一致する Span の送信先として指定されています。
`gateway-traces-standard.out` は変更されないはずです。

{{% tabs %}}
{{% tab title="リソース属性の一致を検証" %}}

```bash
jq -c '.resourceSpans[] as $resource | $resource.scopeSpans[].spans[] | {spanId: .spanId, deploymentEnvironment: ($resource.resource.attributes[] | select(.key == "deployment.environment") | .value.stringValue)}' gateway-traces-security.out
```

{{% /tabs %}}
{{% tab title="出力" %}}

```json
{"spanId":"cb799e92e26d5782","deploymentEnvironment":"security-applications"}
```

{{% /tab %}}
{{% /tabs %}}

このシナリオを複数回繰り返すことができ、各トレースは対応する出力ファイルに書き込まれます。

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、`agent` と `gateway` のプロセスを停止してください。

{{% /notice %}}

## まとめ

このセクションでは、異なる Span を送信し、その送信先を確認することで、Gateway の Routing Connector のテストに成功しました。

- **通常の Span** は `gateway-traces-standard.out` に正しくルーティングされ、一致する `deployment.environment` 属性を持たない Span がデフォルトのパイプラインに従うことを確認しました。

- **セキュリティ関連の Span** は `gateway-traces-security.out` にルーティングされ、`"deployment.environment": "security-applications"` に基づくルーティングルールが期待通りに動作することを実証しました。

出力ファイルを検査することで、OpenTelemetry Collector が *Span の属性を正しく評価し、適切な送信先にルーティングする* ことを確認しました。これにより、ルーティングルールが異なるユースケースに応じてテレメトリデータを効果的に分離・転送できることが検証されました。

このアプローチを拡張して、異なる属性に基づいて Span、メトリクス、ログをさらに分類する追加のルーティングルールを定義できます。
