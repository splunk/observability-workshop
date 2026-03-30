---
title: 2. OBI による計装
weight: 2
---

実行中のアプリにAPMトレースを追加します。**コードを一行も変更する必要はありません**。

## OBI バイナリの抽出

OBIにはまだスタンドアロンのダウンロードがないため、Dockerイメージからバイナリを抽出します：

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
IMAGE=otel/ebpf-instrument:main
sudo docker pull $IMAGE
ID=$(sudo docker create $IMAGE)
sudo docker cp "$ID:/obi" ./obi
sudo docker rm -v $ID
ls -la ./obi
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` text
main: Pulling from otel/ebpf-instrument
0f5fbf7fdc05: Pull complete
c9d0c8eb6b20: Pull complete
05db807c0ef0: Pull complete
9414859de0f9: Pull complete
04083a69ab27: Pull complete
Digest: sha256:f1b61af237c7ec02ea83afb7108ec8d65f3e308f9501818a15b67983f243cf97
Status: Downloaded newer image for otel/ebpf-instrument:main
docker.io/otel/ebpf-instrument:main
Successfully copied 108MB to /home/splunk/workshop/obi/01-obi-python/obi
baa799720f42deaeeeb7690a39b91a5ae16f71ec33833d8a963808f14109ea0f
-rwxr-xr-x 1 root root 107922836 Feb 27 14:47 ./obi
```

{{% /tab %}}
{{< /tabs >}}

## OBI の実行

{{% notice title="演習" style="green" icon="running" %}}

**別のターミナル**で、`sudo` を使用してOBIを実行します。3つのプレースホルダーを前のステップで取得したrealm、token、hostnameに置き換えてください：

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
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
トラフィックを生成し、以下の出力を確認してください

``` text
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
| `sudo` | eBPF プローブには root/カーネルアクセスが必要です |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Splunk の OTLP トレース取り込み用の完全な URL です。シグナル別の環境変数はこの URL に正確に送信します。ベースの `OTEL_EXPORTER_OTLP_ENDPOINT` は `/v1/traces` を追加しますが、これは Splunk のパスと一致しません |
| `OTEL_EXPORTER_OTLP_HEADERS` | Splunk 用の認証ヘッダーです |
| `OTEL_SERVICE_NAME` | Splunk APM に表示されるサービス名です |
| `OTEL_RESOURCE_ATTRIBUTES` | すべてのトレースに `deployment.environment` と `host.name` を設定し、データをフィルタリングできるようにします |
| `OTEL_EBPF_OPEN_PORT` | OBI にポート 5150 でリッスンしているプロセスを計装するよう指示します |

{{% notice title="注意" style="info" %}}
OBIのログで `failed to upload metrics: 404 Not Found` のような警告が表示されることがあります。これは想定内の動作です。Splunkの直接取り込みには標準的なOTLPメトリクスエンドポイントがありません。トレースは正しくエクスポートされます。フェーズ2では、コレクターがトレースとメトリクスの両方を適切に処理します。
{{% /notice %}}

## トラフィックの生成

最初のターミナルに戻り、いくつかのリクエストを生成します：

``` bash
for i in $(seq 1 20); do curl -s http://localhost:5150/hello; sleep 1; done
```
