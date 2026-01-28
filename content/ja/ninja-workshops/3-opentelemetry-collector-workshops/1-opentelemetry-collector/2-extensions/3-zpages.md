---
title: OpenTelemetry Collector Extensions
linkTitle: 2.3 zPages
weight: 3
---

## zPages

[**zPages**](https://github.com/open-telemetry/opentelemetry-collector/blob/main/extension/zpagesextension/README.md) は、外部エクスポーターの代わりにインプロセスで使用できる機能です。組み込まれると、バックグラウンドでトレースとメトリクス情報を収集・集約し、リクエストされたときにウェブページでこのデータを提供します。zPages は、Collector が期待どおりに動作していることを確認するための非常に便利な診断機能です。

{{< tabs >}}
{{% tab title="ServiceZ" %}}

**ServiceZ** は、Collector サービスの概要と、pipelinez、extensionz、featurez の各 zPages へのクイックアクセスを提供します。このページには、ビルド情報とランタイム情報も表示されます。

サンプル URL: [**http://localhost:55679/debug/servicez**](http://localhost:55679/debug/servicez)（`localhost` をご自身の環境に合わせて変更してください）。

![ServiceZ](../../images/servicez.png)

{{% /tab %}}
{{% tab title="PipelineZ" %}}

**PipelineZ** は、Collector で実行されているパイプラインに関する洞察を提供します。タイプ、データが変更されるかどうかの情報を確認でき、各パイプラインで使用されているレシーバー、プロセッサー、エクスポーターの情報も確認できます。

サンプル URL: [**http://localhost:55679/debug/pipelinez**](http://localhost:55679/debug/pipelinez)（`localhost` をご自身の環境に合わせて変更してください）。

![PipelineZ](../../images/pipelinez.png)

{{% /tab %}}
{{% tab title="ExtensionZ" %}}

**ExtensionZ** は、Collector でアクティブな拡張機能を表示します。

サンプル URL: [**http://localhost:55679/debug/extensionz**](http://localhost:55679/debug/extensionz)（`localhost` をご自身の環境に合わせて変更してください）。

![ExtensionZ](../../images/extensionz.png)

{{% /tab %}}
{{% /tabs %}}

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** storage 拡張機能でデータの耐久性を向上させる{{% /badge %}}" %}}

このためには、使用しているディストリビューションに `file_storage` 拡張機能がインストールされていることを確認する必要があります。これは、`otelcol-contrib components` コマンドを実行することで確認でき、以下のような結果が表示されるはずです

{{< tabs >}}
{{% tab title="Truncated Output" %}}

```yaml
# ... truncated for clarity
extensions:
  - file_storage
```

{{% /tab %}}
{{% tab title="Full Output" %}}

```yaml
buildinfo:
    command: otelcol-contrib
    description: OpenTelemetry Collector Contrib
    version: 0.80.0
receivers:
    - prometheus_simple
    - apache
    - influxdb
    - purefa
    - purefb
    - receiver_creator
    - mongodbatlas
    - vcenter
    - snmp
    - expvar
    - jmx
    - kafka
    - skywalking
    - udplog
    - carbon
    - kafkametrics
    - memcached
    - prometheus
    - windowseventlog
    - zookeeper
    - otlp
    - awsecscontainermetrics
    - iis
    - mysql
    - nsxt
    - aerospike
    - elasticsearch
    - httpcheck
    - k8sobjects
    - mongodb
    - hostmetrics
    - signalfx
    - statsd
    - awsxray
    - cloudfoundry
    - collectd
    - couchdb
    - kubeletstats
    - jaeger
    - journald
    - riak
    - splunk_hec
    - active_directory_ds
    - awscloudwatch
    - sqlquery
    - windowsperfcounters
    - flinkmetrics
    - googlecloudpubsub
    - podman_stats
    - wavefront
    - k8s_events
    - postgresql
    - rabbitmq
    - sapm
    - sqlserver
    - redis
    - solace
    - tcplog
    - awscontainerinsightreceiver
    - awsfirehose
    - bigip
    - filelog
    - googlecloudspanner
    - cloudflare
    - docker_stats
    - k8s_cluster
    - pulsar
    - zipkin
    - nginx
    - opencensus
    - azureeventhub
    - datadog
    - fluentforward
    - otlpjsonfile
    - syslog
processors:
    - resource
    - batch
    - cumulativetodelta
    - groupbyattrs
    - groupbytrace
    - k8sattributes
    - experimental_metricsgeneration
    - metricstransform
    - routing
    - attributes
    - datadog
    - deltatorate
    - spanmetrics
    - span
    - memory_limiter
    - redaction
    - resourcedetection
    - servicegraph
    - transform
    - filter
    - probabilistic_sampler
    - tail_sampling
exporters:
    - otlp
    - carbon
    - datadog
    - f5cloud
    - kafka
    - mezmo
    - skywalking
    - awsxray
    - dynatrace
    - loki
    - prometheus
    - logging
    - azuredataexplorer
    - azuremonitor
    - instana
    - jaeger
    - loadbalancing
    - sentry
    - splunk_hec
    - tanzuobservability
    - zipkin
    - alibabacloud_logservice
    - clickhouse
    - file
    - googlecloud
    - prometheusremotewrite
    - awscloudwatchlogs
    - googlecloudpubsub
    - jaeger_thrift
    - logzio
    - sapm
    - sumologic
    - otlphttp
    - googlemanagedprometheus
    - opencensus
    - awskinesis
    - coralogix
    - influxdb
    - logicmonitor
    - signalfx
    - tencentcloud_logservice
    - awsemf
    - elasticsearch
    - pulsar
extensions:
    - zpages
    - bearertokenauth
    - oidc
    - host_observer
    - sigv4auth
    - file_storage
    - memory_ballast
    - health_check
    - oauth2client
    - awsproxy
    - http_forwarder
    - jaegerremotesampling
    - k8s_observer
    - pprof
    - asapclient
    - basicauth
    - headers_setter
```

{{% /tab %}}
{{< /tabs >}}

この拡張機能は、エクスポーターが設定されたエンドポイントにデータを送信できない場合に、エクスポーターがデータをディスクにキューイングする機能を提供します。

拡張機能を設定するには、以下の情報を含めるように設定を更新する必要があります。まず、/tmp/otel-data ディレクトリを作成し、読み書き権限を付与してください

```yaml
extensions:
...
  file_storage:
    directory: /tmp/otel-data
    timeout: 10s
    compaction:
      directory: /tmp/otel-data
      on_start: true
      on_rebound: true
      rebound_needed_threshold_mib: 5
      rebound_trigger_threshold_mib: 3

# ... truncated for clarity

service:
  extensions: [health_check, pprof, zpages, file_storage]
```

## なぜデータをディスクにキューイングするのか？

これにより、Collector はネットワークの中断（さらには Collector の再起動）を乗り越えて、データがアップストリームプロバイダーに送信されることを保証できます。

## データをディスクにキューイングする際の考慮事項

ディスクのパフォーマンスにより、データスループットのパフォーマンスに影響を与える可能性があります。

### 参考資料

1. [https://community.splunk.com/t5/Community-Blog/Data-Persistence-in-the-OpenTelemetry-Collector/ba-p/624583](https://community.splunk.com/t5/Community-Blog/Data-Persistence-in-the-OpenTelemetry-Collector/ba-p/624583)
2. [https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage)

{{% /expand %}}

---

## 設定の確認

拡張機能について学んだので、設定の変更を確認しましょう。

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}設定を確認する{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml { lineNos="table" wrap="true" hl_lines="5" }
# See https://github.com/open-telemetry/opentelemetry-collector/blob/main/docs/security-best-practices.md#safeguards-against-denial-of-service-attacks

extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679

receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  opencensus:
    endpoint: 0.0.0.0:55678

  # Collect own metrics
  prometheus:
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

拡張機能について確認したので、次はワークショップのデータパイプライン部分に進みましょう。パイプラインは、Collector 内でデータが辿る経路を定義し、受信から始まり、さらなる処理や変更を経て、最終的にエクスポーターを通じて Collector を出ていきます。

OpenTelemetry Collector のデータパイプラインは、**レシーバー**、**プロセッサー**、**エクスポーター**で構成されています。まずはレシーバーから始めます。
