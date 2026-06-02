---
title: OpenTelemetry Collector Development
linkTitle: 8.2 Configuration
weight: 10 
---

## 設定の構築

コンポーネントの設定部分は、ユーザーがコンポーネントに対して入力を与えるための手段です。
そのため、設定で使用される値は次のような特性を備えている必要があります。

1. そのフィールドが何を制御するのかをユーザーが直感的に理解できること
1. 必須項目と任意項目が明示されていること
1. 共通の名称やフィールドを再利用していること
1. オプションをシンプルに保つこと

{{% tabs %}}
{{% tab title="bad config" %}}

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
{{% tab title="good config" %}}

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

bad configuration の例は、設定に関する推奨事項とは逆のことを行うとコンポーネントの使い勝手にどのような影響を与えるかを示しています。フィールドの値がどうあるべきかが明確でなく、既存のプロセッサに任せられる機能まで含めてしまっており、フィールドの命名も collector 内の他のコンポーネントと一貫していません。

good configuration の例は、必須の値をシンプルに保ち、他のコンポーネントから命名規則を再利用し、コンポーネントが Jenkins と collector の連携のみに集中するようにしています。

コードタブは、自分たちで追加する必要のある部分と、collector 内の共有ライブラリによってすでに提供されている部分の量を示しています。これらについては、ビジネスロジックに進んだ際にさらに詳しく説明します。設定は最初は小さく始めるべきであり、ビジネスロジックで必要となる追加機能を含めていく過程で変化していきます。

## コードを書く

設定に必要なコードを実装するために、`config.go` という名前の新しいファイルを以下の内容で作成します。

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
