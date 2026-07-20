---
title: 前提条件
weight: 2.1
archetype: chapter
time: 5 minutes
---

## 前提条件

- `vi`、`vim`、`nano`、またはお好みのテキストエディタを使用してYAMLファイルを編集できること。
- サポートされている環境
  - 提供されたSplunk Workshop Instance（推奨）。`ssh`アクセスのためにポート `2222` への送信アクセスが必要です。
  - Apple Mac（Apple Silicon）。`jq`のインストールが必要です - [**https://jqlang.org/download/**](https://jqlang.org/download/)

{{% exercise title="ワークショップディレクトリの作成" %}}

{{< step "初期セットアップ" "1" >}}

環境に新しいディレクトリを作成し、そのディレクトリに移動します。

``` bash
mkdir advanced-otel-workshop && \
cd advanced-otel-workshop
```

以降、このディレクトリを `[WORKSHOP]` と呼びます。

{{% notice title="既存のOpenTelemetry Collectorの削除" style="warning" %}}
Splunk IMワークショップを完了している場合は、続行する前にKubernetesで実行中のCollectorを削除してください。以下のコマンドを実行して削除できます。

``` bash
helm delete splunk-otel-collector
```

その場合、EC2インスタンスでこのワークショップに干渉する可能性のあるサービスが実行されていることがあります。以下のコマンドを実行して、存在する場合はそれらを停止してください。

``` bash
kubectl delete ~/workshop/apm/deployment.yaml
```

{{% /notice %}}
{{< /step >}}

{{< step "ワークショップバイナリのダウンロード" "2" >}}

`[WORKSHOP]` ディレクトリに移動し、OpenTelemetry Collector、Load Generatorバイナリ、およびセットアップスクリプトをダウンロードします。

{{% tabs %}}
{{% tab title="Splunk Workshop Instance" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v{{< otel-version >}}/otelcol_linux_amd64 -o otelcol && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64 -o loadgen && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/setup-workshop.sh -o setup-workshop.sh && \
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% tab title="Apple Silicon" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v{{< otel-version >}}/otelcol_darwin_arm64 -o otelcol && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-darwin-arm64 -o loadgen && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/setup-workshop.sh -o setup-workshop.sh && \
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% /tabs %}}

{{< /step >}}

{{< step "セットアップの実行" "3" >}}
`setup-workshop.sh` スクリプトを実行します。このスクリプトは適切な権限を設定し、 **Agent** と **Gateway** の初期設定を作成します。

{{% tabs %}}
{{% tab title="ワークショップのセットアップ" %}}

```bash
./setup-workshop.sh
```

{{% /tab %}}
{{% tab title="セットアップの確認" %}}

```text
███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝

Welcome to the Splunk Advanced OpenTelemetry Workshop!
======================================================

macOS detected. Removing quarantine attributes...
otelcol version v0.126.0
Usage: loadgen [OPTIONS]
Options:
  -base       Send base traces (enabled by default)
  -health     Send health traces
  -security   Send security traces
  -logs       Enable logging of random quotes to quotes.log
  -json       Output logs in JSON format (only applicable with -logs)
  -count      Number of traces or logs to send (default: infinite)
  -h, --help  Display this help message

Example:
  loadgen -health -security -count 10   Send 10 health and security traces
  loadgen -logs -json -count 5          Write 5 random quotes in JSON format to quotes.log
Creating workshop directories...
✓ Created subdirectories:
  ├── 1-agent-gateway
  ├── 2-building-resilience
  ├── 3-dropping-spans
  ├── 4-sensitive-data
  ├── 5-transform-data
  ├── 6-routing-data
  └── 7-sum-count

Creating configuration files for 1-agent-gateway...
Creating OpenTelemetry Collector agent configuration file: 1-agent-gateway/agent.yaml
✓ Configuration file created successfully: 1-agent-gateway/agent.yaml
✓ File size:     4355 bytes

Creating OpenTelemetry Collector gateway configuration file: 1-agent-gateway/gateway.yaml
✓ Configuration file created successfully: 1-agent-gateway/gateway.yaml
✓ File size:     3376 bytes

✓ Completed configuration files for 1-agent-gateway

Creating configuration files for 2-building-resilience...
Creating OpenTelemetry Collector agent configuration file: 2-building-resilience/agent.yaml
✓ Configuration file created successfully: 2-building-resilience/agent.yaml
✓ File size:     4355 bytes

Creating OpenTelemetry Collector gateway configuration file: 2-building-resilience/gateway.yaml
✓ Configuration file created successfully: 2-building-resilience/gateway.yaml
✓ File size:     3376 bytes

✓ Completed configuration files for 2-building-resilience

Workshop environment setup complete!
Configuration files created in the following directories:
  1-agent-gateway/
    ├── agent.yaml
    └── gateway.yaml
  2-building-resilience/
    ├── agent.yaml
    └── gateway.yaml
```

{{% /tab %}}
{{% /tabs %}}

```text { title="初期ディレクトリ構造" }
[WORKSHOP]
├── 1-agent-gateway
├── 2-building-resilience
├── 3-dropping-spans
├── 4-sensitive-data
├── 5-transform-data
├── 6-routing-data
├── 7-sum-count
├── loadgen
├── otelcol
└── setup-workshop.sh
```

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "ワークショップ環境の準備が完了しました。 **Chapter 1: Agent Configuration** に進みましょう。" >}}
