---
title: 1.2 設定の検証とテスト
linkTitle: 1.2 設定の検証とテスト
weight: 3
---

これで **Gateway** と **Agent** を起動できるようになりました。**Agent** は起動時に自動で **Host Metrics** を送信するように設定されています。これにより、**Agent** から **Gateway** へデータが正しくルーティングされていることを検証します。

{{% exercise title="Gateway と Agent の起動" %}}

**Gateway**: **Gateway terminal** ウィンドウで、次のコマンドを実行して **Gateway** を起動します。

```bash {title="Start the Gateway"}
../otelcol --config=gateway.yaml
```

すべてが正しく構成されている場合、コレクターが起動し、出力に `Everything is ready. Begin running and processing data.` と表示されます。次のような出力になります。

```text
2025-06-09T09:22:11.944+0100    info    service@v0.126.0/service.go:289 Everything is ready. Begin running and processing data. {"resource": {}}
```

**Gateway** が稼働すると、ポート `5318` で受信データを待ち受け、受信したデータを次のファイルにエクスポートします。

* `gateway-traces.out`
* `gateway-metrics.out`
* `gateway-logs.out`

**Agent の起動**: **Agent terminal** ウィンドウで、agent 構成を使って agent を起動します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**CPU メトリクスの確認**:

1. **Agent** が起動すると、ただちに **CPU** メトリクスの送信を開始することを確認します。
2. **Agent** と **Gateway** の両方が、デバッグ出力にこの動作を表示します。出力は次のスニペットのようになります。

```text
<snip>
NumberDataPoints #31
Data point attributes:
     -> cpu: Str(cpu3)
     -> state: Str(wait)
StartTimestamp: 2025-07-07 16:49:42 +0000 UTC
Timestamp: 2025-07-09 09:36:21.190226459 +0000 UTC
Value: 77.380000
        {"resource": {}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "metrics"}
```

この段階では、**Agent** は1時間に1回、または再起動のたびに **CPU** メトリクスを収集し続け、それを gateway へ送信します。**Gateway** はこれらのメトリクスを処理し、`gateway-metrics.out` という名前のファイルにエクスポートします。このファイルは、パイプラインサービスの一部としてエクスポートされたメトリクスを保存します。

**データが Gateway に到達したことの確認**: CPU メトリクス、特に `cpu0` のメトリクスが gateway に正しく届いていることを確認するために、`jq` コマンドで `gateway-metrics.out` ファイルを確認します。

次のコマンドは、`system.cpu.time` メトリクスをフィルタリングして抽出し、`cpu0` に焦点を当てます。メトリクスの state（例: `user`、`system`、`idle`、`interrupt`）と、対応する値が表示されます。

3つ目のターミナルウィンドウを開くか作成し、**Tests** という名前を付けてください。**Tests terminal** で次のコマンドを実行して、`system.cpu.time` メトリクスを確認します。

{{% tabs %}}
{{% tab title="Check CPU Metrics" %}}

```bash
jq '.resourceMetrics[].scopeMetrics[].metrics[] | select(.name == "system.cpu.time") | .sum.dataPoints[] | select(.attributes[0].value.stringValue == "cpu0") | {cpu: .attributes[0].value.stringValue, state: .attributes[1].value.stringValue, value: .asDouble}' gateway-metrics.out
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
  "cpu": "cpu0",
  "state": "user",
  "value": 123407.02
}
{
  "cpu": "cpu0",
  "state": "system",
  "value": 64866.6
}
{
  "cpu": "cpu0",
  "state": "idle",
  "value": 216427.87
}
{
  "cpu": "cpu0",
  "state": "interrupt",
  "value": 0
}
```

{{% /tab %}}
{{% /tabs %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止してください。

{{% /exercise %}}
