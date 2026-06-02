---
title: OpenTelemetry Collector Exporters
linkTitle: 5.1 OTLP HTTP
weight: 1
---

## OTLP HTTP Exporter

メトリクスを HTTP 経由で Splunk Observability Cloud に送信するには、**otlphttp** exporter を設定する必要があります。

`/etc/otelcol-contrib/config.yaml` ファイルを編集して、**otlphttp** exporter を設定してみましょう。**exporters** セクションの下に、以下の YAML を 2 スペースのインデントに注意して挿入します。

また、ディスクが満杯になるのを防ぐために、logging exporter のログレベルも変更します。デフォルトの `detailed` は非常に冗長です。

```yaml {hl_lines="3-4"}
exporters:
  debug:
    verbosity: normal
  otlphttp/splunk:
```

次に、`metrics_endpoint` を定義してターゲット URL を設定する必要があります。

{{% notice style="note" %}}
Splunk 主催のワークショップに参加されている方は、使用しているインスタンスにすでに Realm 環境変数が設定されています。設定ファイルでその環境変数を参照します。それ以外の場合は、新しい環境変数を作成して Realm を設定する必要があります。例：

``` bash
export REALM="us1"
```

{{% /notice %}}

使用する URL は `https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp` です。（Splunk はデータレジデンシーのために、世界中の主要な地理的拠点に Realm を持っています。）

**otlphttp** exporter は、`traces_endpoint` と `logs_endpoint` のターゲット URL をそれぞれ定義することで、トレースとログを送信するように設定することもできます。これらの設定は本ワークショップの範囲外です。

```yaml {hl_lines="5"}
exporters:
  debug:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp
```

デフォルトでは、すべてのエンドポイントで `gzip` 圧縮が有効になっています。これは exporter の設定で `compression: none` を指定することで無効にできます。本ワークショップでは、これがデータ送信の最も効率的な方法であるため、圧縮を有効のままにしてデフォルトを採用します。

メトリクスを Splunk Observability Cloud に送信するには、Access Token を使用する必要があります。これは Splunk Observability Cloud UI で新しいトークンを作成することで行えます。トークンの作成方法の詳細については、[Create a token](https://docs.splunk.com/Observability/admin/authentication-tokens/org-tokens.html) を参照してください。トークンは **INGEST** タイプである必要があります。

{{% notice style="note" %}}
Splunk 主催のワークショップに参加されている方は、使用しているインスタンスにすでに Access Token が（環境変数として）設定されています。設定ファイルでその環境変数を参照します。それ以外の場合は、新しいトークンを作成して環境変数として設定する必要があります。例：

``` bash
export ACCESS_TOKEN=<replace-with-your-token>
```

{{% /notice %}}

トークンは、設定ファイル内で `headers:` セクションの下に `X-SF-TOKEN: ${env:ACCESS_TOKEN}` を挿入することで定義します。

```yaml {hl_lines="6-8"}
exporters:
  debug:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp
    headers:
      X-SF-TOKEN: ${env:ACCESS_TOKEN}
```

## Configuration Check-in

exporter について説明したので、設定変更を確認しましょう。

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}Review your configuration{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml {lineNos="table" wrap="true" hl_lines="83-87"}
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

もちろん、`metrics_endpoint` を **OTLP** プロトコルをサポートする他のソリューションを指すように簡単に設定することもできます。

次に、`config.yaml` の service セクションで、設定したばかりの receiver、processor、exporter を有効化する必要があります。
