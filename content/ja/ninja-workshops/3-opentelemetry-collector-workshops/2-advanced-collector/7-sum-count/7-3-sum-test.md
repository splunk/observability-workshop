---
title: 7.3 Sum Connector のテスト
linkTitle: 7.3 Test Sum Connector
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Gateway を起動する**：
**Gateway terminal** ウィンドウで以下を実行します：

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent を起動する**：
**Agent terminal** ウィンドウで以下を実行します：

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Loadgen を起動する**：
**Spans terminal** ウィンドウで、以下の `loadgen` コマンドを使用して8つのスパンを送信します：

```bash { title="Loadgen" }
../loadgen -count 8
```

**Agent** と **Gateway** の両方がデバッグ情報を表示し、データを処理していることを示します。loadgen が完了するまで待ちます。

**メトリクスを確認する**：
スパンを処理する際、**Agent** はメトリクスを生成して **Gateway** に転送します。**Gateway** はそれらを `gateway-metrics.out` に書き込みます。

メトリクス出力に `user.card-charge` が存在し、それぞれに `user.name` 属性があることを確認するには、以下の jq クエリを実行します：

{{% tabs %}}
{{% tab title="jq query command" %}}

```bash

jq -r '.resourceMetrics[].scopeMetrics[].metrics[] | select(.name == "user.card-charge") | .sum.dataPoints[] | "\(.attributes[] | select(.key == "user.name").value.stringValue)\t\(.asDouble)"' gateway-metrics.out | while IFS=$'\t' read -r name charge; do
    printf "%-20s %s\n" "$name" "$charge"
done
```

{{% /tab %}}
{{% tab title="jq example output" %}}

```text
George Lucas         67.49
Frodo Baggins        87.14
Thorin Oakenshield   90.98
Luke Skywalker       51.37
Luke Skywalker       65.56
Thorin Oakenshield   67.5
Thorin Oakenshield   66.66
Peter Jackson        94.39
```

{{% /tab %}}
{{% /tabs %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して **Agent** と **Gateway** のプロセスを停止してください。

{{% /notice %}}
