---
title: 2. OBI でインストルメントする
weight: 2
---

実行中のアプリに**コードを一行も変更せずに** APM トレーシングを追加します。

## OBI のダウンロード

[GitHub リリースページ](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases)からビルド済みの OBI バイナリをダウンロードします。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
VERSION=0.6.0
ARCH=amd64
wget "https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases/download/v$VERSION/obi-v$VERSION-linux-$ARCH.tar.gz"
wget "https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases/download/v$VERSION/SHA256SUMS"
sha256sum -c SHA256SUMS --ignore-missing
tar -xzf "obi-v$VERSION-linux-$ARCH.tar.gz"
ls -la ./obi
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
obi-v0.6.0-linux-amd64.tar.gz: OK
-rwxr-xr-x 1 splunk splunk 112345678 Feb 27 14:47 ./obi
```

{{% /tab %}}
{{< /tabs >}}

## OBI の実行

{{% notice title="Exercise" style="green" icon="running" %}}

**別のターミナル**で、`sudo` を使って OBI を実行します。3つのプレースホルダーを前のステップで確認した realm、token、hostname に置き換えてください（完了まで1〜2分かかる場合があります）。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
cd ~/workshop/obi/01-obi-python

sudo env \
  OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="https://ingest.${REALM}.signalfx.com:443" \
  OTEL_EXPORTER_OTLP_TRACES_PROTOCOL="grpc" \
  OTEL_EXPORTER_OTLP_HEADERS="X-SF-Token=${ACCESS_TOKEN}" \
  OTEL_SERVICE_NAME="warmup-app" \
  OTEL_RESOURCE_ATTRIBUTES="deployment.environment=ebpf-bare-app,host.name=${INSTANCE}" \
  OTEL_EBPF_OPEN_PORT=5150 \
  ./obi
```

{{% /tab %}}
{{% tab title="Look for this in your Output" %}}
トラフィックを生成し、以下の出力を確認してください

```text
...
time=2026-02-27T19:29:56.296Z level=INFO msg="instrumenting process" component=discover.traceAttacher cmd=/usr/bin/python3.10 pid=245031 ino=7094 type=python service=warmup-app logenricher=false
...
time=2026-02-27T19:29:58.278Z level=INFO msg="Launching p.Tracer" component=generic.Tracer
```

{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

### 各変数の説明

| 変数 | 目的 |
|---|---|
| `sudo` | eBPF プローブには root/カーネルアクセスが必要です |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Splunk の OTLP トレース取り込み用の完全な URL です。シグナルごとの環境変数はこの URL にそのまま送信します。ベースの `OTEL_EXPORTER_OTLP_ENDPOINT` は `/v1/traces` を付加しますが、Splunk のパスとは一致しません |
| `OTEL_EXPORTER_OTLP_HEADERS` | Splunk の認証ヘッダーです |
| `OTEL_SERVICE_NAME` | Splunk APM に表示されるサービス名です |
| `OTEL_RESOURCE_ATTRIBUTES` | すべてのトレースに `deployment.environment` と `host.name` を設定し、自分のデータでフィルタリングできるようにします |
| `OTEL_EBPF_OPEN_PORT` | ポート 5150 でリッスンしているプロセスをインストルメントするよう OBI に指示します |

{{% notice title="Note" style="info" %}}
OBI のログに `failed to upload metrics: 404 Not Found` のような警告が表示される場合があります。これは想定どおりです。Splunk の直接取り込みには標準的な OTLP メトリクスエンドポイントがありません。トレースは正常にエクスポートされます。Phase 2 では、Collector がトレースとメトリクスの両方を適切に処理します。
{{% /notice %}}

## トラフィックの生成

最初のターミナルに戻り、いくつかのリクエストを生成します。

```bash
for i in $(seq 1 20); do curl -s "http://localhost:5150/hello"; sleep 1; done
```

***注意:*** 404 エラーが発生した場合は、curl している URL の末尾に `\` が付加されていないか確認してください。一部のターミナルでは `;` がエスケープされ、無効な URL になることがあります
