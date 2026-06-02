---
title: OpenTelemetry Collector Development
linkTitle: 8.4 Designing the Metrics 
weight: 12
---

### メトリクスの設計

レシーバーで収集するメトリクスを定義してエクスポートしやすくするため、[**mdatagen**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/mdatagen) を使用します。これは、YAML で定義したメトリクスをコードに変換するために Collector 向けに開発されたツールです。

{{% tabs %}}
{{% tab title="metadata.yaml"%}}

``` yaml
---
# Type defines the name to reference the component
# in the configuration file
type: jenkins

# Status defines the component type and the stability level
status:
  class: receiver
  stability:
    development: [metrics]

# Attributes are the expected fields reported
# with the exported values.
attributes:
  job.name:
    description: The name of the associated Jenkins job
    type: string
  job.status:
    description: Shows if the job had passed, or failed
    type: string
    enum:
    - failed
    - success
    - unknown

# Metrics defines all the pontentially exported values from this receiver. 
metrics:
  jenkins.jobs.count:
    enabled: true
    description: Provides a count of the total number of configured jobs
    unit: "{Count}"
    gauge:
      value_type: int
  jenkins.job.duration:
    enabled: true
    description: Show the duration of the job
    unit: "s"
    gauge:
      value_type: int
    attributes:
    - job.name
    - job.status
  jenkins.job.commit_delta:
    enabled: true
    description: The calculation difference of the time job was finished minus commit timestamp
    unit: "s"
    gauge:
      value_type: int
    attributes:
    - job.name
    - job.status
```

{{% /tab %}}
{{% tab title="gen.go" %}}

``` go
// To generate the additional code needed to capture metrics, 
// the following command to be run from the shell:
//  go generate -x ./...

//go:generate go run github.com/open-telemetry/opentelemetry-collector-contrib/cmd/mdatagen@v0.80.0 metadata.yaml
package jenkinscireceiver

// There is no code defined within this file.
```

{{% /tab%}}
{{% /tabs %}}

次のセクションに進む前に、これらのファイルをプロジェクトフォルダ内に作成してください。

## Factory の構築

Factory は、提供された設定に基づいてオブジェクト（このケースでは `jenkinscireceiver`）を動的に生成できるようにするソフトウェアデザインパターンです。より身近な例で説明すると、携帯電話ショップに行き、自分の希望に合った電話を伝え、それを店員から渡してもらうようなものです。

`go generate -x ./...` コマンドを実行すると、新しいフォルダ `jenkinscireceiver/internal/metadata` が作成され、定義されたメトリクスをエクスポートするために必要なすべてのコードが生成されます。必要なコードは次のとおりです。

{{% tabs %}}
{{% tab title="factory.go" %}}

``` go
package jenkinscireceiver

import (
    "errors"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/config/confighttp"
    "go.opentelemetry.io/collector/receiver"
    "go.opentelemetry.io/collector/receiver/scraperhelper"

    "splunk.conf/workshop/example/jenkinscireceiver/internal/metadata"
)

func NewFactory() receiver.Factory {
    return receiver.NewFactory(
        metadata.Type,
        newDefaultConfig,
        receiver.WithMetrics(newMetricsReceiver, metadata.MetricsStability),
    )
}

func newMetricsReceiver(_ context.Context, set receiver.CreateSettings, cfg component.Config, consumer consumer.Metrics) (receiver.Metrics, error) {
    // Convert the configuration into the expected type
    conf, ok := cfg.(*Config)
    if !ok {
        return nil, errors.New("can not convert config")
    }
    sc, err := newScraper(conf, set)
    if err != nil {
        return nil, err
    }
    return scraperhelper.NewScraperControllerReceiver(
        &conf.ScraperControllerSettings,
        set,
        consumer,
        scraperhelper.AddScraper(sc),
    )
}
```

{{% /tab %}}
{{% tab title="config.go" %}}

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

func newDefaultConfig() component.Config {
    return &Config{
        ScraperControllerSettings: scraperhelper.NewDefaultScraperControllerSettings(metadata.Type),
        HTTPClientSettings:        confighttp.NewDefaultHTTPClientSettings(),
        MetricsBuilderConfig:      metadata.DefaultMetricsBuilderConfig(),
    }
}
```

{{% /tab %}}
{{% tab title="scraper.go" %}}

``` go
package jenkinscireceiver

type scraper struct {}

func newScraper(cfg *Config, set receiver.CreateSettings) (scraperhelper.Scraper, error) {
    // Create a our scraper with our values 
    s := scraper{
        // To be filled in later
    }
    return scraperhelper.NewScraper(metadata.Type, s.scrape)
}

func (scraper) scrape(ctx context.Context) (pmetric.Metrics, error) {
    // To be filled in
    return pmetrics.NewMetrics(), nil
}
```

{{% /tab %}}
{{% tab title="build-config.yaml" %}}

``` yaml
---
dist:
  name: otelcol
  description: "Conf workshop collector"
  output_path: ./dist
  version: v0.0.0-experimental

extensions:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/basicauthextension v0.80.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/healthcheckextension v0.80.0

receivers:
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.80.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/jaegerreceiver v0.80.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/prometheusreceiver v0.80.0
  - gomod: splunk.conf/workshop/example/jenkinscireceiver v0.0.0
    path: ./jenkinscireceiver

processors:
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.80.0

exporters:
  - gomod: go.opentelemetry.io/collector/exporter/loggingexporter v0.80.0
  - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.80.0
  - gomod: go.opentelemetry.io/collector/exporter/otlphttpexporter v0.80.0

# This replace is a go directive that allows for redefine
# where to fetch the code to use since the default would be from a remote project.
replaces:
- splunk.conf/workshop/example/jenkinscireceiver => ./jenkinscireceiver
```

{{% /tab %}}
{{% tab title="project layout" %}}

``` text
├── build-config.yaml
└── jenkinscireceiver
    ├── go.mod
    ├── config.go
    ├── factory.go
    ├── scraper.go
    └── internal
      └── metadata
```

{{% /tab %}}
{{% /tabs %}}

これらのファイルを期待される内容でプロジェクトに書き込んだら、`go mod tidy` を実行してください。これによりすべてのリモート依存関係が取得され、`go.mod` が更新されて `go.sum` ファイルが生成されます。
