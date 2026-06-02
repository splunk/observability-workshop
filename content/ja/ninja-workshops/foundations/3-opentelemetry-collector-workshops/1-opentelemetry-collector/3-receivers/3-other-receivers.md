---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Other Receivers
weight: 3
---

## その他のReceiver

デフォルト設定には他にも **otlp**、**opencensus**、**jaeger**、**zipkin** といったReceiverが含まれていることに気付くでしょう。これらは他のソースからテレメトリデータを受信するために使われます。本ワークショップではこれらのReceiverは扱わないため、そのままにしておいて構いません。

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Receiverを動的に作成する{{% /badge %}}" %}}

dockerコンテナ、kubernetes pod、sshセッションなどの短命なタスクを観測するために、[receiver creator](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator) と [observer extensions](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/observer) を使って、これらのサービスが起動した際に新しいReceiverを作成することができます。

## 必要なもの

receiver creatorと関連するobserver extensionsを使い始めるには、これらをCollectorのビルドマニフェストに含める必要があります。

詳細は [installation](../1-installation/) を参照してください。

## 考慮すべきこと

短命なタスクの中には、_username_ や _password_ などの追加設定が必要になるものもあります。
これらの値は [environment variables](https://opentelemetry.io/docs/collector/configuration/#configuration-environment-variables) で参照したり、`${file:./path/to/database/password}` のようなscheme expand構文を使うことができます。
この方法を取る場合は、所属組織のシークレット管理ポリシーに従ってください。

## The Ninja Zone

このninja zoneで必要なのは2つだけです。

1. receiver createrとobserver extensionsをbuilderマニフェストに追加していることを確認する。
2. 検出されたエンドポイントとマッチングするための設定を作成する。

テンプレート化された設定を作成するには、次のようにします。

```yaml
receiver_creator:
  watch_observers: [host_observer]
  receivers:
    redis:
      rule: type == "port" && port == 6379
      config:
        password: ${env:HOST_REDIS_PASSWORD}
```

その他の例は、こちらの [receiver creator's examples](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator#examples) を参照してください。

{{% /expand %}}

---

## 設定のチェックイン

ここまででReceiverについて説明したので、設定の変更内容を確認してみましょう。

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

ReceiverによってOpenTelemetry Collectorにデータが入ってくる仕組みを確認したので、次はCollectorが受信したデータをどのように処理するかを見ていきましょう。

{{% notice style="warning" %}}
`/etc/otelcol-contrib/config.yaml` はまだ完成していないため、この時点ではCollectorを再起動 **しないでください**。
{{% /notice %}}
