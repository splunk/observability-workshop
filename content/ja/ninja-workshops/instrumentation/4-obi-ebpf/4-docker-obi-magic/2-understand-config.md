---
title: 2. OBI設定の理解
weight: 2
---

## OBI設定ファイル

`obi-config.yaml`（リポジトリに含まれています）を開いて、OBIがサービスを検出し計装する仕組みを確認します:

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

**`discovery.instrument`** は、OBIにサービスの検出方法と名前の付け方を指示します。プロセスがリッスンしているポートで照合し、生成されたトレースの `service.name` 属性として `name` を割り当てます。この設定がない場合、OBIは実行ファイルのパスをサービス名として使用します（例: `/usr/local/bin/order-processor`）。

**`context_propagation: all`** は分散トレーシングの鍵となる設定です。OBIはカーネルレベルで送信HTTPリクエストに `Traceparent` ヘッダーを注入します。これにより、`frontend` で開始されたトレースが `order-processor` を経由して `payment-service` まで接続されます。これらのサービスはトレーシングについて何も知らないにもかかわらず、これが実現されます。

**`otel_traces_export.endpoint`** は、OBIにトレースの送信先を指示します。OBIは `network_mode: host` を使用するため、`localhost:4318` はcomposeファイルでホストにマッピングされたCollectorのポートに到達します。

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
より詳細な設定オプションについては、OBIドキュメントを参照してください。

* [Service discovery](https://opentelemetry.io/docs/zero-code/obi/configure/service-discovery)
* [Context propagation](https://opentelemetry.io/docs/zero-code/obi/configure/metrics-traces-attributes/#context-propagation)
* [Config example](https://opentelemetry.io/docs/zero-code/obi/configure/example/)
{{% /notice %}}
