---
title: 2.3 障害のシミュレーション
linkTitle: 2.3 Simulate Failure
weight: 3
---

**Agent** の耐障害性を評価するために、一時的な **Gateway** の停止をシミュレートし、**Agent** がそれをどのように処理するかを観察します：

{{% notice title="Exercise" style="green" icon="running" %}}

**ネットワーク障害のシミュレーション**: **Gateway ターミナル** で `Ctrl-C` を使用して **Gateway** を停止し、Gateway のコンソールが停止したことを示すまで待ちます。**Agent** は引き続き実行されますが、Gateway にデータを送信できません。**Gateway ターミナル** の出力は以下のようになります：

```text
2025-07-09T10:22:37.941Z        info    service@v0.126.0/service.go:345 Shutdown complete.      {"resource": {}}
```

**トレースの送信**: **Loadgen ターミナル** ウィンドウで、`loadgen` を使用してさらに5つのトレースを送信します。

```bash { title="Start Load Generator" }
../loadgen -count 5
```

Agent のリトライメカニズムが有効になり、データを再送信しようと継続的に試みていることに注目してください。Agent のコンソール出力には、以下のようなメッセージが繰り返し表示されます：

```text
2025-01-28T14:22:47.020+0100  info  internal/retry_sender.go:126  Exporting failed. Will retry the request after interval.  {"kind": "exporter", "data_type": "traces", "name": "otlphttp", "error": "failed to make an HTTP request: Post \"http://localhost:5318/v1/traces\": dial tcp 127.0.0.1:5318: connect: connection refused", "interval": "9.471474933s"}
```

**Agent の停止**: **Agent ターミナル** ウィンドウで、`Ctrl-C` を使用して Agent を停止します。Agent のコンソールが停止を確認するまで待ちます：

```text
2025-07-09T10:25:59.344Z        info    service@v0.126.0/service.go:345 Shutdown complete.      {"resource": {}}
```

{{% /notice %}}

> [!IMPORTANT]
> Agent を停止すると、リトライ用にメモリに保持されているメトリクス、トレース、ログは失われます。ただし、FileStorage Extension を設定しているため、ターゲットエンドポイントでまだ受け入れられていないすべてのテレメトリーはディスクに安全にチェックポイントされています。
>
> Agent の停止は、Agent が再起動されたときにシステムがどのように復旧するかを明確に示すための重要なステップです。
