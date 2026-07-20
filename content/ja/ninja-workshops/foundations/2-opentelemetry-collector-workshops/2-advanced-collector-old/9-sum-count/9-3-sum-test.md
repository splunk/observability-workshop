---
title: 9.3 Count Connectorのテスト
linkTitle: 9.3 Sum Connectorのテスト
weight: 3
---

{{% notice title="エクササイズ" style="green" icon="running" %}}

**Gatewayの起動**:  
**Gatewayターミナル** ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動し、以下を実行します:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agentの起動**:  
**Agentターミナル** ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動し、以下を実行します:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Loadgenの起動**:  
**Spansターミナル** ウィンドウで `[WORKSHOP]/9-sum-count` ディレクトリに移動します。以下の `loadgen` コマンドで8つのSpanを送信します:

```bash { title="Loadgen" }
../loadgen -count 8
```

`agent` と `gateway` の両方がデバッグ情報を表示し、データを処理していることが確認できます。loadgenが完了するまで待ちます。

**メトリクスの確認**  
Spanの処理中に **Agent** がメトリクスを生成し、**Gateway** に渡しています。**Gateway** はそれらを `gateway-metrics.out` に書き込んでいます。

メトリクス出力で `user.card-charge` が存在し、各エントリに `user.name` 属性があることを確認するために、以下のjqクエリを実行します:

{{% tabs %}}
{{% tab title="jqクエリコマンド" %}}

```bash

jq -r '.resourceMetrics[].scopeMetrics[].metrics[] | select(.name == "user.card-charge") | .sum.dataPoints[] | "\(.attributes[] | select(.key == "user.name").value.stringValue)\t\(.asDouble)"' gateway-metrics.out | while IFS=$'\t' read -r name charge; do
    printf "%-20s %s\n" "$name" "$charge"
done    
```

{{% /tab %}}
{{% tab title="jq出力例" %}}

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
