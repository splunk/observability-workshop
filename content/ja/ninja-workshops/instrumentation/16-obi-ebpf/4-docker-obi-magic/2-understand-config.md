---
title: 2. OBI 設定の理解
weight: 2
---

## OBI 設定ファイル

`obi-config.yaml`（リポジトリに既に含まれています）を開いて、OBI がどのようにサービスを検出し、計装するのかを理解しましょう。

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

**`discovery.instrument`** は、OBI に対してサービスを見つける方法と、そのサービスに付ける名前を指示します。リッスンしているポートでプロセスをマッチングし、`name` を生成されるトレースの `service.name` 属性に割り当てます。これがない場合、OBI は実行ファイルのパス（例: `/usr/local/bin/order-processor`）をサービス名として使用します。

**`context_propagation: all`** は分散トレーシングの鍵となります。OBI はカーネルレベルで送信 HTTP リクエストに `Traceparent` ヘッダーを注入します。これにより、`frontend` で開始されたトレースが、これらのサービスがトレーシングについて何も知らなくても、`order-processor` を経由して `payment-service` まで接続されます。

**`otel_traces_export.endpoint`** は、OBI にトレースの送信先を指示します。OBI は `network_mode: host` を使用しているため、`localhost:4318` は compose ファイルでホストにマッピングされている collector のポートに到達します。

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
より詳細な設定オプションについては、OBI のドキュメントを参照してください。

* [Service discovery](https://opentelemetry.io/docs/zero-code/obi/configure/service-discovery)
* [Context propagation](https://opentelemetry.io/docs/zero-code/obi/configure/metrics-traces-attributes/#context-propagation)
* [Config example](https://opentelemetry.io/docs/zero-code/obi/configure/example/)
{{% /notice %}}
