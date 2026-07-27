---
title: 5.2 Setup Environment
linkTitle: 5.2 Setup Environment
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Gateway を起動する**: **Gateway terminal** で以下を実行します

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent を起動する**: **Agent terminal** で以下を実行します

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Load Generator を起動する**: **Loadgen terminal** ウィンドウで、次のコマンドを実行して **JSON を有効**にした Load Generator を起動します

```bash { title="Log Generator" }
../loadgen -logs -json -count 5
```

`loadgen` は JSON 形式で 5 行のログを `./quotes.log` に書き込みます。

{{% /notice %}}
