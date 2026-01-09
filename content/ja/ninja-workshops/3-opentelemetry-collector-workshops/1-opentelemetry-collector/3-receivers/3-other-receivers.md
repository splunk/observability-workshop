---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Other Receivers
weight: 3
---

## その他の Receiver

デフォルト設定には、**otlp**、**opencensus**、**jaeger**、**zipkin** などの他の Receiver があることに気づくでしょう。これらは他のソースからテレメトリデータを受信するために使用されます。このワークショップではこれらの Receiver については取り上げませんので、そのままにしておいてください。

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Receiver を動的に作成する{{% /badge %}}" %}}

Docker コンテナ、Kubernetes Pod、SSH セッションなどの短期間のタスクを監視するために、[receiver creator](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator) と [observer extensions](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/observer) を使用して、これらのサービスが起動するときに新しい Receiver を作成できます。

## 何が必要ですか？

receiver creator とそれに関連する observer extension を使い始めるには、それらが Collector のビルドマニフェストに含まれている必要があります。

詳細は [installation](../1-installation/) を参照してください。

## 考慮すべき事項

一部の短期間のタスクでは、_username_ や _password_ などの追加設定が必要な場合があります。
これらの値は [環境変数](https://opentelemetry.io/docs/collector/configuration/#configuration-environment-variables) で参照するか、
`${file:./path/to/database/password}` のようなスキーム展開構文を使用できます。
この方法を採用する場合は、組織のシークレット管理のベストプラクティスに従ってください。

## Ninja ゾーン

この Ninja ゾーンに必要なことは2つだけです：

1. ビルダーマニフェストに receiver creator と observer extension が追加されていることを確認します。
2. 検出されたエンドポイントとマッチングするために使用できる設定を作成します。

テンプレート化された設定を作成するには、以下のようにします：

```yaml
receiver_creator:
  watch_observers: [host_observer]
  receivers:
    redis:
      rule: type == "port" && port == 6379
      config:
        password: ${env:HOST_REDIS_PASSWORD}
```

その他の例については、[receiver creator の例](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator#examples) を参照してください。

{{% /expand %}}

---

## 設定の確認

Receiver について説明しましたので、設定の変更を確認しましょう。

---

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

---

Receiver を通じてデータが OpenTelemetry Collector にどのように取り込まれるかを確認しました。次は、Collector が受信したデータをどのように処理するかを見ていきましょう。

{{% notice style="warning" %}}
`/etc/otelcol-contrib/config.yaml` はまだ完成していないため、この時点では Collector を再起動**しないでください**。
{{% /notice %}}
