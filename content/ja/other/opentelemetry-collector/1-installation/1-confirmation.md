---
title: OpenTelemetry Collector Contribをインストールする
linkTitle: 1.1 インストールを確認する
weight: 1
---

## Collector が動作していることを確認する

これで、Collector が動いているはずです。root権限で `systemctl` コマンドを使って、それを確かめてみましょう。ステータス表示を中止するには `q` を押してください。

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
     Active: active (running) since Tue 2023-05-16 08:23:23 UTC; 25s ago
   Main PID: 1415 (otelcol-contrib)
      Tasks: 5 (limit: 1141)
     Memory: 22.2M
        CPU: 125ms
     CGroup: /system.slice/otelcol-contrib.service
             └─1415 /usr/bin/otelcol-contrib --config=/etc/otelcol-contrib/config.yaml

May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: NumberDataPoints #0
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: Data point attributes:
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:      -> exporter: Str(logging)
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:      -> service_instance_id: Str(df8a57f4-abdc-46b9-a847-acd62db1001f)
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:      -> service_name: Str(otelcol-contrib)
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:      -> service_version: Str(0.75.0)
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: StartTimestamp: 2023-05-16 08:23:39.006 +0000 UTC
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: Timestamp: 2023-05-16 08:23:39.006 +0000 UTC
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: Value: 0.000000
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:         {"kind": "exporter", "data_type": "metrics", "name": "logging"}
```

{{% /tab %}}
{{< /tabs >}}

このワークショップでは、ここで設定した `otelcol-contrib` のスタンドアローンで動作するバイナリーを使っていきます。サービスを停止して、自動起動を無効化するために、次のコマンドを使ってください:

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo systemctl stop otelcol-contrib
```

