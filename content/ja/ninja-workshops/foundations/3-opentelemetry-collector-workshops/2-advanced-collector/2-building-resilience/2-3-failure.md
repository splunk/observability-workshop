---
title: 2.3 障害をシミュレートする
linkTitle: 2.3 障害をシミュレートする
weight: 3
---

**Agent** の回復力を評価するために、**Gateway** の一時的な障害をシミュレートし、**Agent** がそれをどのように処理するかを観察します。

{{% exercise title="Gateway の障害をシミュレートする" %}}

**ネットワーク障害をシミュレートする**: **Gateway terminal** で `Ctrl-C` を使って **Gateway** を停止し、ゲートウェイのコンソールに停止したと表示されるまで待ちます。**Agent** は実行を継続しますが、データをゲートウェイに送信できなくなります。**Gateway terminal** の出力は次のようになります。

```text
2025-07-09T10:22:37.941Z        info    service@v0.126.0/service.go:345 Shutdown complete.      {"resource": {}}
```

**トレースを送信する**: **Loadgen terminal** ウィンドウで `loadgen` を使ってさらに 5 件のトレースを送信します。

```bash { title="Start Load Generator" }
../loadgen -count 5
```

エージェントのリトライ機構が動作し、データの再送を継続的に試みていることに気づくでしょう。エージェントのコンソール出力には、次のようなメッセージが繰り返し表示されます。

```text
2025-01-28T14:22:47.020+0100  info  internal/retry_sender.go:126  Exporting failed. Will retry the request after interval.  {"kind": "exporter", "data_type": "traces", "name": "otlphttp", "error": "failed to make an HTTP request: Post \"http://localhost:5318/v1/traces\": dial tcp 127.0.0.1:5318: connect: connection refused", "interval": "9.471474933s"}
```

**Agent を停止する**: **Agent terminal** ウィンドウで `Ctrl-C` を使ってエージェントを停止します。エージェントのコンソールに停止が確認されるまで待ちます。

```text
2025-07-09T10:25:59.344Z        info    service@v0.126.0/service.go:345 Shutdown complete.      {"resource": {}}
```

{{% /exercise %}}

> [!IMPORTANT]
> エージェントを停止すると、リトライのためにメモリに保持されているメトリクス、トレース、ログは失われます。ただし、FileStorage Extension を構成しているため、ターゲットエンドポイントによってまだ受け入れられていないテレメトリーはすべてディスクに安全にチェックポイントされます。
>
> エージェントを停止することは、エージェントが再起動された際にシステムがどのように回復するかを明確に示すための重要なステップです。
