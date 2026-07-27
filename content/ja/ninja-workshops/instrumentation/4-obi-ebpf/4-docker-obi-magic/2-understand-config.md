---
title: 2. OBI 設定の理解
weight: 2
---

## OBI 設定ファイル

`obi-config.yaml`（リポジトリに既に含まれています）を開いて、OBI がサービスを検出し計装する方法を理解しましょう

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

**`discovery.instrument`** は、OBI にサービスの検出方法と名前の付け方を指示します。リッスンしているポートでプロセスをマッチングし、生成されたトレースの `service.name` 属性として `name` を割り当てます。この設定がない場合、OBI は実行ファイルのパス（例`/usr/local/bin/order-processor`）をサービス名として使用します。

**`context_propagation: all`** は分散トレーシングの鍵となる設定です。OBI はカーネルレベルで送信 HTTP リクエストに `Traceparent` ヘッダーを注入します。これにより、`frontend` で開始されたトレースが `order-processor` を経由して `payment-service` まで接続されます。これらのサービスがトレーシングについて何も知らないにもかかわらず、です。

**`otel_traces_export.endpoint`** は、OBI にトレースの送信先を指示します。OBI は `network_mode: host` を使用するため、`localhost:4318` は compose ファイルでホストにマッピングされたコレクターのポートに到達します。

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
より詳細な設定オプションについては、OBI のドキュメントを参照してください

* [Service discovery](https://opentelemetry.io/docs/zero-code/obi/configure/service-discovery)
* [Context propagation](https://opentelemetry.io/docs/zero-code/obi/configure/metrics-traces-attributes/#context-propagation)
* [Config example](https://opentelemetry.io/docs/zero-code/obi/configure/example/)
{{% /notice %}}
