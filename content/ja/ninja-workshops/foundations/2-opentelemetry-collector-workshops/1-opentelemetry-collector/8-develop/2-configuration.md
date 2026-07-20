---
title: OpenTelemetry Collector 開発
linkTitle: 8.2 Configuration
weight: 10 
---

## コンフィギュレーションの構築

コンポーネントのコンフィギュレーション部分は、ユーザーがコンポーネントに対して入力を行う方法です。そのため、コンフィギュレーションに使用される値は以下の条件を満たす必要があります。

1. そのフィールドが何を制御するかをユーザーが直感的に理解できること
1. 何が必須で何がオプションかを明示すること
1. 共通の名前やフィールドを再利用すること
1. オプションをシンプルに保つこと

{{% tabs %}}
{{% tab title="悪い設定例" %}}

```yaml
---
jenkins_server_addr: hostname
jenkins_server_api_port: 8089
interval: 10m
filter_builds_by:
    - name: my-awesome-build
      status: amber
track:
    values:
        example.metric.1: yes
        example.metric.2: yes
        example.metric.3: no
        example.metric.4: no
```

{{% /tab %}}
{{% tab title="良い設定例" %}}

``` yaml
---
# Required Values
endpoint: http://my-jenkins-server:8089
auth:
    authenticator: basicauth/jenkins
# Optional Values
collection_interval: 10m
metrics:
    example.metric.1:
        enabled: true
    example.metric.2:
        enabled: true
    example.metric.3:
        enabled: true
    example.metric.4:
        enabled: true
```

{{% /tab %}}
{{% /tabs %}}

悪い設定例は、コンフィギュレーションのベストプラクティスの逆を行うとコンポーネントの使いやすさにどのような影響を与えるかを示しています。フィールドの値が何であるべきかが明確でなく、既存のProcessorに委ねるべき機能が含まれており、フィールドの命名がCollectorに存在する他のコンポーネントと一貫していません。

良い設定例は、必須値をシンプルに保ち、他のコンポーネントのフィールド名を再利用し、JenkinsとCollector間のインタラクションだけに焦点を当てています。

コードタブは、私たちが追加する必要がある部分と、Collector内の共有ライブラリによって既に提供されている部分を示しています。これらについてはビジネスロジックに入った際により詳しく説明します。コンフィギュレーションは小さく始め、ビジネスロジックに追加機能が必要になった時点で変更していきます。

## コードを書く

コンフィギュレーションに必要なコードを実装するために、以下の内容で `config.go` という新しいファイルを作成します。

``` go
package jenkinscireceiver

import (
    "go.opentelemetry.io/collector/config/confighttp"
    "go.opentelemetry.io/collector/receiver/scraperhelper"

    "splunk.conf/workshop/example/jenkinscireceiver/internal/metadata"
)

type Config struct {
    // HTTPClientSettings contains all the values
    // that are commonly shared across all HTTP interactions
    // performed by the collector.
    confighttp.HTTPClientSettings `mapstructure:",squash"`
    // ScraperControllerSettings will allow us to schedule 
    // how often to check for updates to builds.
    scraperhelper.ScraperControllerSettings `mapstructure:",squash"`
    // MetricsBuilderConfig contains all the metrics
    // that can be configured.
    metadata.MetricsBuilderConfig `mapstructure:",squash"`
}
```
