---
title: 8.1 Routing Connector の設定
linkTitle: 8.1 Routing 設定
weight: 1
---

この演習では、`gateway.yaml` ファイルで **Routing Connector** を設定します。この設定により、`gateway` は送信されたスパンの `deployment.environment` 属性に基づいてトレースをルーティングできるようになります。これを実装することで、属性に応じてトレースを異なる方法で処理できます。

{{% notice title="演習" style="green" icon="running" %}}

OpenTelemetry の設定ファイルでは、`connectors` は receivers や processors と同様に、専用のセクションを持ちます。

**`routing` コネクターを追加します**:
**Gateway ターミナル** ウィンドウで `gateway.yaml` を編集し、`#connectors:` セクションのコメントを解除します。次に、`connectors:` セクションの下に以下を追加します:

```yaml
connectors: 
  routing:
    default_pipelines: [traces/standard] # Default pipeline if no rule matches
    error_mode: ignore                   # Ignore errors in routing
    table:                               # Define routing rules
      # Routes spans to a target pipeline if the resourceSpan attribute matches the rule
      - statement: route() where attributes["deployment.environment"] == "security-applications"
        pipelines: [traces/security]     # Target pipeline 
```

上記のルールはトレースに適用されますが、このアプローチは `metrics` や `logs` にも適用でき、`resourceMetrics` または `resourceLogs` の属性に基づいてルーティングできます。

**`file:` exporter を設定します**: `routing` コネクターは、ルーティング先として個別のターゲットを必要とします。`exporters:` セクションに、`file/traces/security` と `file/traces/standard` の 2 つの file exporter を追加し、データが正しく送信されるようにします。

```yaml
  file/traces/standard:                    # Exporter for regular traces
    path: "./gateway-traces-standard.out"  # Path for saving trace data
    append: false                          # Overwrite the file each time
  file/traces/security:                    # Exporter for security traces
    path: "./gateway-traces-security.out"  # Path for saving trace data
    append: false                          # Overwrite the file each time 
```

{{% /notice %}}

`routing` の設定が完了したら、次のステップではこれらのルーティングルールを適用するために `pipelines` を設定します。
