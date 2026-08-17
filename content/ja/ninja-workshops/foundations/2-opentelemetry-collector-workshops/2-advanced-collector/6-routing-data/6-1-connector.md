---
title: 6.1 Configure the Routing Connector
linkTitle: 6.1 Routing Configuration
weight: 1
---

この演習では、`gateway.yaml` で **Routing Connector** を設定します。Routing Connector はメトリクス、トレース、ログを任意の属性に基づいてルーティングできますが、ここでは `deployment.environment` 属性に基づくトレースルーティングに焦点を当てます（ただし、任意のスパン/ログ/メトリクス属性を使用できます）。

{{% notice title="Exercise" style="green" icon="running" %}}

**新しい `file` エクスポーターを追加する**: `routing` コネクターには、ルーティング用に異なるターゲットが必要です。**Gateway terminal** で、`gateway.yaml` の `exporters` セクションに 2 つの新しいファイルエクスポーター `file/traces/route1-regular` と `file/traces/route2-security` を作成し、データが正しく振り分けられるようにします

```yaml
  file/traces/route1-regular:                     # Exporter for regular traces
    path: "./gateway-traces-route1-regular.out"   # Path for saving trace data
    append: false                                 # Overwrite the file each time
  file/traces/route2-security:                    # Exporter for security traces
    path: "./gateway-traces-route2-security.out"  # Path for saving trace data
    append: false                                 # Overwrite the file each time
```

**ルーティングを有効にする**: `routing` コネクターを追加します。OpenTelemetry の設定ファイルでは、`connectors` はレシーバーやプロセッサーと同様に専用のセクションを持っています。

`#connectors:` セクションを見つけてコメントを解除します。次に、`connectors:` セクションの下に以下を追加します

```yaml
  routing:
    default_pipelines: [traces/route1-regular]  # Default pipeline if no rule matches
    error_mode: ignore                          # Ignore errors in routing
    table:                                      # Define routing rules
      # Routes spans to a target pipeline if the resourceSpan attribute matches the rule
      - statement: route() where attributes["deployment.environment"] == "security-applications"
        pipelines: [traces/route2-security]     # Security target pipeline
```

{{% /notice %}}

設定ファイルのデフォルトパイプラインは、キャッチオールとして機能します。ルーティングルールテーブルのルールに一致しないすべてのデータ（この場合はスパン）のルーティング先となります。このテーブルには、`["deployment.environment"] == "security-applications"` ルールに一致するスパンのターゲットパイプラインが定義されています。

`routing` の設定が完了したら、次のステップはこれらのルーティングルールを適用する `pipelines` を設定することです。
