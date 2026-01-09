---
title: 1.2 設定の検証とテスト
linkTitle: 1.2 Validate & Test Configuration
weight: 3
---

次に、**Gateway** と **Agent** を起動します。**Agent** は起動時に自動的に **Host Metrics** を送信するよう設定されています。これにより、データが **Agent** から **Gateway** に正しくルーティングされることを確認します。

{{% notice title="Exercise" style="green" icon="running" %}}

**Gateway**: **Gateway ターミナル** ウィンドウで、以下のコマンドを実行して **Gateway** を起動します：

```bash {title="Start the Gateway"}
../otelcol --config=gateway.yaml
```

すべてが正しく設定されている場合、Collector が起動し、出力に `Everything is ready. Begin running and processing data.` と表示されます。以下のような出力になります：

```text
2025-06-09T09:22:11.944+0100    info    service@v0.126.0/service.go:289 Everything is ready. Begin running and processing data. {"resource": {}}
```

**Gateway** が実行されると、ポート `5318` で受信データをリッスンし、受信したデータを以下のファイルにエクスポートします：

* `gateway-traces.out`
* `gateway-metrics.out`
* `gateway-logs.out`

**Agent の起動**: **Agent ターミナル** ウィンドウで、Agent 設定を使用して Agent を起動します：

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**CPU メトリクスの確認**:

1. **Agent** が起動すると、すぐに **CPU** メトリクスの送信を開始することを確認します。
2. **Agent** と **Gateway** の両方がデバッグ出力にこのアクティビティを表示します。出力は以下のスニペットのようになります：

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

この段階で、**Agent** は1時間ごとまたは再起動ごとに **CPU** メトリクスを収集し、Gateway に送信し続けます。**Gateway** はこれらのメトリクスを処理し、`gateway-metrics.out` という名前のファイルにエクスポートします。このファイルは、パイプラインサービスの一部としてエクスポートされたメトリクスを保存します。

**Gateway にデータが到着したことの確認**: CPU メトリクス（特に `cpu0`）が Gateway に正常に到達したことを確認するために、`jq` コマンドを使用して `gateway-metrics.out` ファイルを検査します。

以下のコマンドは、`system.cpu.time` メトリクスをフィルタリングして抽出し、`cpu0` に焦点を当てます。メトリクスの状態（例：`user`、`system`、`idle`、`interrupt`）と対応する値を表示します。

3つ目のターミナルウィンドウを開くか作成し、**Tests** と名前を付けます。**Tests ターミナル** で以下のコマンドを実行して `system.cpu.time` メトリクスを確認します：

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
> **Agent** と **Gateway** のプロセスを、それぞれのターミナルで `Ctrl-C` を押して停止してください。

{{% /notice %}}
