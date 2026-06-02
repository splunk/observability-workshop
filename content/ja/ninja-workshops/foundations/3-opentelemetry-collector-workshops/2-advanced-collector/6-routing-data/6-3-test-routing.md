---
title: 6.3 Test Routing Connector
linkTitle: 6.3 Test Routing Connector
weight: 3
---

{{% exercise title="Verify spans route to the security file" %}}

このセクションでは、**Gateway** に設定した `routing` ルールをテストします。期待される結果は、`loadgen` によって生成された `span` のうち `"[deployment.environment"] == "security-applications"` ルールに一致するものが、`gateway-traces-route2-security.out` ファイルに送信されることです。

**Gatewayを起動します**: **Gateway terminal** ウィンドウで **Gateway** を起動します。

```bash
../otelcol --config gateway.yaml
```

**Agentを起動します**: **Agent terminal** ウィンドウで **Agent** を起動します。

```bash
../otelcol --config agent.yaml
```

**通常のSpanを送信します**: **Loadgen terminal** ウィンドウで `loadgen` を使用して通常のスパンを送信します。

```bash
../loadgen -count 1
```

**Agent** と **Gateway** の両方がデバッグ情報を表示します。Gatewayは新しい `gateway-traces-route1-regular.out` ファイルも生成します。これは、通常のスパンの送信先として指定されたためです。

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
`gateway-traces-route1-regular.out` を確認すると、`loadgen` によって送信された `span` が含まれています。また、空の `gateway-traces-route2-security..out` ファイルも確認できます。これは、ルーティング設定が、一致するスパンがまだ処理されていない場合でも出力ファイルを即座に作成するためです。
{{% /notice %}}

**Security Spanを送信します**: **Loadgen terminal** ウィンドウで `security` フラグを使用してセキュリティスパンを送信します。

```bash
../loadgen -security -count 1
```

再び、**Agent** と **Gateway** の両方がデバッグ情報（先ほど送信したスパンを含む）を表示するはずです。今回は、**Gateway** が `gateway-traces-route2-security.out` ファイルに行を書き込みます。このファイルは、`deployment.environment` リソース属性が `"security-applications"` に一致するスパン用に指定されたものです。

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

このシナリオは複数回繰り返すことができ、各トレースは対応する出力ファイルに書き込まれます。

{{% /exercise %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止します。

## Conclusion

このセクションでは、異なるスパンを送信して送信先を検証することで、Gatewayにおけるルーティングコネクタのテストに成功しました。

- **通常のスパン** は `gateway-traces-route1-regular.out` に正しくルーティングされました。これにより、`deployment.environment` 属性が一致しないスパンがデフォルトのパイプラインに従うことが確認されました。

- **セキュリティ関連のスパン** は `gateway-traces-route2-security.out` にルーティングされました。これにより、`"deployment.environment": "security-applications"` に基づくルーティングルールが期待どおりに動作することが実証されました。

出力ファイルを検査することで、OpenTelemetry Collectorが *スパンの属性を正しく評価し、適切な送信先にルーティングする* ことを確認しました。これにより、ルーティングルールが異なるユースケースに応じてテレメトリーデータを効果的に分離し、振り分けられることが検証されます。

このアプローチを拡張して、異なる属性に基づいてスパン、メトリクス、ログをさらに分類するための追加のルーティングルールを定義することができます。
