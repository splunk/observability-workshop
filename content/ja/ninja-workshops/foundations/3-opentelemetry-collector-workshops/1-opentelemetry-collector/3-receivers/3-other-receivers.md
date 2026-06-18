---
title: OpenTelemetry Collector レシーバー
linkTitle: 3. その他のレシーバー
weight: 3
---

## その他のレシーバー

デフォルト設定には、**otlp**、**opencensus**、**jaeger**、**zipkin** という他のレシーバーがあることに気づくでしょう。これらは他のソースからテレメトリデータを受信するために使用されます。このワークショップではこれらのレシーバーについては扱いませんので、そのままにしておいてください。

---

{{% expand title="{{% badge style=primary icon=star %}}**Ninja:** レシーバーを動的に作成する{{% /badge %}}" %}}

Docker コンテナ、Kubernetes Pod、SSH セッションなどの短命なタスクを監視するために、[receiver creator](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator) と [observer extensions](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/observer) を使用して、これらのサービスが起動する際に新しいレシーバーを作成できます。

## 何が必要ですか？

receiver creator とそれに関連する observer extensions の使用を開始するには、それらをコレクターのビルドマニフェストに含める必要があります。

詳細については [installation](../1-installation/) を参照してください。

## 考慮すべき事項

短命なタスクの中には、_username_ や _password_ などの追加設定が必要なものがあります。
これらの値は[環境変数](https://opentelemetry.io/docs/collector/configuration/#configuration-environment-variables)で参照するか、
`${file:./path/to/database/password}` のようなスキーム展開構文を使用できます。
この方法を採用する際は、組織のシークレット管理のプラクティスに従ってください。

## Ninja ゾーン

この Ninja ゾーンに必要なものは2つだけです

1. receiver creator と observer extensions がビルダーマニフェストに追加されていることを確認します。
2. 検出されたエンドポイントに対してマッチングに使用できる設定を作成します。

テンプレート化された設定を作成するには、以下のようにします

```yaml
receiver_creator:
  watch_observers: [host_observer]
  receivers:
    redis:
      rule: type == "port" && port == 6379
      config:
        password: ${env:HOST_REDIS_PASSWORD}
```

その他の例については、[receiver creator の例](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator#examples)を参照してください。

{{% /expand %}}

## 設定の確認

レシーバーについて説明しましたので、設定の変更内容を確認しましょう。

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}設定を確認する{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml {lineNos="table" wrap="true" hl_lines="13-33 45"}
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

レシーバーを通じて OpenTelemetry Collector にデータがどのように入るかを確認しましたので、次にコレクターが受信したデータをどのように処理するかを見ていきましょう。

{{% notice style="warning" %}}
`/etc/otelcol-contrib/config.yaml` はまだ完成していないため、この時点ではコレクターを再起動**しないでください**。
{{% /notice %}}
