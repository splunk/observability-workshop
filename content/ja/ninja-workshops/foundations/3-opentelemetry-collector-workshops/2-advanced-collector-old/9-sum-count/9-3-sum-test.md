---
title: 9.3 Count Connector のテスト
linkTitle: 9.3 Sum Connector のテスト
weight: 3
---

{{% notice title="演習" style="green" icon="running" %}}

**Gateway の起動**:  
**Gateway ターミナル**ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動し、以下を実行します:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent の起動**:  
**Agent ターミナル**ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動し、以下を実行します:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Loadgen の起動**:  
**Spans ターミナル**ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動します。以下の `loadgen` コマンドで 8 つのスパンを送信します:

```bash { title="Loadgen" }
../loadgen -count 8
```

`agent` と `gateway` の両方がデバッグ情報を表示し、データを処理していることが確認できます。loadgen が完了するまで待ちます。

**メトリクスの確認**  
スパンの処理中に、**Agent** がメトリクスを生成し、**Gateway** に渡しています。**Gateway** はそれらを `gateway-metrics.out` に書き込んでいます。

メトリクス出力に `user.card-charge` が存在し、各データポイントに `user.name` 属性があることを確認するには、以下の jq クエリを実行します:

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
> それぞれのターミナルで `Ctrl-C` を押して、`agent` と `gateway` のプロセスを停止してください。

{{% /notice %}}
