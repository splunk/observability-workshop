---
title: OpenTelemetry Collector Contribのインストール
linkTitle: 1.1 インストールの確認
weight: 1
---

## Collectorが動作していることを確認する

Collectorが動作しているはずです。rootとして `systemctl` コマンドを使用して確認します。ステータス表示を終了するには `q` を押します。

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

この後、設定ファイルの変更、環境変数の設定、Collectorの再起動を複数回行うため、Collectorサービスを停止し、起動時の自動起動を無効にする必要があります。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo systemctl stop otelcol-contrib && sudo systemctl disable otelcol-contrib
```

{{% /tab %}}
{{< /tabs >}}

---

{{% expand title="{{% badge style=primary icon=star %}}**Ninja:** Open Telemetry Collector Builder (ocb) を使って独自のCollectorをビルドする{{% /badge %}}" %}}
このパートでは、システムに以下がインストールされている必要があります。

- Golang（最新バージョン）

  ``` bash
  cd /tmp
  wget https://golang.org/dl/go1.20.linux-amd64.tar.gz
  sudo tar -C /usr/local -xzf go1.20.linux-amd64.tar.gz
  ```

  `.profile` を編集して、以下の環境変数を追加します。

  ``` bash
  export GOROOT=/usr/local/go
  export GOPATH=$HOME/go
  export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
  ```

  シェルセッションを更新します。
  
  ``` bash
  source ~/.profile
  ```

  Goのバージョンを確認します。

  ``` bash
  go version
  ```  

- ocbのインストール
  - [プロジェクトのリリースページ](https://github.com/open-telemetry/opentelemetry-collector/releases/tag/cmd%2Fbuilder%2Fv0.80.0)からocbバイナリをダウンロードし、以下のコマンドを実行します。

    ```bash
    mv ocb_0.80.0_darwin_arm64 /usr/bin/ocb
    chmod 755 /usr/bin/ocb
    ```

    別の方法として、golangツールチェーンを使用してローカルでバイナリをビルドすることもできます。

    ```bash
    go install go.opentelemetry.io/collector/cmd/builder@v0.80.0
    mv $(go env GOPATH)/bin/builder /usr/bin/ocb
    ```

- （オプション）Docker

## なぜ独自のCollectorをビルドするのか？

Collectorのデフォルトディストリビューション（coreおよびcontrib）は、提供する機能が多すぎるか少なすぎるかのどちらかです。

また、contribのCollectorを本番環境で実行することは推奨されません。インストールされるコンポーネントの量が多く、デプロイメントに必要のないものがほとんどだからです。

## 独自のCollectorをビルドするメリット

独自のCollectorバイナリ（一般的にディストリビューションと呼ばれます）を作成する場合、必要なものだけをビルドできます。

そのメリットは以下の通りです。

1. バイナリサイズが小さくなる
2. 既存のGoスキャナーを使用して脆弱性を検出できる
3. 組織に固有の内部コンポーネントを含めることができる

## 独自のCollectorをビルドする際の考慮事項

これは🥷 Ninjaゾーンなので、いくつかの注意点があります。

1. Goの経験が推奨（必須ではないが）
1. Splunkサポート **なし**
1. ディストリビューションとライフサイクル管理の責任

プロジェクトは安定性に向けて取り組んでいますが、変更によってワークフローが壊れないという保証はありません。Splunkのチームは、より高いサポートレベルと安定性を提供し、デプロイメントのニーズに対応するキュレートされた体験を提供しています。

## The Ninja Zone

必要なツールをすべてインストールしたら、`otelcol-builder.yaml` という名前の新しいファイルを作成します。以下のディレクトリ構造に従います。

``` bash
.
└── otelcol-builder.yaml
```

ファイルを作成したら、追加のメタデータとともにインストールするコンポーネントのリストを追加する必要があります。

この例では、イントロダクション設定に必要なコンポーネントのみをインストールするビルダーマニフェストを作成します。

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

yamlファイルを _ocb_ 用に更新したら、以下のコマンドを実行します。

```shell
ocb --config=otelcol-builder.yaml
```

以下のディレクトリ構造が生成されます。

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

OpenTelemetryはYAMLファイルで設定します。これらのファイルにはデフォルト設定があり、必要に応じて変更できます。提供されるデフォルト設定を確認しましょう。

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

おめでとうございます！OpenTelemetry Collectorのダウンロードとインストールが完了しました。OTel Ninjaへの道を順調に進んでいます。まずは設定ファイルとOpenTelemetry Collectorのさまざまなディストリビューションについて見ていきましょう。

{{% notice style="note" %}}

Splunkは独自のフルサポート付きOpenTelemetry Collectorディストリビューションを提供しています。このディストリビューションは [**Splunk GitHubリポジトリ**](https://github.com/signalfx/splunk-otel-collector) からインストールするか、Splunk Observability Cloudのウィザードを使用してコピー＆ペースト用の簡単なインストールスクリプトを生成できます。このディストリビューションには、OpenTelemetry Collector Contribディストリビューションでは利用できない多くの追加機能と拡張が含まれています。

- Splunk Distribution of the OpenTelemetry Collectorは本番環境でテスト済みであり、大多数のお客様が本番環境で使用しています。
- このディストリビューションを使用するお客様は、SLA内でSplunkの公式サポートから直接支援を受けることができます。
- お客様は、メトリクスとトレースの収集に関するコア設定体験への将来の破壊的変更を心配することなく、Splunk Distribution of the OpenTelemetry Collectorを使用または移行できます（OpenTelemetryのログ収集設定はベータ版です）。Collectorのメトリクスに破壊的変更がある可能性があります。

{{% /notice %}}

次に、設定ファイルの各セクションを順に見ていき、ホストメトリクスをSplunk Observability Cloudに送信するように変更します。
