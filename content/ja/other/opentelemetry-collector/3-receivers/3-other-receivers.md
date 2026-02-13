---
title: OpenTelemetry Collector レシーバー
linkTitle: 3. その他のレシーバー
weight: 3
---

## その他のレシーバー

デフォルトの設定には、他のレシーバーがあることに気づくはずです。 **[otlp](https://github.com/open-telemetry/opentelemetry-collector/blob/main/receiver/otlpreceiver)**、**[opencensus](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/opencensusreceiver)**、**[jaeger](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/jaegerreceiver)**、**[zipkin](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/zipkinreceiver)** が定義されています。これらは他のソースからテレメトリーデータを受信するために使われます。このワークショップでは、これらのレシーバーについては取り上げませんので、そのままにしておきましょう。

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** レシーバーを動的に生成する{{% /badge %}}" %}}

dockerコンテナ、kubernetesポッド、sshセッションのような短時間のタスクを観測するために、[receiver creator](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator) レシーバーと [observer](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/observer) エクステンションを使って、対象のサービスが起動するタイミングで新しいレシーバーを作成することができます。

## 何が必要なの？

receiver creatorとそれに関連するobserverエクステンションの使用を開始するには、collector build manifestに追加する必要があります。

詳細は [installation](../1-installation/) を参照してください。

## 注意事項はある？

短命なタスクの中には、_username_ や _password_ のような追加設定を必要とするものがあります。それらの値は[環境変数](https://opentelemetry.io/docs/collector/configuration/#configuration-environment-variables) を参照したり、 `${file:./path/to/database/password}` のようなスキーム展開構文を使うこともできます。

組織における機密情報の取り扱い規定に従って、どのような方法を取るかを検討してください。

## Ninja ゾーン

このNinjaゾーンに必要なものは2つだけです:

1. builder manifestに、 receiver creatorレシーバーとobserverエクステンションを追加する
2. 検出されたエンドポイントを検出するように、設定を作成する

次のようにすると、設定をテンプレート化できます:

```yaml
receiver_creator:
  watch_observers: [host_observer]
  receivers:
    redis:
      rule: type == "port" && port == 6379
      config:
        password: ${env:HOST_REDIS_PASSWORD}
```

他の例は [receiver creator's examples](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator#examples) にあります。

{{% /expand %}}

---

## 設定を確認しましょう

これで、レシーバーをカバーできました。ここで、設定のの変更内容をチェックしてみましょう。

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}設定をレビューしてください{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml {lineNos="table" wrap="true" hl_lines="10-30 39"}
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
      receivers: [otlp, opencensus, prometheus/internal]
      processors: [batch]
      exporters: [logging]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand %}}

---

これで、レシーバーを通してOpenTelemetry Collectorにデータがどのように取り込まれるかを確認しました。次に、コレクターが受信したデータをどのように処理するかを見てみましょう。

{{% notice style="warning" %}}
**ここではコレクターを再起動しないでください**！　 `/etc/otelcol-contrib/config.yaml` の変更はまだ完了していません。
{{% /notice %}}
