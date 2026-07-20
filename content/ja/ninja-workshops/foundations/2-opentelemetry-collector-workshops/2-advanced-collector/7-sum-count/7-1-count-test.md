---
title: 7.1 Count Connectorのテスト
linkTitle: 7.1 Count Connectorのテスト
weight: 1
---

{{% exercise title="Count Connectorのテスト" %}}

**Gatewayの起動**:  
**Gatewayターミナル** ウィンドウで以下を実行します:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agentの起動**:  
**Agentターミナル** ウィンドウで以下を実行します:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Loadgenで12行のログを送信**:  
**Spansターミナル** ウィンドウで12行のログを送信します。これらは2回のインターバルで読み取られます。以下の `loadgen` コマンドを実行します:

```bash { title="Loadgen" }
../loadgen -logs -json -count 12
```

**Agent** と **Gateway** の両方がデバッグ情報を表示し、データを処理していることを示します。`loadgen` が完了するまで待ちます。

**メトリクスが生成されたことを確認**  
ログが処理されると、**Agent** がメトリクスを生成し、**Gateway** に転送します。Gateway はそれらを `gateway-metrics.out` に書き込みます。

メトリクス `logs.full.count`、`logs.sw.count`、`logs.lotr.count`、`logs.error.count` が出力に含まれているか確認するには、以下の **jq** クエリを実行します:

{{% tabs %}}
{{% tab title="jqクエリコマンド" %}}

```bash
jq '.resourceMetrics[].scopeMetrics[].metrics[]
    | select(.name == "logs.full.count" or .name == "logs.sw.count" or .name == "logs.lotr.count" or .name == "logs.error.count")
    | {name: .name, value: (.sum.dataPoints[0].asInt // "-")}' gateway-metrics.out
```

{{% /tab %}}
{{% tab title="jq出力例" %}}

```json
{
  "name": "logs.sw.count",
  "value": "2"
}
{
  "name": "logs.lotr.count",
  "value": "2"
}
{
  "name": "logs.full.count",
  "value": "4"
}
{
  "name": "logs.error.count",
  "value": "2"
}
{
  "name": "logs.error.count",
  "value": "1"
}
{
  "name": "logs.sw.count",
  "value": "2"
}
{
  "name": "logs.lotr.count",
  "value": "6"
}
{
  "name": "logs.full.count",
  "value": "8"
}
```

{{% /tab %}}
{{% /tabs %}}
{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
注意: `logs.full.count` は通常 `logs.sw.count` + `logs.lotr.count` と等しくなりますが、`logs.error.count` はランダムな数値になります。
{{% /notice %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止してください。

{{% /exercise %}}
