---
title: 前提条件
weight: 2.1
archetype: chapter
time: 5 minutes
---

## 前提条件

- `vi`、`vim`、`nano`、またはお好みのテキストエディターを使用してYAMLファイルを編集できること。
- サポートされている環境:
  - 提供されるSplunk Workshop Instance（推奨）。`ssh` アクセスのため、ポート `2222` への送信アクセスが必要です。
  - Apple Mac (Apple Silicon)。`jq` のインストールが必要です - [**https://jqlang.org/download/**](https://jqlang.org/download/)

{{% exercise title="ワークショップ用ディレクトリの作成" %}}

{{< step "初期セットアップ" "1" >}}

ご利用の環境で新しいディレクトリを作成し、そのディレクトリに移動します:

``` bash
mkdir advanced-otel-workshop && \
cd advanced-otel-workshop
```

このディレクトリは、ワークショップの残りの部分で `[WORKSHOP]` として参照します。

{{% notice title="既存のOpenTelemetry Collectorを削除する" style="warning" %}}
Splunk IMワークショップを完了している場合、続行する前にKubernetes上で動作しているcollectorが削除されていることを確認してください。これは以下のコマンドを実行することで実施できます:

``` bash
helm delete splunk-otel-collector
```

その場合のEC2インスタンスでは、本ワークショップに干渉する可能性のあるサービスが動作している場合があるため、以下のコマンドを実行して、それらが存在する場合は確実に停止させてください:

``` bash
kubectl delete ~/workshop/apm/deployment.yaml
```

{{% /notice %}}
{{< /step >}}

{{< step "ワークショップのバイナリをダウンロード" "2" >}}

`[WORKSHOP]` ディレクトリに移動し、OpenTelemetry Collector、Load Generatorのバイナリ、およびセットアップスクリプトをダウンロードします:

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

{{< step "セットアップを実行する" "3" >}}
`setup-workshop.sh` スクリプトを実行します。このスクリプトは正しい権限を設定するとともに、**Agent** および **Gateway** の初期設定を作成します:

{{% tabs %}}
{{% tab title="Setup Workshop" %}}

```bash
./setup-workshop.sh
```

{{% /tab %}}
{{% tab title="Verify Setup" %}}

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

```text { title="Initial Directory Structure" }
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

{{< checkpoint "ワークショップ環境の準備が完了しました — **第1章: Agent Configuration** へ進みましょう。" >}}
