---
title: OpenTelemetry Collector Processors
linkTitle: 4.3 Attributes
weight: 3
---

## Attributes Processor

Attributes プロセッサーは、スパン、ログ、またはメトリクスの属性を変更します。このプロセッサーは、指定されたアクションに対して含めるか除外するかを決定するために、入力データのフィルタリングとマッチングもサポートしています。

設定ファイルで指定された順序で実行されるアクションのリストを受け取ります。サポートされているアクションは以下の通りです

- `insert`: キーがまだ存在しない入力データに新しい属性を挿入します。
- `update`: キーが存在する入力データの属性を更新します。
- `upsert`: 挿入または更新を実行します。キーがまだ存在しない入力データに新しい属性を挿入し、キーが存在する入力データの属性を更新します。
- `delete`: 入力データから属性を削除します。
- `hash`: 既存の属性値をハッシュ化（SHA1）します。
- `extract`: 入力キーから正規表現ルールを使用して値を抽出し、ルールで指定されたターゲットキーに設定します。ターゲットキーが既に存在する場合は、上書きされます。

ここでは、すべてのホストメトリクスに `participant.name` という新しい属性を `insert` する attributes プロセッサーを作成します。値にはあなたの名前を設定します（例`marge_simpson`）。

{{% notice style="warning" %}}

`INSERT_YOUR_NAME_HERE` を必ずあなたの名前に置き換えてください。また、名前にスペースを**使用しない**ようにしてください。

{{% /notice %}}

ワークショップの後半で、この属性を使用して Splunk Observability Cloud でメトリクスをフィルタリングします。

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

{{% expand title="{{% badge style=primary icon=star %}}**Ninja:** コネクターを使用して内部インサイトを取得する{{% /badge %}}" %}}

コレクターへの最新の追加機能の1つが[**コネクター**](https://opentelemetry.io/docs/collector/configuration/#connectors)の概念です。これにより、あるパイプラインの出力を別のパイプラインの入力に接続できます。

これが有益な例として、エクスポートされるデータポイントの量に基づいてメトリクスを出力するサービス、エラーステータスを含むログの数、または1つのデプロイメント環境から送信されるデータ量などがあります。count コネクターは、これらの課題をすぐに解決してくれます。

## なぜプロセッサーではなくコネクターなのか？

プロセッサーは、処理したデータを渡す必要があるため、追加データの生成が制限され、追加情報の公開が困難です。コネクターは受信したデータを出力する必要がないため、求めているインサイトを作成する機会を提供します。

例えば、デプロイメント環境属性を持たないログ、メトリクス、トレースの数をカウントするコネクターを作成できます。

デプロイメント環境ごとにデータ使用量を分解できる、非常にシンプルな例です。

## コネクターに関する考慮事項

コネクターは、あるパイプラインからエクスポートされ、別のパイプラインで受信されるデータのみを受け付けます。そのため、コネクターを活用するにはコレクターの設定をどのように構成するかを考慮する必要があります。

## References

1. [**https://opentelemetry.io/docs/collector/configuration/#connectors**](https://opentelemetry.io/docs/collector/configuration/#connectors)
2. [**https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector)

{{% /expand %}}

## 設定の確認

プロセッサーのセクションは以上です。設定の変更を確認しましょう。

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}設定を確認する{{% /badge %}}" %}}
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
