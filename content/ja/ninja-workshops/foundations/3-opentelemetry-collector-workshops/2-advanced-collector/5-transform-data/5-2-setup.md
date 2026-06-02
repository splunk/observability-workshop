---
title: 5.2 環境のセットアップ
linkTitle: 5.2 環境のセットアップ
weight: 2
---

{{% exercise title="transform テストのセットアップ" %}}

**Gateway を起動する**: **Gateway terminal** で以下を実行します。

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent を起動する**: **Agent terminal** で以下を実行します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Load Generator を起動する**: **Loadgen terminal** ウィンドウで、**JSON を有効化** した状態で以下のコマンドを実行し、ロードジェネレーターを起動します。

```bash { title="Log Generator" }
../loadgen -logs -json -count 5
```

`loadgen` は JSON 形式で 5 行のログを `./quotes.log` に書き込みます。

{{% /exercise %}}
