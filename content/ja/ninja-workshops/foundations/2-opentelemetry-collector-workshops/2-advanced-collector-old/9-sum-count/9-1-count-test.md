---
title: 9.1 Count Connectorのテスト
linkTitle: 9.1 Count Connectorのテスト
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Gatewayの起動**:  
**Gatewayターミナル**ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動し、以下を実行します:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agentの起動**:  
**Agentターミナル**ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動し、以下を実行します:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Loadgenで12行のログを送信**:  
**Spansターミナル**ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動します。  
12行のログを送信します。これらは2つのインターバルで読み取られます。以下の `loadgen` コマンドを実行します:

```bash { title="Loadgen" }
../loadgen -logs -json -count 12
```

`agent` と `gateway` の両方がデバッグ情報を表示し、データを処理していることが確認できます。loadgenが完了するまで待ちます。

**メトリクスが生成されたことを確認**  
ログが処理されると、**Agent** がメトリクスを生成し、**Gateway** に転送します。Gatewayはそれらを `gateway-metrics.out` に書き込みます。

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
> それぞれのターミナルで `Ctrl-C` を押して、`agent` と `gateway` のプロセスを停止してください。

{{% /notice %}}
