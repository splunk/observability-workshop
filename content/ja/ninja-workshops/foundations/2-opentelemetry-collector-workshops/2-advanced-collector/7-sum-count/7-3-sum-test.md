---
title: 7.3 Count Connectorのテスト
linkTitle: 7.3 Sum Connectorのテスト
weight: 3
---

{{% exercise title="Sum Connectorのテスト" %}}

**Gatewayの起動**:  
**Gatewayターミナル**ウィンドウで以下を実行します:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agentの起動**:  
**Agentターミナル**ウィンドウで以下を実行します:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Loadgenの起動**:  
**Spansターミナル**ウィンドウで、以下の `loadgen` コマンドを使用して8つのSpanを送信します:

```bash { title="Loadgen" }
../loadgen -count 8
```

**Agent** と **Gateway** の両方がデバッグ情報を表示し、データを処理していることを確認できます。loadgenが完了するまで待ちます。

**メトリクスの確認**:  
Spanの処理中に、**Agent** がメトリクスを生成し、**Gateway** に渡しています。**Gateway** はそれらを `gateway-metrics.out` に書き込んでいます。

`user.card-charge` の存在を確認し、メトリクス出力内の各エントリに `user.name` 属性があることを検証するために、以下のjqクエリを実行します:

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
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止します。

{{% /exercise %}}
