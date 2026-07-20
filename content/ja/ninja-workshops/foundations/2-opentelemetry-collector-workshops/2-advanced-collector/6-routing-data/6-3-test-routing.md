---
title: 6.3 Routing Connector のテスト
linkTitle: 6.3 Routing Connector のテスト
weight: 3
---

{{% exercise title="Span がセキュリティファイルにルーティングされることを確認する" %}}

このセクションでは、**Gateway** に設定した `routing` ルールをテストします。期待される結果は、`loadgen` が生成した `span` のうち、`"[deployment.environment"] == "security-applications"` ルールに一致するものが `gateway-traces-route2-security.out` ファイルに送信されることです。

**Gateway の起動**: **Gateway ターミナル** ウィンドウで **Gateway** を起動します。

```bash
../otelcol --config gateway.yaml
```

**Agent の起動**: **Agent ターミナル** ウィンドウで **Agent** を起動します。

```bash
../otelcol --config agent.yaml
```

**通常の Span を送信**: **Loadgen ターミナル** ウィンドウで `loadgen` を使用して通常の span を送信します。

```bash
../loadgen -count 1
```

**Agent** と **Gateway** の両方にデバッグ情報が表示されます。Gateway は新しい `gateway-traces-route1-regular.out` ファイルも生成します。これは通常の span の送信先として指定されたファイルです。

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
`gateway-traces-route1-regular.out` を確認すると、`loadgen` が送信した `span` が含まれています。また、空の `gateway-traces-route2-security..out` ファイルも確認できます。これは、ルーティング設定が一致する span がまだ処理されていなくても、出力ファイルを即座に作成するためです。
{{% /notice %}}

**セキュリティ Span を送信**: **Loadgen ターミナル** ウィンドウで `security` フラグを使用してセキュリティ span を送信します。

```bash
../loadgen -security -count 1
```

再び、**Agent** と **Gateway** の両方に、送信した span を含むデバッグ情報が表示されます。今回は、**Gateway** が `gateway-traces-route2-security.out` ファイルに行を書き込みます。このファイルは、`deployment.environment` リソース属性が `"security-applications"` に一致する span の送信先です。

{{% tabs %}}
{{% tab title="リソース属性の一致を検証" %}}

```bash
jq -c '.resourceSpans[] as $resource | $resource.scopeSpans[].spans[] | {spanId: .spanId, deploymentEnvironment: ($resource.resource.attributes[] | select(.key == "deployment.environment") | .value.stringValue)}' gateway-traces-route2-security.out
```

{{% /tabs %}}
{{% tab title="出力" %}}

```json
{"spanId":"cb799e92e26d5782","deploymentEnvironment":"security-applications"}
```

{{% /tab %}}
{{% /tabs %}}

このシナリオを複数回繰り返すことができ、各トレースは対応する出力ファイルに書き込まれます。

{{% /exercise %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止してください。

## まとめ

このセクションでは、異なる span を送信してその送信先を確認することで、Gateway の Routing Connector を正常にテストしました。

- **通常の span** は `gateway-traces-route1-regular.out` に正しくルーティングされ、一致する `deployment.environment` 属性を持たない span がデフォルトのパイプラインに従うことを確認しました。

- **セキュリティ関連の span** は `gateway-traces-route2-security.out` にルーティングされ、`"deployment.environment": "security-applications"` に基づくルーティングルールが期待通りに動作することを実証しました。

出力ファイルを検査することで、OpenTelemetry Collector が *span の属性を正しく評価し、適切な送信先にルーティングする* ことを確認しました。これにより、ルーティングルールがさまざまなユースケースに対してテレメトリデータを効果的に分離および転送できることが検証されました。

このアプローチを拡張して、異なる属性に基づいて span、メトリクス、ログをさらに分類する追加のルーティングルールを定義できます。
