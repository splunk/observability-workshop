---
title: 前提条件
weight: 2.1
archetype: chapter
time: 5 minutes
---

### 前提条件

- `vi`、`vim`、`nano`、またはお好みのテキストエディタを使用して YAML ファイルを編集するスキル
- サポートされている環境：
  - 提供される Splunk Workshop インスタンス（推奨）。`ssh` アクセス用にポート `2222` への外部アクセスが必要です。
  - Apple Mac（Apple Silicon）。`jq` のインストールが必要です - [**https://jqlang.org/download/**](https://jqlang.org/download/)

{{% notice title="Exercise" style="green" icon="running" %}}

**ディレクトリの作成**: 環境内で新しいディレクトリを作成し、そのディレクトリに移動します：

``` bash
mkdir advanced-otel-workshop && \
cd advanced-otel-workshop
```

このワークショップの残りの部分では、このディレクトリを `[WORKSHOP]` と呼びます。

{{% notice title="既存の OpenTelemetry Collector を削除してください" style="warning" %}}
Splunk IM ワークショップを完了している場合は、続行する前に Kubernetes で実行中の Collector を削除してください。以下のコマンドを実行して削除できます：

``` bash
helm delete splunk-otel-collector
```

その場合、EC2 インスタンスでこのワークショップと干渉する可能性のあるサービスが実行されている場合があるため、以下のコマンドを実行してそれらが存在する場合は停止してください：

``` bash
kubectl delete ~/workshop/apm/deployment.yaml
```

{{% /notice %}}

**ワークショップバイナリのダウンロード**: `[WORKSHOP]` ディレクトリに移動し、OpenTelemetry Collector、Load Generator バイナリ、およびセットアップスクリプトをダウンロードします：

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

<!--
{{% notice style="warning" title="macOS Users" icon="desktop" %}}
macOS でバイナリを実行する前に、macOS がダウンロードしたファイルに適用する隔離属性を削除する必要があります。この手順により、制限なく実行できるようになります。

ターミナルで以下のコマンドを実行してください：

```bash { title="Remove Quarantine Attribute"}
xattr -dr com.apple.quarantine otelcol && \
xattr -dr com.apple.quarantine loadgen
```

{{% /notice %}}
-->
{{% /tab %}}
{{% /tabs %}}

<!--
**ファイル権限の更新**: ダウンロード後、ファイル権限を更新してすべてのファイルを実行可能にします：

```bash
chmod +x otelcol loadgen setup-workshop.sh && \
./otelcol -v && \
./loadgen --help && \
./setup-workshop.sh
```
-->

`setup-workshop.sh` スクリプトを実行します。このスクリプトは正しい権限を設定し、**Agent** と **Gateway** の初期設定も作成します：

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

<!--
{{% notice note %}}
[**jq**](https://jqlang.org/download/) へのアクセスが推奨されます（Splunk ワークショップインスタンスにはデフォルトでインストールされています）。この軽量なコマンドラインツールは、JSON データの処理とフォーマットを支援し、OpenTelemetry Collector からのトレース、メトリクス、ログの検査を容易にします。
{{% /notice %}}
-->
{{% /notice %}}
