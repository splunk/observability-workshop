---
title: OpenTelemetry Collector エクステンション
linkTitle: 2.3 zPages
weight: 3
---

## zPages エクステンション

[**zPages**](https://github.com/open-telemetry/opentelemetry-collector/blob/main/extension/zpagesextension/README.md) は、外部エクスポータに代わるプロセス内部の機能です。有効化すると、バックグラウンドでトレースとメトリクス情報を収集し、集計し、どのようなデータを扱ったかの Web ページを公開します。zpages は、コレクターが期待どおりに動作していることを確認するための非常に便利な診断機能です。

{{< tabs >}}
{{% tab title="ServiceZ" %}}

**ServiceZ** は、コレクターサービスの概要と、pipelinez、extensionz、featurez zPages へのクイックアクセスを提供します。このページでは、ビルドとランタイムの情報も提供します。

URL: [http://localhost:55679/debug/servicez](http://localhost:55679/debug/servicez) (`localhost` は、適切なホスト名に切り替えてください)

![ServiceZ](../../images/servicez.png)

{{% /tab %}}
{{% tab title="PipelineZ" %}}

**PipelineZ** は、コレクターで実行中のパイプラインに関する情報を提供します。タイプ、データが変更されているか、各パイプラインで使用されているレシーバー、プロセッサー、エクスポーターの情報を見ることができます。

URL: [http://localhost:55679/debug/pipelinez](http://localhost:55679/debug/pipelinez) (`localhost` は、適切なホスト名に切り替えてください)

![PipelineZ](../../images/pipelinez.png)

{{% /tab %}}
{{% tab title="ExtensionZ" %}}

**ExtensionZ** は、コレクターで有効化されたエクステンションを確認できます。

Example URL: [http://localhost:55679/debug/extensionz](http://localhost:55679/debug/extensionz) (`localhost` は、適切なホスト名に切り替えてください)

![ExtensionZ](../../images/extensionz.png)

{{% /tab %}}
{{% /tabs %}}

{{% notice style="info" %}}
ついていけない場合は、ブラウザーでzPagesの情報を発信しているテスト環境にアクセスしてください：

- **ServiceZ:** [http://63.33.64.193:55679/debug/servicez](http://63.33.64.193:55679/debug/servicez)
- **PipelineZ:** [http://63.33.64.193:55679/debug/pipelinez](http://63.33.64.193:55679/debug/pipelinez)
- **ExtensionZ:** [http://63.33.64.193:55679/debug/extensionz](http://63.33.64.193:55679/debug/extensionz)
{{% /notice %}}

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** storage エクステンションでデータの耐久性を向上させる{{% /badge %}}" %}}

これをこなうには、ディストリビューションに `file_storage` エクステンションモジュールがインストールされていることを確認する必要があります。確認するには、`otelcol-contrib components` コマンドを実行します: 

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

このエクステンションは、エクスポーターが設定されたエンドポイントにデータを送信できない事象が発生したときに、データをディスクにキューイングする機能をエクスポーターに提供します。

このエクステンションを設定するには、以下の情報を含むように設定を更新する必要があります。まず、 /tmp/otel-data ディレクトリを作成し、読み取り/書き込み権限を与えてください：

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

## なぜキューデータをディスクに書くの？

コレクターはネットワークの不調（および、コレクターの再起動）を乗り切って、アップストリームプロバイダーに確実にデータを送信できるようになります。

## キューデータをディスクに書く時の注意事項は？

ディスクの性能により、データスループットの性能に影響を与える可能性があります

### 参照

1. [https://community.splunk.com/t5/Community-Blog/Data-Persistence-in-the-OpenTelemetry-Collector/ba-p/624583](https://community.splunk.com/t5/Community-Blog/Data-Persistence-in-the-OpenTelemetry-Collector/ba-p/624583)
2. [https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage)

{{% /expand %}}

---

## 設定を確認しましょう

さて、エクステンションについて説明したので、設定の変更箇所を確認していきましょう。

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}設定ファイルを確認してください{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml { lineNos="table" wrap="true" hl_lines="3" }
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
      http:

  opencensus:

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
      receivers: [otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [logging]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand %}}

---

さて、エクステンションについて復習したところで、ワークショップのデータパイプラインの部分に飛び込んでみましょう。パイプラインとは、コレクター内でデータがたどる経路を定義するもので、レシーバーから始まり、追加の処理や変更をし、最終的にエクスポーターを経由してコレクターを出ます。

OpenTelemetry Collector のデータパイプラインは、レシーバー、プロセッサー、エクスポーターで構成されています。まずは、レシーバーから見ていきましょう。
