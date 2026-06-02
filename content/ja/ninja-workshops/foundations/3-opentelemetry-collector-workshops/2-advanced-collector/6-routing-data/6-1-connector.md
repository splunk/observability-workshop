---
title: 6.1 Routing Connector の設定
linkTitle: 6.1 Routing の設定
weight: 1
---

この演習では、`gateway.yaml` 内で **Routing Connector** を設定します。Routing Connector はメトリクス、トレース、ログを任意の属性に基づいてルーティングできますが、ここでは `deployment.environment` 属性に基づくトレースのルーティングに絞って扱います（任意の span / log / metric 属性を使用可能です）。

{{% exercise title="Configure the routing connector" %}}

**新しい `file` exporter を追加します**: `routing` connector はルーティング先として複数のターゲットを必要とします。**Gateway ターミナル**で、`gateway.yaml` の `exporters` セクションに、データが正しく振り分けられるよう、`file/traces/route1-regular` と `file/traces/route2-security` の 2 つの新しい file exporter を作成します。

```yaml
  file/traces/route1-regular:                     # Exporter for regular traces
    path: "./gateway-traces-route1-regular.out"   # Path for saving trace data
    append: false                                 # Overwrite the file each time
  file/traces/route2-security:                    # Exporter for security traces
    path: "./gateway-traces-route2-security.out"  # Path for saving trace data
    append: false                                 # Overwrite the file each time 
```

`routing` connector を追加して**ルーティングを有効化**します。OpenTelemetry の設定ファイルでは、`connectors` は receivers や processors と同様に専用のセクションを持っています。

`#connectors:` セクションを見つけてコメントアウトを解除します。次に、`connectors:` セクションの下に以下を追加します。

```yaml
  routing:
    default_pipelines: [traces/route1-regular]  # Default pipeline if no rule matches
    error_mode: ignore                          # Ignore errors in routing
    table:                                      # Define routing rules
      # Routes spans to a target pipeline if the resourceSpan attribute matches the rule
      - statement: route() where attributes["deployment.environment"] == "security-applications"
        pipelines: [traces/route2-security]     # Security target pipeline 
```

{{% /exercise %}}

設定ファイル内の default pipeline は Catch all として機能します。これはルーティングルールテーブル内のどのルールにも一致しないデータ（ここでは span）に対するルーティング先となります。このテーブルでは、次のルール `["deployment.environment"] == "security-applications"` に一致する span のルーティング先となる pipeline を定義しています。

`routing` の設定が完了したら、次のステップではこれらのルーティングルールを適用するために `pipelines` を設定します。
