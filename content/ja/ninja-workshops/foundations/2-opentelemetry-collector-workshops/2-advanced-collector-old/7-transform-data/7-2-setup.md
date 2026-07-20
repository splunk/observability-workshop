---
title: 7.2 環境のセットアップ
linkTitle: 7.2 環境のセットアップ
weight: 2
---

{{% notice title="演習" style="green" icon="running" %}}

**Gatewayの起動**: **Gatewayターミナル** で以下を実行します

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agentの起動**: **Agentターミナル** で以下を実行します

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Load Generatorの起動**: **Logsターミナル** ウィンドウを開き、`loadgen` を実行します。

> [!IMPORTANT]
> ログがJSON形式で構造化されるようにするため、スクリプトの起動時に `-json` フラグを含めてください。

```bash { title="Log Generator" }
../loadgen -logs -json -count 5
```

`loadgen` はJSON形式で5行のログを `./quotes.log` に書き込みます。

{{% /notice %}}