{{% /tab %}}
{{< /tabs >}}

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo systemctl disable otelcol-contrib
```

{{% /tab %}}
{{< /tabs >}}

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Open Telemetry Collector Builder (ocb) を使って、独自のコレクターを作る {{% /badge %}}" %}}

このパートでは、お使いのシステムに以下のものがインストールされている必要があります：

- Go (latest version)

  ``` bash
  cd /tmp
  wget https://golang.org/dl/go1.20.linux-amd64.tar.gz
  sudo tar -C /usr/local -xzf go1.20.linux-amd64.tar.gz
  ```

  `.profile` を編集して、次の環境変数をセットします:
  
  ``` bash
  export GOROOT=/usr/local/go
  export GOPATH=$HOME/go
  export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
  ```

  そして、シェルのセッションを更新します:
  
  ``` bash
  source ~/.profile
  ```

  Go のバージョンを確認します:
  
  ``` bash
  go version
  ```  

- ocb のインストール
  - ocb バイナリーを [project releases](https://github.com/open-telemetry/opentelemetry-collector/releases/tag/cmd%2Fbuilder%2Fv0.80.0)
    からダウンロードして、次のコマンドを実行します:
    
    ```bash
    mv ocb_0.80.0_darwin_arm64 /usr/bin/ocb
    chmod 755 /usr/bin/ocb
    ```

    別のアプローチとして、Go のツールチェーンを使ってバイナリをローカルにビルドする方法もあります:

    ```bash
    go install go.opentelemetry.io/collector/cmd/builder@v0.80.0
    mv $(go env GOPATH)/bin/builder /usr/bin/ocb
    ```

- (Optional) Docker

## なぜ独自のコレクターをビルドするの？

コレクターのデフォルトのディストリビューション（core および contrib）は、含まれれるコンポーネントが少なすぎたり、もしくは多すぎたりします。

本番環境で contrib コレクターを実行することはできますが、インストールされているコンポーネントの量が多く、デプロイに必要ではないものも含まれるため、一般的には推奨されません。

## 独自のコレクターをビルドする利点は？

独自のコレクターバイナリー（通常は「ディストリビューション」と呼ばれる）を作成することで、必要なものだけをビルドすることができます。

メリットは次のとおりです:

1. バイナリーのサイズが小さい
2. 一般的な Go の脆弱性スキャナーを利用できる
3. 組織独自のコンポーネントを組み込むことができる

## カスタムコレクターをビルドするときの注意事項は？

さて、これは Ninja ゾーンの人たちにあえて言うことではないかもしれませんが:

1. Go の開発経験を、必須ではないが、推奨される
1. Splunk の **サポートがない**
1. ディストリビューションのライフサイクルを管理しなければならない

プロジェクトは安定性に向けて進んでいますが、行われた変更がワークフローを壊す可能性があることに注意してください。Splunk チームは、より高い安定性とサポートを提供し、デプロイメントニーズに対応するためのキュレーションされた経験を提供しています。

## Ninja ゾーン

必要なツールをすべてインストールしたら、以下のディレクトリ構造に従い、 `otelcol-builder.yaml` という新しいファイルを作成します:


``` bash
.
└── otelcol-builder.yaml
```

ファイルを作成したら、インストールするコンポーネントのリストと追加のメタデータを追加する必要があります。

この例では、導入設定に必要なコンポーネントのみをインストールするためのビルダーマニフェストを作成します:

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
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/sapmexporter v0.80.0

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

_ocb_ のためのyamlファイルを作成して更新したら、 次のコマンドを実行します:

```shell
ocb --config=otelcol-builder.yaml
```

すると、次のようなディレクトリ構造が作成されます:

``` text
├── dist
│   ├── components.go
│   ├── components_test.go
│   ├── go.mod
│   ├── go.sum
│   ├── main.go
│   ├── main_others.go
│   ├── main_windows.go
│   └── otelcol-ninja
└── otelcol-builder.yaml
```

### リファレンス

1. [https://opentelemetry.io/docs/collector/custom-collector/](https://opentelemetry.io/docs/collector/custom-collector/)

{{% /expand %}}

---

## デフォルト設定

OpenTelemetry Collector は YAML ファイルを使って設定をしていきます。これらのファイルには、必要に応じて変更できるデフォルト設定が含まれています。提供されているデフォルト設定を見てみましょう:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
cat /etc/otelcol-contrib/config.yaml
```

{{% /tab %}}
{{% tab title="config.yaml" %}}

```yaml { lineNos="table" wrap="true"}
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

おめでとうございます！OpenTelemetry Collector のダウンロードとインストールに成功しました。あなたは OTel Ninja になる準備ができました。しかしまずは、設定ファイルと OpenTelemetry Collector の異なるディストリビューションについて見ていきましょう。

{{% notice style="note" %}}

Splunk は、自社で完全にサポートされた OpenTelemetry Collector のディストリビューションを提供しています。このディストリビューションは、[Splunk GitHub Repository](https://github.com/signalfx/splunk-otel-collector) からインストールするか、Splunk Observability Cloud のウィザードを使用して、簡単なインストールスクリプトを作成し、コピー＆ペーストすることで利用できます。このディストリビューションには、OpenTelemetry Collector Contrib ディストリビューションにはない追加機能や強化が含まれています。

- Splunk の OpenTelemetry Collector ディストリビューションは本番環境でテスト済みであり、多くの顧客が本番環境で使用しています。
- このディストリビューションを使用する顧客は、公式の Splunk サポートから、SLA の範囲内で直接支援を受けることができます。
- メトリクスとトレース収集のコア構成体験に将来的な破壊的変更がないことを心配せずに、Splunk の OpenTelemetry Collector ディストリビューションを使用または移行することができます（OpenTelemetry ログ収集の設定はベータ版です）。Collector 自身のメトリクスに破壊的変更がある可能性はあります。

{{% /notice %}}

このセクションでは、ホストメトリクスを Splunk Observability Cloud に送信するために、設定ファイルの各セクションを詳しく見ていき、変更する方法について説明します。
