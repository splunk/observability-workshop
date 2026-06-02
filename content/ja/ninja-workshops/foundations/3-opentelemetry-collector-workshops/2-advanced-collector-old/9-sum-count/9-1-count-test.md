---
title: 9.1 Count Connector のテスト
linkTitle: 9.1 Count Connector のテスト
weight: 1
---

{{% notice title="演習" style="green" icon="running" %}}

**Gateway を起動する**:  
**Gateway terminal** ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動して、次のコマンドを実行します。

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent を起動する**:  
**Agent terminal** ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動して、次のコマンドを実行します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Loadgen で 12 行のログを送信する**:  
**Spans terminal** ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動します。  
12 行のログを送信します。これらは 2 つのインターバルで読み込まれます。次の `loadgen` コマンドで実行します。

```bash { title="Loadgen" }
../loadgen -logs -json -count 12
```

`agent` と `gateway` の両方が、データを処理していることを示すデバッグ情報を表示します。loadgen が完了するまで待機してください。

**メトリクスが生成されたことを確認する**  
ログが処理されると、**Agent** はメトリクスを生成し、**Gateway** に転送します。**Gateway** はそれを `gateway-metrics.out` に書き込みます。

メトリクス `logs.full.count`、`logs.sw.count`、`logs.lotr.count`、`logs.error.count` が出力に含まれているかを確認するため、次の **jq** クエリを実行します。

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
補足: 通常 `logs.full.count` は `logs.sw.count` + `logs.lotr.count` と等しくなりますが、`logs.error.count` はランダムな数値になります。
{{% /notice %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、`agent` と `gateway` のプロセスを停止してください。

{{% /notice %}}
