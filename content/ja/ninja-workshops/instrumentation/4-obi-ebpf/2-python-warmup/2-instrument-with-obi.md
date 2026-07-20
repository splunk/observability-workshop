---
title: 2. OBIで計装する
weight: 2
---

実行中のアプリに **コードを一行も変更せずに** APMトレーシングを追加します。

## OBIのダウンロード

[GitHubリリースページ](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases)からビルド済みのOBIバイナリをダウンロードします。

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
VERSION=0.8.0
ARCH=amd64
wget "https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases/download/v$VERSION/obi-v$VERSION-linux-$ARCH.tar.gz"
wget "https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases/download/v$VERSION/SHA256SUMS"
sha256sum -c SHA256SUMS --ignore-missing
tar -xzf "obi-v$VERSION-linux-$ARCH.tar.gz"
ls -la ./obi
```

{{% /tab %}}
{{% tab title="出力例" %}}

```text
obi-v0.6.0-linux-amd64.tar.gz: OK
-rwxr-xr-x 1 splunk splunk 112345678 Feb 27 14:47 ./obi
```

{{% /tab %}}
{{< /tabs >}}

## OBIの実行

{{% notice title="Exercise" style="green" icon="running" %}}

**別のターミナル** で、`sudo` を使ってOBIを実行します。3つのプレースホルダーを前のステップで確認したrealm、token、hostnameに置き換えてください（完了までに1〜2分かかる場合があります）。

{{< tabs >}}
{{% tab title="スクリプト" %}}

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
{{% tab title="出力で確認する内容" %}}
トラフィックを生成し、以下の出力を確認します

```text
...
time=2026-02-27T19:29:56.296Z level=INFO msg="instrumenting process" component=discover.traceAttacher cmd=/usr/bin/python3.10 pid=245031 ino=7094 type=python service=warmup-app logenricher=false
...
time=2026-02-27T19:29:58.278Z level=INFO msg="Launching p.Tracer" component=generic.Tracer
```

{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

### 各変数の役割

| 変数 | 目的 |
|---|---|
| `sudo` | eBPFプローブにはroot/カーネルアクセスが必要 |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | SplunkのOTLPトレースインジェストの完全なURL。シグナルごとの環境変数はこのURLにそのまま送信します。ベースの `OTEL_EXPORTER_OTLP_ENDPOINT` は `/v1/traces` を追加しますが、Splunkのパスと一致しません |
| `OTEL_EXPORTER_OTLP_HEADERS` | Splunkの認証ヘッダー |
| `OTEL_SERVICE_NAME` | Splunk APMに表示されるサービス名 |
| `OTEL_RESOURCE_ATTRIBUTES` | すべてのトレースに `deployment.environment` と `host.name` を設定し、自分のデータでフィルタリングできるようにします |
| `OTEL_EBPF_OPEN_PORT` | ポート5150でリッスンしているプロセスを計装するようOBIに指示します |

{{% notice title="注意" style="info" %}}
OBIのログに `failed to upload metrics: 404 Not Found` のような警告が表示されることがあります。これは想定どおりです。Splunkのダイレクトインジェストには標準的なOTLPメトリクスエンドポイントがありません。トレースは正しくエクスポートされます。フェーズ2では、Collectorがトレースとメトリクスの両方を適切に処理します。
{{% /notice %}}

## トラフィックの生成

最初のターミナルに戻り、リクエストを生成します。

```bash
for i in $(seq 1 20); do curl -s "http://localhost:5150/hello"; sleep 1; done
```

***注意:*** 404エラーが返される場合は、curlで指定しているURLの末尾に `\` が付いていないか確認してください。一部のターミナルでは `;` がエスケープされ、無効なURLになることがあります。
