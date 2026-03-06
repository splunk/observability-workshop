---
title: OpenTelemetry Collector サービス
linkTitle: 6.5 OTLP HTTP
weight: 5
---

## OTLP HTTP エクスポーター

ワークショップのエクスポーターセクションでは、`otlphttp` エクスポーターを設定して、メトリクスをSplunk Observability Cloudに送信するようにしました。これをメトリクスパイプライン下で有効にする必要があります。

`metrics` パイプラインの下の `exporters` セクションを更新して、`otlphttp/splunk` を追加します

```yaml {hl_lines="13"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf]
      exporters: [logging, otlphttp/splunk]
```

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** コレクターの内部を観測する{{% /badge %}}" %}}

コレクターは、その動作に関する内部シグナルを捕捉しています。これには実行中のコンポーネントからの追加されるシグナルも含まれます。これは、データの流れに関する決定を行うコンポーネントが、その情報をメトリクスやトレースとして表面化する方法を必要とするためです。

## なぜコレクターを監視するの？

これは「監視者を監視するのは誰か？」という種類の問題ですが、このような情報を表面化できることは重要です。コレクターの歴史の興味深い部分は、GoメトリクスのSDKが安定と考えられる前に存在していたことで、コレクターは当面の間、この機能を提供するためにPrometheusエンドポイントを公開しています。

## 注意点

組織内で稼働している各コレクターの内部使用状況を監視することは、新しいメトリクス量（MTS）を大幅な増加させる可能性があります。Splunkディストリビューションはこれらのメトリクスをキュレーションしており、増加を予測するのに役立ちます。

## Ninja ゾーン

コレクターの内部オブザーバビリティを公開するためには、いくつかの設定を追加することがあります

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

## 参照

1. [https://opentelemetry.io/docs/collector/configuration/#service](https://opentelemetry.io/docs/collector/configuration/#service)

{{% /expand %}}

---

## 完成した設定

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}完成した設定をレビューしてください{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

``` yaml {lineNos="table" wrap="true" hl_lines="88-90"}
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
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp
    headers:
      X-SF-TOKEN: ${env:ACCESS_TOKEN}

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf] 
      exporters: [logging, otlphttp/splunk]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{% /tabs %}}

{{% /expand %}}

---

{{% notice style="tip" %}}
コレクターを再起動する前に、設定ファイルを検証することをお勧めします。これは、組み込みの `validate` コマンドを使用して行うことができます

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
otelcol-contrib validate --config=file:/etc/otelcol-contrib/config.yaml
```

{{% /tab %}}
{{% tab title="Example error output" %}}

``` text
Error: failed to get config: cannot unmarshal the configuration: 1 error(s) decoding:

* error decoding 'processors': error reading configuration for "attributes/conf": 1 error(s) decoding:

* 'actions[0]' has invalid keys: actions
2023/06/29 09:41:28 collector server run finished with error: failed to get config: cannot unmarshal the configuration: 1 error(s) decoding:

* error decoding 'processors': error reading configuration for "attributes/conf": 1 error(s) decoding:

* 'actions[0]' has invalid keys: actions
```

{{% /tab %}}
{{< /tabs >}}
{{% /notice %}}

動作する設定ができたので、コレクターを起動し、その後 [zPages](../2-extensions/#zpages) が報告している内容を確認しましょう。

{{% tab title="Command" %}}

``` bash
sudo systemctl restart otelcol-contrib
```

{{% /tab %}}

![pipelinez-full-config](../../images/pipelinez-full-config.png)
