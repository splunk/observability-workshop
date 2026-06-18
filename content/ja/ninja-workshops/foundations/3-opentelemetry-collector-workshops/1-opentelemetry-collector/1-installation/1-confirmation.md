---
title: OpenTelemetry Collector Contrib のインストール
linkTitle: 1.1 インストールの確認
weight: 1
---

## Collector が動作していることを確認する

Collector が動作しているはずです。`systemctl` コマンドを使用して root として確認します。ステータス表示を終了するには `q` を押してください。

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

設定ファイルの変更、環境変数の設定、Collector の再起動を複数回行うため、Collector サービスを停止し、起動時の自動起動を無効にする必要があります。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo systemctl stop otelcol-contrib && sudo systemctl disable otelcol-contrib
```

{{% /tab %}}
{{< /tabs >}}

---

{{% expand title="{{% badge style=primary icon=star %}}**Ninja:** Open Telemetry Collector Builder (ocb) を使って独自の Collector をビルドする{{% /badge %}}" %}}
このパートでは、システムに以下がインストールされている必要があります:

- Golang (最新バージョン)

  ``` bash
  cd /tmp
  wget https://golang.org/dl/go1.20.linux-amd64.tar.gz
  sudo tar -C /usr/local -xzf go1.20.linux-amd64.tar.gz
  ```

  `.profile` を編集し、以下の環境変数を追加します:

  ``` bash
  export GOROOT=/usr/local/go
  export GOPATH=$HOME/go
  export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
  ```

  シェルセッションを更新します:
  
  ``` bash
  source ~/.profile
  ```

  Go のバージョンを確認します:

  ``` bash
  go version
  ```  

- ocb のインストール
  - [プロジェクトのリリースページ](https://github.com/open-telemetry/opentelemetry-collector/releases/tag/cmd%2Fbuilder%2Fv0.80.0)から ocb バイナリをダウンロードし、以下のコマンドを実行します:

    ```bash
    mv ocb_0.80.0_darwin_arm64 /usr/bin/ocb
    chmod 755 /usr/bin/ocb
    ```

    別の方法として、golang ツールチェーンを使用してローカルでバイナリをビルドすることもできます:

    ```bash
    go install go.opentelemetry.io/collector/cmd/builder@v0.80.0
    mv $(go env GOPATH)/bin/builder /usr/bin/ocb
    ```

- (オプション) Docker

## なぜ独自の Collector をビルドするのか?

Collector のデフォルトディストリビューション (core および contrib) は、提供する機能が多すぎるか少なすぎるかのどちらかです。

また、インストールされているコンポーネントの数が多く、デプロイメントに必要のないものがほとんどであるため、本番環境で contrib Collector を実行することは推奨されません。

## 独自の Collector をビルドするメリットは?

独自の Collector バイナリ (一般的にディストリビューションと呼ばれます) を作成することは、必要なものだけをビルドすることを意味します。

そのメリットは以下の通りです:

1. バイナリサイズの縮小
2. 既存の Go スキャナーを使用した脆弱性チェックが可能
3. 組織と連携する内部コンポーネントを含めることが可能

## 独自の Collector をビルドする際の考慮事項は?

これは🥷 Ninja ゾーンですので、いくつかのデメリットもあります:

1. Go の経験が推奨 (必須ではないにしても)
1. Splunk サポート**なし**
1. ディストリビューションとライフサイクル管理の責任

プロジェクトは安定性に向けて取り組んでいますが、変更がワークフローを壊さないという保証はありません。Splunk のチームは、より高いサポートと安定性を提供し、デプロイメントのニーズに対応するキュレーションされた体験を提供しています。

## The Ninja Zone

必要なツールがすべてインストールされたら、`otelcol-builder.yaml` という名前の新しいファイルを作成します。以下のディレクトリ構造に従います:

``` bash
.
└── otelcol-builder.yaml
```

ファイルを作成したら、追加のメタデータとともにインストールするコンポーネントのリストを追加する必要があります。

この例では、イントロダクションの設定に必要なコンポーネントのみをインストールするビルダーマニフェストを作成します:

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

yaml ファイルが _ocb_ 用に更新されたら、以下のコマンドを実行します:

```shell
ocb --config=otelcol-builder.yaml
```

以下のディレクトリ構造が生成されます:

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

### 参考資料

1. [https://opentelemetry.io/docs/collector/custom-collector/](https://opentelemetry.io/docs/collector/custom-collector/)

{{% /expand %}}

## デフォルト設定

OpenTelemetry は YAML ファイルを通じて設定されます。これらのファイルにはデフォルト設定があり、ニーズに合わせて変更できます。提供されているデフォルト設定を確認しましょう:

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

おめでとうございます！OpenTelemetry Collector のダウンロードとインストールが正常に完了しました。OTel Ninja への道を順調に進んでいます。まずは設定ファイルと OpenTelemetry Collector のさまざまなディストリビューションについて説明します。

{{% notice style="note" %}}

Splunk は独自の完全サポート付き OpenTelemetry Collector ディストリビューションを提供しています。このディストリビューションは [**Splunk GitHub Repository**](https://github.com/signalfx/splunk-otel-collector) からインストールするか、Splunk Observability Cloud のウィザードを使用してコピー＆ペーストできる簡単なインストールスクリプトを生成することで利用できます。このディストリビューションには、OpenTelemetry Collector Contrib ディストリビューションでは利用できない多くの追加機能と拡張が含まれています。

- Splunk Distribution of the OpenTelemetry Collector は本番環境でテスト済みであり、大多数のお客様が本番環境で使用しています。
- このディストリビューションを使用するお客様は、SLA の範囲内で Splunk の公式サポートから直接支援を受けることができます。
- お客様は、メトリクスおよびトレース収集のコア設定体験に対する将来の破壊的変更を心配することなく、Splunk Distribution of the OpenTelemetry Collector を使用または移行できます (OpenTelemetry ログ収集の設定はベータ版です)。Collector のメトリクスには破壊的変更がある可能性があります。

{{% /notice %}}

次に、設定ファイルの各セクションを説明し、ホストメトリクスを Splunk Observability Cloud に送信するように変更します。
