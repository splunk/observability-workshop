---
title: 4.3 障害をシミュレートする
linkTitle: 4.3 障害をシミュレートする
weight: 3
---

**Agent** のレジリエンスを評価するため、`gateway` の一時的な停止をシミュレートし、`agent` がどのように対処するかを観察します。

**概要**:

1. **Agent にトレースを送信** – `agent` にトレースを送信してトラフィックを生成します。
2. **Gateway を停止** – これにより `agent` がリトライモードに入ります。
3. **Gateway を再起動** – `agent` は永続キューからトレースを復元し、正常に転送します。永続キューがなければ、これらのトレースは永久に失われていたでしょう。

{{% notice title="演習" style="green" icon="running" %}}

**ネットワーク障害をシミュレートする**: **Gateway terminal** で `Ctrl-C` を使って `gateway` を停止し、gateway のコンソールに停止したことが表示されるまで待ちます。

```text
2025-01-28T13:24:32.785+0100  info  service@v0.120.0/service.go:309  Shutdown complete.
```

**トレースを送信する**: **Spans terminal** ウィンドウで、`loadgen` を使ってさらに 5 つのトレースを送信します。

agent がデータの再送信を継続的に試みることでリトライメカニズムが起動することに注目してください。agent のコンソール出力には、以下のような繰り返しメッセージが表示されます。

```text
2025-01-28T14:22:47.020+0100  info  internal/retry_sender.go:126  Exporting failed. Will retry the request after interval.  {"kind": "exporter", "data_type": "traces", "name": "otlphttp", "error": "failed to make an HTTP request: Post \"http://localhost:5318/v1/traces\": dial tcp 127.0.0.1:5318: connect: connection refused", "interval": "9.471474933s"}
```

**Agent を停止する**: **Agent terminal** ウィンドウで、`Ctrl-C` を使って agent を停止します。agent のコンソールに停止したことが表示されるまで待ちます。

```text
2025-01-28T14:40:28.702+0100  info  extensions/extensions.go:66  Stopping extensions...
2025-01-28T14:40:28.702+0100  info  service@v0.120.0/service.go:309  Shutdown complete.
```

{{% /notice %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
agent を停止すると、リトライ試行が停止し、以降のリトライ動作が発生しなくなります。

agent がデータを正常に配信できないまま長時間動作し続けると、リトライ設定によってはメモリを節約するためにトレースをドロップし始める場合があります。agent を停止することで、メモリ内に現在保持されているメトリクス、トレース、ログがドロップされる前に失われ、復旧時に利用可能な状態を保つことができます。

このステップは、agent を再起動した際の復旧プロセスを明確に観察するために不可欠です。
{{% /notice %}}
