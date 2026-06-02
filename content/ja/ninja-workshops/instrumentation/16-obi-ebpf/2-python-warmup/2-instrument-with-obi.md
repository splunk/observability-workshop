---
title: 2. OBI でインストルメントする
weight: 2
---

実行中のこのアプリケーションに対して、**コードを 1 行も変更することなく** APM トレーシングを追加します。

## OBI のダウンロード

[GitHub releases page](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases) からビルド済みの OBI バイナリをダウンロードします。

{{< tabs >}}
{{% tab title="Script" %}}

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
{{% tab title="Example Output" %}}

```text
obi-v0.6.0-linux-amd64.tar.gz: OK
-rwxr-xr-x 1 splunk splunk 112345678 Feb 27 14:47 ./obi
```

{{% /tab %}}
{{< /tabs >}}

## OBI の実行

{{% notice title="演習" style="green" icon="running" %}}

**別のターミナル** で、`sudo` を使って OBI を実行します。3 つのプレースホルダーを、前のステップで取得した realm、token、hostname に置き換えてください（完了までに 1 〜 2 分かかる場合があります）。

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
トラフィックを生成し、次のような出力が表示されることを確認します。

```text
...
time=2026-02-27T19:29:56.296Z level=INFO msg="instrumenting process" component=discover.traceAttacher cmd=/usr/bin/python3.10 pid=245031 ino=7094 type=python service=warmup-app logenricher=false
...
time=2026-02-27T19:29:58.278Z level=INFO msg="Launching p.Tracer" component=generic.Tracer
```

{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

### これらの変数の役割

| 変数 | 目的 |
|---|---|
| `sudo` | eBPF プローブには root / カーネルアクセスが必要です |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Splunk の OTLP トレース取り込み用の完全な URL です。シグナルごとの環境変数を使うとこの URL にそのまま送信されますが、ベース変数 `OTEL_EXPORTER_OTLP_ENDPOINT` を使うと末尾に `/v1/traces` が付加され、Splunk のパスと一致しなくなります |
| `OTEL_EXPORTER_OTLP_HEADERS` | Splunk 用の認証ヘッダーです |
| `OTEL_SERVICE_NAME` | Splunk APM に表示されるサービス名です |
| `OTEL_RESOURCE_ATTRIBUTES` | すべてのトレースに `deployment.environment` と `host.name` を設定し、自分のデータに絞り込めるようにします |
| `OTEL_EBPF_OPEN_PORT` | ポート 5150 でリッスンしているプロセスをインストルメントするように OBI に指示します |

{{% notice title="Note" style="info" %}}
OBI のログに `failed to upload metrics: 404 Not Found` のような警告が表示されることがあります。これは想定された動作です。Splunk の direct ingest には標準の OTLP メトリクスエンドポイントが存在しないためです。トレースは引き続き正しくエクスポートされます。Phase 2 では、collector がトレースとメトリクスの両方を適切に処理します。
{{% /notice %}}

## トラフィックの生成

最初のターミナルに戻り、いくつかリクエストを生成します。

```bash
for i in $(seq 1 20); do curl -s "http://localhost:5150/hello"; sleep 1; done
```

***NOTE:*** 404 エラーが発生した場合、curl で指定している URL の末尾に `\` が付いていないか再確認してください。一部のターミナルでは `;` がエスケープされ、不正な URL になることがあります。
