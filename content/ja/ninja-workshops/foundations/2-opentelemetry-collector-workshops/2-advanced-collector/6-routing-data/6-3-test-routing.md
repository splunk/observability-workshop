---
title: 6.3 Test Routing Connector
linkTitle: 6.3 Test Routing Connector
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

このセクションでは、**Gateway** 用に設定した `routing` ルールをテストします。期待される結果は、`"[deployment.environment"] == "security-applications"` ルールに一致する `loadgen` によって生成された `span` が `gateway-traces-route2-security.out` ファイルに送信されることです。

**Gateway を起動する**: **Gateway terminal** ウィンドウで **Gateway** を起動します。

```bash
../otelcol --config gateway.yaml
```

**Agent を起動する**: **Agent terminal** ウィンドウで **Agent** を起動します。

```bash
../otelcol --config agent.yaml
```

**通常のスパンを送信する**: **Loadgen terminal** ウィンドウで `loadgen` を使用して通常のスパンを送信します

```bash
../loadgen -count 1
```

**Agent** と **Gateway** の両方でデバッグ情報が表示されます。Gateway は新しい `gateway-traces-route1-regular.out` ファイルも生成します。これが通常のスパンの指定された宛先になりました。

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
`gateway-traces-route1-regular.out` を確認すると、`loadgen` によって送信された `span` が含まれています。また、空の `gateway-traces-route2-security..out` ファイルも表示されます。これは、ルーティング設定が、一致するスパンがまだ処理されていなくても、すぐに出力ファイルを作成するためです。
{{% /notice %}}

**セキュリティスパンを送信する**: **Loadgen terminal** ウィンドウで `security` フラグを使用してセキュリティスパンを送信します

```bash
../loadgen -security -count 1
```

再び、**Agent** と **Gateway** の両方で、送信したスパンを含むデバッグ情報が表示されるはずです。今回は、**Gateway** が `gateway-traces-route2-security.out` ファイルに行を書き込みます。これは、`deployment.environment` リソース属性が `"security-applications"` に一致するスパン用に指定されたファイルです。

{{% tabs %}}
{{% tab title="Validate resource attribute matches" %}}

```bash
jq -c '.resourceSpans[] as $resource | $resource.scopeSpans[].spans[] | {spanId: .spanId, deploymentEnvironment: ($resource.resource.attributes[] | select(.key == "deployment.environment") | .value.stringValue)}' gateway-traces-route2-security.out
```

{{% /tabs %}}
{{% tab title="Output" %}}

```json
{"spanId":"cb799e92e26d5782","deploymentEnvironment":"security-applications"}
```

{{% /tab %}}
{{% /tabs %}}

このシナリオを複数回繰り返すことができ、各トレースは対応する出力ファイルに書き込まれます。

{{% /notice %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止してください。

## まとめ

このセクションでは、異なるスパンを送信し、その宛先を確認することで、Gateway のルーティングコネクターを正常にテストしました。

- **通常のスパン** は `gateway-traces-route1-regular.out` に正しくルーティングされ、一致する `deployment.environment` 属性を持たないスパンがデフォルトパイプラインに従うことが確認されました。

- **セキュリティ関連のスパン** は `gateway-traces-route2-security.out` にルーティングされ、`"deployment.environment": "security-applications"` に基づくルーティングルールが期待どおりに機能することが実証されました。

出力ファイルを検査することで、OpenTelemetry Collector が *スパン属性を正しく評価し、適切な宛先にルーティングしている* ことを確認しました。これにより、ルーティングルールが異なるユースケース向けにテレメトリデータを効果的に分離して振り分けることができることが検証されました。

追加のルーティングルールを定義して、異なる属性に基づいてスパン、メトリクス、ログをさらに分類することで、このアプローチを拡張できます。
