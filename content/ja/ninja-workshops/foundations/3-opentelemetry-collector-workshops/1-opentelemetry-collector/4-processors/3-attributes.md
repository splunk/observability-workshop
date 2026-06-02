---
title: OpenTelemetry Collector Processors
linkTitle: 4.3 Attributes
weight: 3
---

## Attributes Processor

attributes processor は、span、log、metric の属性を変更します。このプロセッサーは、入力データをフィルタリング・マッチングして、指定したアクションの対象に含めるか除外するかを判定する機能もサポートしています。

設定で指定された順番で実行される一連のアクションを受け取ります。サポートされているアクションは次のとおりです。

- `insert`: キーがまだ存在しない場合に、入力データへ新しい属性を挿入します。
- `update`: キーが存在する場合に、入力データの属性を更新します。
- `upsert`: insert または update を実行します。キーが存在しない場合は新しい属性を挿入し、キーが存在する場合は属性を更新します。
- `delete`: 入力データから属性を削除します。
- `hash`: 既存の属性値をハッシュ化（SHA1）します。
- `extract`: 正規表現ルールを使用して、入力キーからルールに指定されたターゲットキーへ値を抽出します。ターゲットキーが既に存在する場合は上書きされます。

これから、すべてのホストメトリクスに `participant.name` という新しい属性を `insert` する attributes processor を作成します。値にはご自身の名前（例: `marge_simpson`）を設定します。

{{% notice style="warning" %}}

`INSERT_YOUR_NAME_HERE` は必ずご自身の名前に置き換えてください。また、名前にスペースを **使用しない** ようにしてください。

{{% /notice %}}

ワークショップの後半では、この属性を使用して Splunk Observability Cloud のメトリクスをフィルタリングします。

{{% tab title="Attributes Processor Configuration" %}}

``` yaml {hl_lines="9-13"}
processors:
  batch:
  resourcedetection/system:
    detectors: [system]
    system:
      hostname_sources: [os]
  resourcedetection/ec2:
    detectors: [ec2]
  attributes/conf:
    actions:
      - key: participant.name
        action: insert
        value: "INSERT_YOUR_NAME_HERE"
```

{{%/ tab %}}

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Using connectors to gain internal insights{{% /badge %}}" %}}

Collector に最近追加されたものの一つに [**connector**](https://opentelemetry.io/docs/collector/configuration/#connectors) という概念があり、あるパイプラインの出力を別のパイプラインの入力につなぐことができます。

これがどのように役立つかの例として、エクスポートされたデータポイントの量、エラーステータスを含むログの数、あるデプロイ環境から送信されたデータの量に基づいてメトリクスを発行するサービスがあります。count connector はこれを標準で対応してくれます。

## なぜプロセッサーではなくコネクターなのか?

プロセッサーは、処理したデータをそのまま渡さなければならないため、追加で生成できるデータが限られており、追加情報を公開するのが困難です。コネクターは受け取ったデータをそのまま発行する必要がないため、求めているインサイトを生み出す機会を提供してくれます。

例えば、デプロイ環境属性を持たないログ、メトリクス、トレースの数をカウントするコネクターを作成できます。

非常にシンプルな例として、デプロイ環境ごとにデータ使用量を分解して出力できます。

## コネクターを使う際の考慮事項

コネクターは、あるパイプラインからエクスポートされ、別のパイプラインで受信されるデータのみを受け付けます。これを活用するためには、Collector の設定をどのように構成するかを考慮する必要があります。

## References

1. [**https://opentelemetry.io/docs/collector/configuration/#connectors**](https://opentelemetry.io/docs/collector/configuration/#connectors)
2. [**https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector)

{{% /expand %}}

---

## Configuration Check-in

プロセッサーについては以上です。設定の変更内容を確認してみましょう。

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}Review your configuration{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml {lineNos="table" wrap="true" hl_lines="69-79"}
# To limit exposure to denial of service attacks, change the host in endpoints below from 0.0.0.0 to a specific network interface.
# See https://github.com/open-telemetry/opentelemetry-collector/blob/main/docs/security-best-practices.md#safeguards-against-denial-of-service-attacks

extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679

receivers:
  hostmetrics:
    collection_interval: 10s
    scrapers:
      # CPU utilization metrics
      cpu:
      # Disk I/O metrics
      disk:
      # File System utilization metrics
      filesystem:
      # Memory utilization metrics
      memory:
      # Network interface I/O metrics & TCP connection metrics
      network:
      # CPU load metrics
      load:
      # Paging/Swap space utilization and I/O metrics
      paging:
      # Process count metrics
      processes:
      # Per process CPU, Memory and Disk I/O metrics. Disabled by default.
      # process:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  opencensus:
    endpoint: 0.0.0.0:55678

  # Collect own metrics
  prometheus/internal:
    config:
      scrape_configs:
      - job_name: 'otel-collector'
        scrape_interval: 10s
        static_configs:
        - targets: ['0.0.0.0:8888']

  jaeger:
    protocols:
      grpc:
        endpoint: 0.0.0.0:14250
      thrift_binary:
        endpoint: 0.0.0.0:6832
      thrift_compact:
        endpoint: 0.0.0.0:6831
      thrift_http:
        endpoint: 0.0.0.0:14268

  zipkin:
    endpoint: 0.0.0.0:9411

processors:
  batch:
  resourcedetection/system:
    detectors: [system]
    system:
      hostname_sources: [os]
  resourcedetection/ec2:
    detectors: [ec2]
  attributes/conf:
    actions:
      - key: participant.name
        action: insert
        value: "INSERT_YOUR_NAME_HERE"

exporters:
  debug:
    verbosity: detailed

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [debug]

    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand %}}

---
