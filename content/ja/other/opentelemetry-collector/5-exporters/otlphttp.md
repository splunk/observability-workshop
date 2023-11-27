---
title: OpenTelemetry Collector エクスポーター
linkTitle: 5.1 OTLP HTTP
weight: 1
---

## OTLP HTTP エクスポーター

Splunk Observability Cloud へ HTTP 経由でメトリックスを送信するためには、**otlphttp** エクスポーターを設定する必要があります。

`/etc/otelcol-contrib/config.yaml` ファイルを編集し、**otlphttp** エクスポーターを設定しましょう。以下の YAML を **exporters** セクションの下に挿入し、例えば2スペースでインデントしてください。

また、ディスクの容量不足を防ぐために、ロギングエクスポーターの詳細度を変更します。デフォルトの `detailed` は非常に詳細です。

```yaml {hl_lines="3-4"}
exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
```

次に、`metrics_endpoint` を定義して、ターゲットURLを設定していきます。

{{% notice style="note" %}}
Splunk 主催のワークショップの参加者である場合、使用しているインスタンスにはすでに Realm 環境変数が設定されています。その環境変数を設定ファイルで参照します。それ以外の場合は、新しい環境変数を作成して Realm を設定する必要があります。例えば：

``` bash
export REALM="us1"
```

{{% /notice %}}

使用するURLは `https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp` です。（Splunkは、データの居住地に応じて世界中の主要地域に Realm を持っています）。

**otlphttp** エクスポーターは、`traces_endpoint` と `logs_endpoint` それぞれのターゲットURLを定義することにより、トレースとログを送信するようにも設定できますが、そのような設定はこのワークショップの範囲外とします。

```yaml {hl_lines="5"}
exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp
```

デフォルトでは、すべてのエンドポイントで `gzip` 圧縮が有効になっています。エクスポーターの設定で `compression: none` を設定することにより、圧縮を無効にすることができます。このワークショップでは圧縮を有効にしたままにし、データを送信する最も効率的な方法としてデフォルト設定を使っていきます。

Splunk Observability Cloud にメトリクスを送信するためには、アクセストークンを使用する必要があります。これは、Splunk Observability Cloud UI で新しいトークンを作成することにより行うことができます。トークンの作成方法についての詳細は、[Create a token](https://docs.splunk.com/Observability/admin/authentication-tokens/org-tokens.html) を参照してください。トークンは **INGEST** タイプである必要があります。

{{% notice style="note" %}}
Splunk　主催のワークショップの参加者である場合、使用しているインスタンスにはすでにアクセストークンが設定されています（環境変数として設定されています）ので、その環境変数を設定ファイルで参照します。それ以外の場合は、新しいトークンを作成し、それを環境変数として設定する必要があります。例えば：

``` bash
export ACCESS_TOKEN=<replace-with-your-token>
```

{{% /notice %}}

トークンは、設定ファイル内で `headers:` セクションの下に `X-SF-TOKEN: ${env:ACCESS_TOKEN}` を挿入することにで定義します：

```yaml {hl_lines="6-8"}
exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp
    headers:
      X-SF-TOKEN: ${env:ACCESS_TOKEN}
```

## 設定を確認しましょう

これで、エクスポーターもカバーできました。設定を確認していきましょう：
Now that we've covered exporters, let's check our configuration changes:

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}設定をレビューしてください{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml {lineNos="table" wrap="true" hl_lines="72-76"}
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
      receivers: [otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [logging]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand %}}

---

もちろん、**OTLP** プロトコルをサポートする他のソリューションを指すように `metrics_endpoint` を簡単に設定することができます。

次に、`config.yaml` のサービスセクションで、今設定したレシーバー、プロセッサー、エクスポーターを有効にしていきます。
