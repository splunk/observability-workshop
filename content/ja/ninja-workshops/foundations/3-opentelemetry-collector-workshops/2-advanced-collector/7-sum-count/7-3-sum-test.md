---
title: 7.3 Count Connector のテスト
linkTitle: 7.3 Sum Connector のテスト
weight: 3
---

{{% exercise title="Sum Connector のテスト" %}}

**Gateway を起動します**:  
**Gateway terminal** ウィンドウで次のコマンドを実行します。

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent を起動します**:  
**Agent terminal** ウィンドウで次のコマンドを実行します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Loadgen を起動します**:  
**Spans terminal** ウィンドウで、次の `loadgen` コマンドを使用して 8 個のスパンを送信します。

```bash { title="Loadgen" }
../loadgen -count 8
```

**Agent** と **Gateway** の両方がデバッグ情報を表示し、データを処理していることを示します。loadgen が完了するまでお待ちください。

**メトリクスを確認します**:  
スパンの処理中に、**Agent** はメトリクスを生成し、**Gateway** に渡しています。**Gateway** はそれらを `gateway-metrics.out` に書き込んでいます。

メトリクス出力に `user.card-charge` が存在することを確認し、それぞれが `user.name` 属性を持っていることを検証するために、次の jq クエリを実行します。

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
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止します。

{{% /exercise %}}
