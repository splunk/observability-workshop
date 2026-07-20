---
title: OpenTelemetry Collector Service
linkTitle: 6.5 OTLP HTTP
weight: 5
---

## OTLP HTTP Exporter

ワークショップのExporterセクションで、Splunk Observability Cloudにメトリクスを送信するための `otlphttp` Exporterを設定しました。次に、メトリクスパイプラインでこれを有効にする必要があります。

`metrics` パイプラインの `exporters` セクションに `otlphttp/splunk` を追加します:

```yaml {hl_lines="13"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf]
      exporters: [debug, otlphttp/splunk]
```

---

{{% expand title="{{% badge style=primary icon=star %}}**Ninja:** Collectorの内部観測{{% /badge %}}" %}}

Collectorは自身の動作に関する内部シグナルをキャプチャします。これには実行中のコンポーネントからの追加シグナルも含まれます。これは、データフローに関する意思決定を行うコンポーネントが、その情報をメトリクスやトレースとして表面化する手段を必要とするためです。

## なぜCollectorをモニタリングするのか？

これは「誰が監視者を監視するのか？」という鶏と卵の問題に近いですが、この情報を表面化できることは重要です。Collectorの歴史において興味深い点は、GoのメトリクスSDKが安定版と見なされる前から存在していたため、当面の間はPrometheusエンドポイントを公開してこの機能を提供していることです。

## 考慮事項

組織内で実行されている各Collectorの内部使用状況をモニタリングすると、大量の新しいMetric Time Series（MTS）が発生する可能性があります。Splunkディストリビューションではこれらのメトリクスを厳選しており、予想される増加量の予測を支援できます。

## The Ninja Zone

Collectorの内部オブザーバビリティを公開するために、いくつかの追加設定を調整できます:

{{< tabs >}}
{{% tab title="telemetry schema" %}}

```yaml
service:
  telemetry:
    logs:
      level: <info|warn|error>
      development: <true|false>
      encoding: <console|json>
      disable_caller: <true|false>
      disable_stacktrace: <true|false>
      output_paths: [<stdout|stderr>, paths...]
      error_output_paths: [<stdout|stderr>, paths...]
      initial_fields:
        key: value
    metrics:
      level: <none|basic|normal|detailed>
      # Address binds the promethues endpoint to scrape
      address: <hostname:port>
```

{{% /tab %}}
{{% tab title="example-config.yml" %}}

```yaml
service:
  telemetry:
    logs: 
      level: info
      encoding: json
      disable_stacktrace: true
      initial_fields:
        instance.name: ${env:INSTANCE}
    metrics:
      address: localhost:8888 
```

{{% /tab %}}
{{< /tabs >}}

## 参考資料

1. [https://opentelemetry.io/docs/collector/configuration/#service](https://opentelemetry.io/docs/collector/configuration/#service)

{{% /expand %}}

## 最終設定

{{% expand title="最終設定を確認する" %}}

{{< tabs >}}
{{% tab title="config.yaml" %}}

``` yaml {lineNos="table" wrap="true"}
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
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp
    headers:
      X-SF-Token: ${env:ACCESS_TOKEN}

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf]
      exporters: [debug, otlphttp/splunk]

    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{% /tabs %}}

{{% /expand %}}

{{% notice style="tip" %}}
Collectorを再起動する前に、設定ファイルを検証することを推奨します。`config.yaml` ファイルの内容を **[otelbin.io](https://www.otelbin.io/)** に貼り付けることで検証できます。

{{% expand title="**スクリーンショット**: OTelBin" %}}
![otelbin-validator](../../images/otelbin.png)
{{% /expand %}}

{{% /notice %}}

設定が完成したので、Collectorを起動し、[zPages](../2-extensions/#zpages)が何を報告しているか確認しましょう。

{{% tab title="Command" %}}

``` bash
otelcol-contrib --config=file:/etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

ブラウザでzPagesを開きます: [**http://localhost:55679/debug/pipelinez**](http://localhost:55679/debug/pipelinez)（`localhost` はご自身の環境に合わせて変更してください）。
![pipelinez-full-config](../../images/pipelinez-full-config.png)
