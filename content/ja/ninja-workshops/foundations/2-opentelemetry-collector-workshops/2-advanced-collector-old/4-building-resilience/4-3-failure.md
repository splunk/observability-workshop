---
title: 4.3 障害シミュレーション
linkTitle: 4.3 障害シミュレーション
weight: 3
---

**Agent** の耐障害性を評価するために、一時的な `gateway` の停止をシミュレーションし、`agent` がどのように対処するかを観察します。

**概要**

1. **Agent にトレースを送信する** – `agent` にトレースを送信してトラフィックを生成します。
2. **Gateway を停止する** – これにより `agent` がリトライモードに入ります。
3. **Gateway を再起動する** – `agent` が永続キューからトレースを回復し、正常に転送します。永続キューがなければ、これらのトレースは完全に失われていたでしょう。

{{% notice title="Exercise" style="green" icon="running" %}}

**ネットワーク障害のシミュレーション**: **Gateway terminal** で `Ctrl-C` を使って `gateway` を停止し、gatewayコンソールに停止が表示されるまで待ちます。

```text
2025-01-28T13:24:32.785+0100  info  service@v0.120.0/service.go:309  Shutdown complete.
```

**トレースの送信**: **Spans terminal** ウィンドウで `loadgen` を使用してさらに5つのトレースを送信します。

agentのリトライメカニズムが起動し、データの再送信を継続的に試みていることに注目してください。agentのコンソール出力に、以下のようなメッセージが繰り返し表示されます。

```text
2025-01-28T14:22:47.020+0100  info  internal/retry_sender.go:126  Exporting failed. Will retry the request after interval.  {"kind": "exporter", "data_type": "traces", "name": "otlphttp", "error": "failed to make an HTTP request: Post \"http://localhost:5318/v1/traces\": dial tcp 127.0.0.1:5318: connect: connection refused", "interval": "9.471474933s"}
```

**Agent の停止**: **Agent terminal** ウィンドウで `Ctrl-C` を使ってagentを停止します。agentのコンソールに停止が確認されるまで待ちます。

```text
2025-01-28T14:40:28.702+0100  info  extensions/extensions.go:66  Stopping extensions...
2025-01-28T14:40:28.702+0100  info  service@v0.120.0/service.go:309  Shutdown complete.
```

{{% /notice %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
agentを停止すると、リトライの試行が停止し、将来のリトライアクティビティも防止されます。

agentがデータの配信に成功せずに長時間実行されると、メモリを節約するために、リトライ設定に応じてトレースのドロップを開始する場合があります。agentを停止することで、メモリに保存されているメトリクス、トレース、またはログがドロップされる前に保持され、回復可能な状態を維持できます。

このステップは、agentの再起動時にリカバリプロセスを明確に観察するために不可欠です。
{{% /notice %}}
