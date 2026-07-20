---
title: 2.3 障害のシミュレーション
linkTitle: 2.3 障害のシミュレーション
weight: 3
---

**Agent** の回復力を評価するために、一時的な **Gateway** の停止をシミュレーションし、**Agent** がどのように処理するかを観察します。

{{% exercise title="Gatewayの停止をシミュレーションする" %}}

**ネットワーク障害のシミュレーション**: **Gatewayターミナル** で `Ctrl-C` を使用して **Gateway** を停止し、Gatewayコンソールに停止が表示されるまで待ちます。**Agent** は引き続き実行されますが、Gatewayにデータを送信できなくなります。**Gatewayターミナル** の出力は以下のようになります。

```text
2025-07-09T10:22:37.941Z        info    service@v0.126.0/service.go:345 Shutdown complete.      {"resource": {}}
```

**トレースの送信**: **Loadgenターミナル** ウィンドウで `loadgen` を使用してさらに5つのトレースを送信します。

```bash { title="Start Load Generator" }
../loadgen -count 5
```

Agentのリトライメカニズムが作動し、データの再送信を継続的に試みていることに注目してください。Agentのコンソール出力に、以下のようなメッセージが繰り返し表示されます。

```text
2025-01-28T14:22:47.020+0100  info  internal/retry_sender.go:126  Exporting failed. Will retry the request after interval.  {"kind": "exporter", "data_type": "traces", "name": "otlphttp", "error": "failed to make an HTTP request: Post \"http://localhost:5318/v1/traces\": dial tcp 127.0.0.1:5318: connect: connection refused", "interval": "9.471474933s"}
```

**Agentの停止**: **Agentターミナル** ウィンドウで `Ctrl-C` を使用してAgentを停止します。Agentのコンソールに停止が確認されるまで待ちます。

```text
2025-07-09T10:25:59.344Z        info    service@v0.126.0/service.go:345 Shutdown complete.      {"resource": {}}
```

{{% /exercise %}}

> [!IMPORTANT]
> Agentを停止すると、リトライのためにメモリに保持されていたメトリクス、トレース、またはログは失われます。しかし、FileStorage Extensionを設定しているため、ターゲットエンドポイントにまだ受け入れられていないすべてのテレメトリはディスク上に安全にチェックポイントされています。
>
> Agentの停止は、Agentが再起動されたときにシステムがどのように回復するかを明確に示すための重要なステップです。
