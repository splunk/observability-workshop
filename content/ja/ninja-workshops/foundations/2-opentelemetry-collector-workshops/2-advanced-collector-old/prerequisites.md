---
title: 前提条件
weight: 2.1
archetype: chapter
time: 90 minutes
---

### 前提条件

- `vi`、`vim`、`nano`、またはお好みのテキストエディタを使用してYAMLファイルを編集できること。
- サポートされている環境:
  - Splunkワークショップインスタンス（推奨）
  - Apple Mac（Apple Silicon）。`jq`のインストールが必要です - [**https://jqlang.org/download/**](https://jqlang.org/download/)

{{% notice title="演習" style="green" icon="running" %}}

**ワークショップディレクトリの作成**: お使いの環境で新しいディレクトリ（例: `advanced-otel-workshop`）を作成します。以降、このディレクトリを `[WORKSHOP]` と呼びます。

**ワークショップバイナリのダウンロード**: `[WORKSHOP]` ディレクトリに移動し、OpenTelemetry CollectorとLoad Generatorのバイナリをダウンロードします。

{{% tabs %}}
{{% tab title="Splunkワークショップインスタンス" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v{{< otel-version >}}/otelcol_linux_amd64 -o otelcol && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64 -o loadgen
```

**ファイル権限の更新**: ダウンロード後、両方のファイルを実行可能にするため権限を更新します。

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

{{% notice style="warning" title="macOSユーザー" icon="desktop" %}}
macOSでバイナリを実行する前に、ダウンロードしたファイルにmacOSが付与する隔離属性を削除する必要があります。このステップにより、制限なく実行できるようになります。

ターミナルで以下のコマンドを実行します。

```bash { title="隔離属性の削除"}
xattr -dr com.apple.quarantine otelcol && \
xattr -dr com.apple.quarantine loadgen
```

**ファイル権限の更新**: ダウンロード後、両方のファイルを実行可能にするため権限を更新します。

```bash
chmod +x otelcol loadgen && \
./otelcol -v && \
./loadgen --help
```

{{% /notice %}}

{{% /tab %}}
{{% /tabs %}}

```text { title="初期ディレクトリ構成" }
[WORKSHOP]
├── otelcol      # OpenTelemetry Collector binary
└── loadgen      # Load Generator binary
```

<!--
{{% notice note %}}
[**jq**](https://jqlang.org/download/)へのアクセスを推奨します（Splunkワークショップインスタンスではデフォルトでインストール済み）。この軽量なコマンドラインツールはJSONデータの処理とフォーマットに役立ち、OpenTelemetry Collectorからのトレース、メトリクス、ログの検査が容易になります。
{{% /notice %}}
-->
{{% /notice %}}
