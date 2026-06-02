---
title: 8.3 Routing Connector のテスト
linkTitle: 8.3 Routing Connector のテスト
weight: 3
---

{{% notice title="演習" style="green" icon="running" %}}

このセクションでは、**Gateway** に設定した `routing` ルールをテストします。期待される結果は、`loadgen` によって生成された `span` が `gateway-traces-security.out` ファイルに送信されることです。

**Gateway を起動する**: **Gateway ターミナル**ウィンドウで `gateway` を起動します。

```bash
../otelcol --config gateway.yaml
```

**Agent を起動する**: **Agent ターミナル**ウィンドウで `agent` を起動します。

```bash
../otelcol --config agent.yaml
```

**通常の Span を送信する**: **Spans ターミナル**ウィンドウで、`loadgen` を使用して通常の span を送信します。

```bash
../loadgen -count 1
```

`agent` と `gateway` の両方がデバッグ情報を表示します。gateway は新しい `gateway-traces-standard.out` ファイルも生成します。これは通常の span の指定された送信先となったためです。

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
`gateway-traces-standard.out` を確認すると、`loadgen` によって送信された `span` が含まれています。また、空の `gateway-traces-security.out` ファイルも表示されます。これは、ルーティング設定によって、まだ一致する span が処理されていなくても、出力ファイルが即座に作成されるためです。
{{% /notice %}}

**Security Span を送信する**: **Spans ターミナル**ウィンドウで、`security` フラグを使用して security span を送信します。

```bash
../loadgen -security -count 1
```

再度、`agent` と `gateway` の両方が、送信した span を含むデバッグ情報を表示するはずです。今度は、`gateway` が `gateway-traces-security.out` ファイルに 1 行書き込みます。このファイルは、`deployment.environment` リソース属性が `"security-applications"` に一致する span 用に指定されています。
`gateway-traces-standard.out` は変更されないはずです。

{{% tabs %}}
{{% tab title="リソース属性の一致を検証する" %}}

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

このシナリオは複数回繰り返すことができ、各トレースは対応する出力ファイルに書き込まれます。

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、`agent` と `gateway` のプロセスを停止します。

{{% /notice %}}

## まとめ

このセクションでは、異なる span を送信してそれぞれの送信先を検証することで、gateway の routing connector のテストに成功しました。

- **通常の span** は `gateway-traces-standard.out` に正しくルーティングされ、`deployment.environment` 属性に一致しない span がデフォルトのパイプラインに従うことを確認しました。

- **セキュリティ関連の span** は `gateway-traces-security.out` にルーティングされ、`"deployment.environment": "security-applications"` に基づくルーティングルールが期待どおりに機能することを示しました。

出力ファイルを確認することで、OpenTelemetry Collector が *span 属性を正しく評価し、適切な送信先にルーティングする* ことを確認しました。これにより、ルーティングルールがさまざまなユースケース向けにテレメトリーデータを効果的に分離・転送できることが検証されました。

このアプローチを拡張して、追加のルーティングルールを定義することで、さまざまな属性に基づいて span、メトリクス、ログをさらに分類できます。
