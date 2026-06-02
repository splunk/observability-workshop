---
title: 7.1 Count Connector のテスト
linkTitle: 7.1 Count Connector のテスト
weight: 1
---

{{% exercise title="Count Connector のテスト" %}}

**Gateway を起動します**:  
**Gateway ターミナル** ウィンドウで次のコマンドを実行します。

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent を起動します**:  
**Agent ターミナル** ウィンドウで次のコマンドを実行します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Loadgen で 12 行のログを送信します**:  
**Spans ターミナル** ウィンドウで 12 行のログを送信します。これらは 2 つのインターバルに分けて読み取られます。次の `loadgen` コマンドを実行してください。

```bash { title="Loadgen" }
../loadgen -logs -json -count 12
```

**Agent** と **Gateway** の両方がデバッグ情報を表示し、データを処理していることを示します。`loadgen` が完了するまで待ちます。

**メトリクスが生成されたことを確認します**  
ログが処理されると、**Agent** はメトリクスを生成して **Gateway** に転送し、**Gateway** はそれらを `gateway-metrics.out` に書き込みます。

`logs.full.count`、`logs.sw.count`、`logs.lotr.count`、`logs.error.count` のメトリクスが出力に含まれているかを確認するには、次の **jq** クエリを実行します。

{{% tabs %}}
{{% tab title="jq query command" %}}

```bash
jq '.resourceMetrics[].scopeMetrics[].metrics[]
    | select(.name == "logs.full.count" or .name == "logs.sw.count" or .name == "logs.lotr.count" or .name == "logs.error.count")
    | {name: .name, value: (.sum.dataPoints[0].asInt // "-")}' gateway-metrics.out
```

{{% /tab %}}
{{% tab title="jq example output" %}}

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
注: `logs.full.count` は通常 `logs.sw.count` + `logs.lotr.count` と等しくなりますが、`logs.error.count` はランダムな数値になります。
{{% /notice %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止します。

{{% /exercise %}}
