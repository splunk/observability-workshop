---
title: 5.2 環境のセットアップ
linkTitle: 5.2 環境のセットアップ
weight: 2
---

{{% exercise title="変換テストのセットアップ" %}}

**Gatewayの起動**: **Gatewayターミナル** で以下を実行します

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agentの起動**: **Agentターミナル** で以下を実行します

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Load Generatorの起動**: **Loadgenターミナル** で、以下のコマンドを実行して **JSONを有効** にしたLoad Generatorを起動します

```bash { title="Log Generator" }
../loadgen -logs -json -count 5
```

`loadgen` は5行のログをJSON形式で `./quotes.log` に書き込みます。

{{% /exercise %}}
