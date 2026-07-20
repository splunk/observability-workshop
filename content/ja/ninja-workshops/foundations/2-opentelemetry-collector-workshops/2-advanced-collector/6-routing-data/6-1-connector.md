---
title: 6.1 Routing Connectorの設定
linkTitle: 6.1 Routingの設定
weight: 1
---

この演習では、`gateway.yaml`で **Routing Connector** を設定します。Routing Connectorは任意の属性に基づいてメトリクス、トレース、ログをルーティングできますが、ここでは`deployment.environment`属性に基づくトレースルーティングに焦点を当てます（任意のSpan/ログ/メトリクス属性を使用できます）。

{{% exercise title="Routing Connectorの設定" %}}

**新しい `file` Exporterを追加します**: `routing` Connectorにはルーティング先として異なるターゲットが必要です。**Gatewayターミナル** で、`gateway.yaml`の`exporters`セクションに`file/traces/route1-regular`と`file/traces/route2-security`の2つの新しいファイルExporterを作成し、データが正しく送信されるようにします。

```yaml
  file/traces/route1-regular:                     # Exporter for regular traces
    path: "./gateway-traces-route1-regular.out"   # Path for saving trace data
    append: false                                 # Overwrite the file each time
  file/traces/route2-security:                    # Exporter for security traces
    path: "./gateway-traces-route2-security.out"  # Path for saving trace data
    append: false                                 # Overwrite the file each time 
```

`routing` Connectorを追加して **ルーティングを有効にします**。OpenTelemetryの設定ファイルでは、`connectors`はReceiverやProcessorと同様に専用のセクションを持ちます。

`#connectors:`セクションを見つけてコメントを解除します。次に、`connectors:`セクションの下に以下を追加します。

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

設定ファイルのデフォルトパイプラインはキャッチオールとして機能します。ルーティングルールテーブルのルールに一致しないデータ（ここではSpan）のルーティング先となります。このテーブルには、`["deployment.environment"] == "security-applications"`というルールに一致するSpanのターゲットパイプラインが定義されています。

`routing`の設定が完了したら、次のステップではこれらのルーティングルールを適用するための`pipelines`を設定します。
