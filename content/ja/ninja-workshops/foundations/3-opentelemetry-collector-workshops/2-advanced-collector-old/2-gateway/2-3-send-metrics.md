---
title: 2.3 Agent から Gateway へメトリクスを送信する
linkTitle: 2.3 Send Metrics
weight: 3
---

{{% notice title="演習" style="green" icon="running" %}}

**Agent を起動する**: **Agent ターミナル** ウィンドウで、更新された設定を使って agent を起動します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**CPU メトリクスを確認する**:

1. `agent` が起動したら、ただちに **CPU** メトリクスの送信を開始することを確認します。
2. `agent` と `gateway` の両方が、デバッグ出力にこの動作を表示します。出力は次のスニペットのようになるはずです。

```text
<snip>
NumberDataPoints #37
Data point attributes:
    -> cpu: Str(cpu0)
    -> state: Str(system)
StartTimestamp: 2024-12-09 14:18:28 +0000 UTC
Timestamp: 2025-01-15 15:27:51.319526 +0000 UTC
Value: 9637.660000
```

この段階で、`agent` は 1 時間ごと、または再起動のたびに **CPU** メトリクスを収集し続け、それらを gateway に送信します。

`gateway` はこれらのメトリクスを処理し、`./gateway-metrics.out` という名前のファイルにエクスポートします。このファイルは、パイプラインサービスの一部としてエクスポートされたメトリクスを保存します。

**データが Gateway に到達したことを確認する**: CPU メトリクス、特に `cpu0` のメトリクスが gateway に正常に到達したことを確認するため、`jq` コマンドを使って `gateway-metrics.out` ファイルを調査します。

次のコマンドは、`system.cpu.time` メトリクスをフィルタリングして抽出し、`cpu0` に焦点を当てます。メトリクスの state（例: `user`、`system`、`idle`、`interrupt`）と対応する値を表示します。

**Tests ターミナル** で以下のコマンドを実行し、`system.cpu.time` メトリクスを確認します。

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

{{% /notice %}}
