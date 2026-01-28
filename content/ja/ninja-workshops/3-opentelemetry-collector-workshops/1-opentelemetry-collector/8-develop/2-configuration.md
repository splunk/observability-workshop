---
title: OpenTelemetry Collector 開発
linkTitle: 8.2 Configuration
weight: 10
---

## Configuration の構築

コンポーネントの Configuration 部分は、ユーザーがコンポーネントに対して入力を行う方法です。そのため、設定に使用される値は以下の条件を満たす必要があります

1. そのフィールドが何を制御するかをユーザーが直感的に理解できること
1. 必須と任意を明確にすること
1. 一般的な名前とフィールドを再利用すること
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

悪い設定例は、設定のベストプラクティスの逆を行うことがコンポーネントの使いやすさにどのように影響するかを示しています。フィールド値が何であるべきかが明確ではなく、既存のプロセッサにプッシュできる機能が含まれており、フィールド名が Collector に存在する他のコンポーネントと一貫していません。

良い設定例は、必須の値をシンプルに保ち、他のコンポーネントからフィールド名を再利用し、コンポーネントが Jenkins と Collector 間の相互作用のみに焦点を当てることを確保しています。

コードタブは、私たちが追加する必要がある量と、Collector 内の共有ライブラリによってすでに提供されているものを示しています。これらはビジネスロジックに到達したときにより詳細に説明します。Configuration は小さく始まり、追加機能が必要になるとビジネスロジックが含まれるようになると変更されます。

## コードを書く

Configuration に必要なコードを実装するために、以下の内容で `config.go` という新しいファイルを作成します

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
