---
title: Installing OpenTelemetry Collector Contrib
linkTitle: 1.1 Confirm Installation
weight: 1
---

## Collector が動作していることを確認する

Collector は現在動作しているはずです。`systemctl` コマンドを使って root 権限で確認します。ステータス表示を終了するには `q` を押すだけです。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo systemctl status otelcol-contrib
```

{{% /tab %}}
{{% tab title="Status Output" %}}

``` text
● otelcol-contrib.service - OpenTelemetry Collector Contrib
     Loaded: loaded (/lib/systemd/system/otelcol-contrib.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-10-07 10:27:49 BST; 52s ago
   Main PID: 17113 (otelcol-contrib)
      Tasks: 13 (limit: 19238)
     Memory: 34.8M
        CPU: 155ms
     CGroup: /system.slice/otelcol-contrib.service
             └─17113 /usr/bin/otelcol-contrib --config=/etc/otelcol-contrib/config.yaml

Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: Descriptor:
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:      -> Name: up
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:      -> Description: The scraping was successful
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:      -> Unit:
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:      -> DataType: Gauge
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: NumberDataPoints #0
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: StartTimestamp: 1970-01-01 00:00:00 +0000 UTC
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: Timestamp: 2024-10-07 09:28:36.942 +0000 UTC
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: Value: 1.000000
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:         {"kind": "exporter", "data_type": "metrics", "name": "debug"}
```

{{% /tab %}}
{{< /tabs >}}

これから複数の設定ファイルの変更や環境変数の設定、Collector の再起動を行うため、Collector サービスを停止し、起動時に自動起動しないように無効化します。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo systemctl stop otelcol-contrib && sudo systemctl disable otelcol-contrib
```

{{% /tab %}}
{{< /tabs >}}

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Open Telemetry Collector Builder (ocb) を使って独自の Collector をビルドする{{% /badge %}}" %}}
このパートでは、システムに以下のものがインストールされている必要があります。

- Golang (最新バージョン)

  ``` bash
  cd /tmp
  wget https://golang.org/dl/go1.20.linux-amd64.tar.gz
  sudo tar -C /usr/local -xzf go1.20.linux-amd64.tar.gz
  ```

  `.profile` を編集し、以下の環境変数を追加します。

  ``` bash
  export GOROOT=/usr/local/go
  export GOPATH=$HOME/go
  export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
  ```

  シェルセッションを更新します。
  
  ``` bash
  source ~/.profile
  ```

  Go のバージョンを確認します。

  ``` bash
  go version
  ```  

- ocb のインストール
  - [project releases](https://github.com/open-telemetry/opentelemetry-collector/releases/tag/cmd%2Fbuilder%2Fv0.80.0) から ocb バイナリをダウンロードし、以下のコマンドを実行します。

    ```bash
    mv ocb_0.80.0_darwin_arm64 /usr/bin/ocb
    chmod 755 /usr/bin/ocb
    ```

    別のアプローチとして、golang のツールチェインを使ってバイナリをローカルでビルドする方法もあります。

    ```bash
    go install go.opentelemetry.io/collector/cmd/builder@v0.80.0
    mv $(go env GOPATH)/bin/builder /usr/bin/ocb
    ```

- (オプション) Docker

## なぜ独自の Collector をビルドするのか?

Collector のデフォルトのディストリビューション (core および contrib) は、提供されている内容が多すぎるか、少なすぎるかのいずれかになりがちです。

また、contrib Collector は、デプロイで必要としない可能性が高いコンポーネントが多数インストールされているため、本番環境での実行は推奨されません。

## 独自の Collector をビルドするメリット

独自の Collector バイナリ (一般的にディストリビューションと呼ばれます) を作成することは、必要なものだけをビルドすることを意味します。

メリットは以下のとおりです。

1. バイナリサイズが小さくなる
2. 既存の Go の脆弱性スキャナーを使用できる
3. 組織と連携できる内部コンポーネントを含めることができる

## 独自の Collector をビルドする際の考慮事項

さて、🥷 Ninja ゾーンと呼ばれるからには、いくつかの欠点もあります。

1. Go の経験は必須ではないが推奨される
1. Splunk のサポートは**ありません**
1. 配布とライフサイクル管理の責任が生じる

プロジェクトは安定化に向けて取り組んでいますが、変更によってワークフローが壊れないという保証はないことに注意してください。Splunk のチームは、より手厚いサポートと高い安定性を提供しており、デプロイのニーズに応じてキュレーションされたエクスペリエンスを提供できます。

## The Ninja Zone

開始するために必要なツールがすべてインストールされたら、`otelcol-builder.yaml` という名前の新しいファイルを作成し、以下のディレクトリ構造に従う必要があります。

``` bash
.
└── otelcol-builder.yaml
```

ファイルを作成したら、追加のメタデータとともにインストールするコンポーネントのリストを追加する必要があります。

この例では、introduction の設定で必要なコンポーネントのみをインストールするビルダーマニフェストを作成します。

```yaml
dist:
  name: otelcol-ninja
  description: A custom build of the Open Telemetry Collector
  output_path: ./dist

extensions:
- gomod: go.opentelemetry.io/collector/extension/ballastextension v0.80.0
- gomod: go.opentelemetry.io/collector/extension/zpagesextension  v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/httpforwarder v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/healthcheckextension v0.80.0

exporters:
- gomod: go.opentelemetry.io/collector/exporter/loggingexporter v0.80.0
- gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/splunkhecexporter v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/signalfxexporter v0.80.0

processors:
- gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.80.0
- gomod: go.opentelemetry.io/collector/processor/memorylimiterprocessor v0.80.0

receivers:
- gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/jaegerreceiver v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/prometheusreceiver v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/zipkinreceiver v0.80.0
```

_ocb_ 用の yaml ファイルを更新したら、以下のコマンドを実行します。

```shell
ocb --config=otelcol-builder.yaml
```

実行すると、以下のディレクトリ構造になります。

``` text
├── dist
│   ├── components.go
│   ├── components_test.go
│   ├── go.mod
│   ├── go.sum
│   ├── main.go
│   ├── main_others.go
│   ├── main_windows.go
│   └── otelcol-ninja
└── otelcol-builder.yaml
```

### References

1. [https://opentelemetry.io/docs/collector/custom-collector/](https://opentelemetry.io/docs/collector/custom-collector/)

{{% /expand %}}

---

## デフォルトの設定

OpenTelemetry は YAML ファイルを通じて設定されます。これらのファイルにはデフォルトの設定があり、ニーズに合わせて変更できます。提供されているデフォルトの設定を見てみましょう。

{{< tabs >}}
{{% tab title="Command" %}}

```bash
cat /etc/otelcol-contrib/config.yaml
```

{{% /tab %}}
{{% tab title="config.yaml" %}}

```yaml { lineNos="table" wrap="true"}
# To limit exposure to denial of service attacks, change the host in endpoints below from 0.0.0.0 to a specific network interface.
# See https://github.com/open-telemetry/opentelemetry-collector/blob/main/docs/security-best-practices.md#safeguards-against-denial-of-service-attacks

extensions:
  health_check:
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

おめでとうございます! OpenTelemetry Collector のダウンロードとインストールに成功しました。OTel Ninja への道のりは順調です。しかし、その前に、設定ファイルと OpenTelemetry Collector のさまざまなディストリビューションについて見ていきましょう。

{{% notice style="note" %}}

Splunk は、完全にサポートされた独自の OpenTelemetry Collector ディストリビューションを提供しています。このディストリビューションは、[**Splunk GitHub Repository**](https://github.com/signalfx/splunk-otel-collector) からインストールできるほか、Splunk Observability Cloud のウィザードを使ってシンプルなインストールスクリプトをコピー&ペーストする形でも利用できます。このディストリビューションには、OpenTelemetry Collector Contrib ディストリビューションでは利用できない多くの追加機能と拡張機能が含まれています。

- Splunk Distribution of the OpenTelemetry Collector は本番環境でテスト済みです。多くのお客様が本番環境で使用しています。
- 当社のディストリビューションを利用するお客様は、SLA の範囲内で公式の Splunk サポートから直接支援を受けられます。
- お客様は、メトリクスとトレース収集に関するコア設定エクスペリエンスにおける将来の破壊的変更を心配することなく、Splunk Distribution of the OpenTelemetry Collector を使用または移行できます (OpenTelemetry のログ収集設定はベータ版です)。Collector のメトリクスについては破壊的変更がある可能性があります。

{{% /notice %}}

これから設定ファイルの各セクションを順に見ていき、ホストメトリクスを Splunk Observability Cloud に送信するように変更します。
