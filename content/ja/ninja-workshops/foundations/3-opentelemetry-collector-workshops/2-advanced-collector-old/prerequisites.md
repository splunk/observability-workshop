---
title: 事前準備
weight: 2.1
archetype: chapter
time: 90 minutes
---

### 前提条件

- `vi`、`vim`、`nano`、またはお好みのテキストエディタを使った YAML ファイルの編集に習熟していること。
- サポートされる環境:
  - Splunk Workshop Instance（推奨）
  - Apple Mac (Apple Silicon)。`jq` のインストールが必要です - [**https://jqlang.org/download/**](https://jqlang.org/download/)

{{% notice title="演習" style="green" icon="running" %}}

**ワークショップ用ディレクトリの作成**: ご自身の環境で新しいディレクトリ（例: `advanced-otel-workshop`）を作成します。本ワークショップでは以降、このディレクトリを `[WORKSHOP]` と表記します。

**ワークショップ用バイナリのダウンロード**: `[WORKSHOP]` ディレクトリに移動し、OpenTelemetry Collector とロードジェネレーターのバイナリをダウンロードします。

{{% tabs %}}
{{% tab title="Splunk Workshop Instance" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v{{< otel-version >}}/otelcol_linux_amd64 -o otelcol && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64 -o loadgen
```

**ファイルパーミッションの更新**: ダウンロードが完了したら、両方のファイルに実行権限を付与するためにパーミッションを更新します。

```bash
chmod +x otelcol loadgen && \
./otelcol -v && \
./loadgen --help
```

{{% /tab %}}
{{% tab title="Apple Silicon" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v{{< otel-version >}}/otelcol_darwin_arm64 -o otelcol && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-darwin-arm64 -o loadgen
```

{{% notice style="warning" title="macOS ユーザーの方へ" icon="desktop" %}}
macOS でバイナリを実行する前に、ダウンロードしたファイルに macOS が付与する quarantine 属性を削除する必要があります。この手順により、制限なくバイナリを実行できるようになります。

ターミナルで次のコマンドを実行してください。

```bash { title="Remove Quarantine Attribute"}
xattr -dr com.apple.quarantine otelcol && \
xattr -dr com.apple.quarantine loadgen
```

**ファイルパーミッションの更新**: ダウンロードが完了したら、両方のファイルに実行権限を付与するためにパーミッションを更新します。

```bash
chmod +x otelcol loadgen && \
./otelcol -v && \
./loadgen --help
```

{{% /notice %}}

{{% /tab %}}
{{% /tabs %}}

```text { title="Initial Directory Structure" }
[WORKSHOP]
├── otelcol      # OpenTelemetry Collector binary
└── loadgen      # Load Generator binary
```

<!--
{{% notice note %}}
Having access to [**jq**](https://jqlang.org/download/) is recommended (installed by default on Splunk workshop instances). This lightweight command-line tool helps process and format JSON data, making it easier to inspect traces, metrics, and logs from the OpenTelemetry Collector.
{{% /notice %}}
-->
{{% /notice %}}
