---
title: 2.3 AgentからGatewayへメトリクスを送信する
linkTitle: 2.3 Send Metrics
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Agentの起動**: **Agentターミナル**ウィンドウで、更新した設定を使用してAgentを起動します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**CPUメトリクスの確認**:

1. `agent`が起動すると、すぐに **CPU** メトリクスの送信を開始することを確認します。
2. `agent`と`gateway`の両方がデバッグ出力にこのアクティビティを表示します。出力は以下のスニペットのようになります。

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

この段階では、`agent`は1時間ごとまたは再起動のたびに **CPU** メトリクスを収集し続け、Gatewayに送信します。

`gateway`はこれらのメトリクスを処理し、`./gateway-metrics.out`というファイルにエクスポートします。このファイルは、パイプラインサービスの一部としてエクスポートされたメトリクスを保存します。

**Gatewayにデータが到達したことを確認**: CPUメトリクス（特に`cpu0`）がGatewayに正常に到達したことを確認するために、`jq`コマンドを使用して`gateway-metrics.out`ファイルを検査します。

以下のコマンドは、`system.cpu.time`メトリクスをフィルタリングして`cpu0`に焦点を当てて抽出します。メトリクスの状態（例: `user`、`system`、`idle`、`interrupt`）と対応する値を表示します。

**Testsターミナル**で以下のコマンドを実行して`system.cpu.time`メトリクスを確認します。

{{% tabs %}}
{{% tab title="CPUメトリクスの確認" %}}

```bash
jq '.resourceMetrics[].scopeMetrics[].metrics[] | select(.name == "system.cpu.time") | .sum.dataPoints[] | select(.attributes[0].value.stringValue == "cpu0") | {cpu: .attributes[0].value.stringValue, state: .attributes[1].value.stringValue, value: .asDouble}' gateway-metrics.out
```

{{% /tab %}}
{{% tab title="出力例" %}}

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
