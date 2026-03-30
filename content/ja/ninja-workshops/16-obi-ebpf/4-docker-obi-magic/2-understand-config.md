---
title: 2. OBI 設定の理解
weight: 2
---

## OBI 設定ファイル

`obi-config.yaml`（リポジトリに含まれています）を開いて、OBIがどのようにサービスを検出し、計装するかを理解しましょう:

``` bash
cat ~/workshop/obi/02-obi-docker/obi-config.yaml
```

``` yaml
discovery:
  instrument:
    - name: "frontend"
      open_ports: 3000
    - name: "order-processor"
      open_ports: 8080
    - name: "payment-service"
      open_ports: 8081

ebpf:
  context_propagation: all

otel_traces_export:
  endpoint: http://localhost:4318
```

### 各セクションの動作

**`discovery.instrument`** は、OBIにサービスの検出方法と名前の付け方を指示します。プロセスがリッスンしているポートでマッチングし、生成されるトレースの `service.name` 属性として `name` を割り当てます。これがない場合、OBIは実行ファイルのパスをサービス名として使用します（例: `/usr/local/bin/order-processor`）。

**`context_propagation: all`** は分散トレーシングの鍵です。OBIはカーネルレベルで送信HTTPリクエストに `Traceparent` ヘッダーを注入します。これにより、`frontend` で開始されたトレースが `order-processor` を経由して `payment-service` まで接続されます -- これらのサービスがトレーシングについて何も知らなくても。

**`otel_traces_export.endpoint`** は、OBIにトレースの送信先を指示します。OBIは `network_mode: host` を使用するため、`localhost:4318` はcomposeファイルでホストにマッピングされたCollectorのポートに到達します。

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
詳細な設定オプションについては、OBIドキュメントを参照してください:

* [Service discovery](https://opentelemetry.io/docs/zero-code/obi/configure/service-discovery)
* [Context propagation](https://opentelemetry.io/docs/zero-code/obi/configure/metrics-traces-attributes/#context-propagation)
* [Config example](https://opentelemetry.io/docs/zero-code/obi/configure/example/)
{{% /notice %}}
