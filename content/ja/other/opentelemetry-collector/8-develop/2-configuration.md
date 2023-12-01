---
title: OpenTelemetry Collector を開発する
linkTitle: 8.2 Configuration
weight: 10 
---

## Configuration の構築

コンポーネントの Configuration 部分は、ユーザーがコンポーネントに対する入力を行う方法であり、設定に使用される値は以下のようである必要があります：

1. そのフィールドが何を制御するのか、ユーザーが直感的に理解できる
1. 必須項目とオプション項目が明確である
1. 共通の名前とフィールドを再利用する
1. オプションをシンプルに保つ

{{% tabs %}}
{{% tab title="良い config" %}}

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
{{% tab title="悪い config" %}}

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
{{% /tabs %}}

悪い例では、Configuration のベストプラクティスに反するとコンポーネントが使いにくくなってしまうことが理解できるはずです。
フィールドの値が何であるべきかを明確ではなく、既存のプロセッサーに移譲できる機能を含み、コレクター内の他のコンポーネントと比較してフィールドの命名に一貫性がありません。

良い例では、必要な値をシンプルに保ち、他のコンポーネントからのフィールド名を再利用し、コンポーネントが Jenkins とコレクター間の相互作用にのみ焦点を当てています。

設定値の中には、このコンポーネントで独自に追加するものと、コレクター内部の共有ライブラリによって提供されているものがあります。これらはビジネスロジックに取り組む際にさらに詳しく説明します。Configuration は小さく始めるべきで、ビジネスロジックに追加の機能が必要になったら、設定も追加していきましょう。

## コードを書く

Configuration に必要なコードを実装するために、`config.go` という名前の新しいファイルを以下の内容で作成します：

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
