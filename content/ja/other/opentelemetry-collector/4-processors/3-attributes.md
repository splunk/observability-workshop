---
title: OpenTelemetry Collector プロセッサー
linkTitle: 4.3 Attributes
weight: 3
---

## Attributes プロセッサー

attributeプロセッサーを使うと、スパン、ログ、またはメトリクスの属性を変更できます。また、このプロセッサーは、入力データをフィルタリングし、マッチさせ、指定されたアクションに含めるべきか、除外すべきかを決定する機能もサポートしています。

アクションを設定するには、指定された順序で実行されるアクションのリストを記述します。サポートされるアクションは以下の通りです：

- `insert`: その属性がない場合に、新しい属性値を挿入します。
- `update`: その属性がある場合に、その属性値を更新します。
- `upsert`: insertまたはupdateを実行します。属性がない場合には新しい属性値を挿入し、属性がある場合にはその値を更新します。
- `delete`: 入力データから属性値を削除します。
- `hash`: 属性値をハッシュ化 (SHA1) します。
- `extract`: 入力キーの値を正規表現ルールを使って抽出し、対象キーの値を更新します。対象キーがすでに存在する場合は、その値は上書きされます。

次の例のように、attributeプロセッサーを使って、キーは `participant.name`、あたいはあなたの名前（例: `marge_simpson`）という新しい属性を追加してみましょう。

{{% notice style="warning" %}}

`INSERT_YOUR_NAME_HERE` の箇所は、自分の名前に置き換えてください。また、自分の名前に **スペースを使わない** ようにしてください。

{{% /notice %}}

このワークショップの後半では、この属性を使用してSplunk Observability Cloudでメトリクスをフィルタリングします。

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

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** コネクターを使って内部への洞察を加速する{{% /badge %}}" %}}

最近追加されたものの一つとして、[connector](https://opentelemetry.io/docs/collector/configuration/#connectors) というコンセプトがあります。これを使うと、あるパイプラインの出力を別のパイプラインの入力に結合できるようになります。

利用シーンとして、送信するデータポイントの量、エラーステータスを含むログの数をメトリクスをとして出力するサービスがあります。他には、あるデプロイ環境から送信されるデータ量のメトリクスを生成するサービスがあります。このような場合に、countコネクターですぐに対応できます。

## プロセッサーではなくコネクターなのはなぜ？

プロセッサーは、処理したデータを次に渡すものであり、追加の情報を出力することはできません。コネクターはレシーバーで受け取ったデータを出力せずに、私たちが求める洞察を作り出す機会を提供します。

たとえば、countコネクターを使うと、環境変数 `deployment` を持たないログ、メトリクス、トレースの数をカウントすることができます。

また、非常にシンプルな例として、`deployment` 別にデータ使用量を分解して出力することもできます。

## コネクターの注意事項

コネクターは、あるパイプラインからエクスポートされ、別のパイプラインでレシーバーで定義されたデータのみを受け入れます。コレクターをどう構築してどう利用するか、設定を検討する必要があります。

## 参照

1. [https://opentelemetry.io/docs/collector/configuration/#connectors](https://opentelemetry.io/docs/collector/configuration/#connectors)
2. [https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector)

{{% /expand %}}

---

## 設定を確認しましょう

これで、プロセッサーがカバーできました。ここで、設定のの変更内容をチェックしてみましょう。

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}設定をレビューしてください{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml {lineNos="table" wrap="true" hl_lines="58-68"}
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
      http:

  opencensus:

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
      thrift_binary:
      thrift_compact:
      thrift_http:

  zipkin:

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
  logging:
    verbosity: detailed

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [logging]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand %}}

---
