---
title: 7.2 Setup Environment
linkTitle: 7.2 Setup Environment
weight: 2
---

{{% notice title="演習" style="green" icon="running" %}}

**Gateway を起動**: **Gateway terminal** で以下を実行します。

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent を起動**: **Agent terminal** で以下を実行します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Load Generator を起動**: **Logs terminal** ウィンドウを開き、`loadgen` を実行します。

> [!IMPORTANT]
> ログを JSON 形式で構造化するため、スクリプト起動時に `-json` フラグを必ず指定してください。

```bash { title="Log Generator" }
../loadgen -logs -json -count 5
```

`loadgen` は `./quotes.log` に JSON 形式で 5 行のログを書き込みます。

{{% /notice %}}
