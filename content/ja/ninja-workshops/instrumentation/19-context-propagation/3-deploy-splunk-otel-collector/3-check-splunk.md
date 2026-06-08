---
title: 3. Splunk の確認
weight: 3
---

## Splunk でインフラストラクチャメトリクスを確認する

{{% notice title="注意" style="green" icon="running" %}}

デプロイ後、インフラストラクチャメトリクスが表示されるまで **2〜5 分**かかる場合があります。

{{% /notice %}}

1. **Infrastructure → Kubernetes**（または **Infrastructure Monitoring**）を開きます
2. クラスター **`trace-workshop`**（`k8s.cluster.name`）でフィルタリングします
3. ノードの CPU/メモリおよび Pod メトリクス（例: `k8s.node.*`、`k8s.pod.*`、`system.cpu.*`）が表示されることを確認します

{{% notice title="注意" style="grey" icon="running" %}}
すべてのインフラストラクチャメトリクスには `k8s.cluster.name=trace-workshop-<your-Initials>`（`workshop-config` ConfigMap の `K8S_CLUSTER_NAME` から設定）がタグ付けされています。
{{% /notice %}}

インフラストラクチャメトリクスが表示されない場合:

| 確認項目 | アクション |
| ----- | ------ |
| Agent DaemonSet | `kubectl get pods -n trace-workshop -l app=splunk-otel-collector-agent` — すべて Ready であること |
| Agent ログ | `kubectl logs daemonset/splunk-otel-collector-agent -n trace-workshop` — kubelet TLS エラーがないこと |
| RBAC | ServiceAccount `splunk-otel-collector` が ClusterRole `splunk-otel-collector-workshop` を持っていること |
| トークン | Ingest トークンに **Infrastructure Monitoring** 権限が含まれていること |
| クラスターフィルター | Splunk IMM で **k8s.cluster.name** = `trace-workshop` を設定すること |

## Splunk で APM データを確認する

1. **APM → Services** を開きます
2. **Environment** を `WORKSHOP_ENV` の値（例: `trace-propagation-workshop`）に設定します
3. **storefront-service**、**payment-proxy**、**inventory-service** がリストに表示されることを確認します

サービスが表示されない場合:

| 確認項目 | アクション |
| ----- | ------ |
| トークン | APM 権限を持つ **ingest** アクセストークンを使用すること（RUM 専用トークンではないこと） |
| Realm | `SPLUNK_REALM` を組織に合わせること（US0 → `us0`、EU0 → `eu0`） |
| Environment フィルター | APM で **Environment** = `WORKSHOP_ENV` の値を設定すること |
| 時間範囲 | トラフィック生成後に **Last 15 minutes** に設定すること |
| Collector ログ | `kubectl logs deployment/splunk-otel-collector -n trace-workshop` |
| Traces パイプライン | 設定で `otlphttp` を使用して `https://ingest.<realm>.signalfx.com/v2/trace/otlp` に送信すること |

## Splunk APM で ServiceMap とトレースを観察する（Phase 1）

1. **APM → Traces** を開きます
2. **Environment** を `trace-propagation-workshop`（または `WORKSHOP_ENV` の値）に設定します
3. サービスを **storefront-service** でフィルタリングし、トレースウォーターフォールを開きます

### Collector が稼働した後に確認できること

| ホップ | Splunk トレースの動作 |
| --- | --------------------- |
| **storefront → inventory-service** | **相関あり** — 両方のサービスのスパンが**同じトレース**に表示されます |
| **storefront → payment-service** | **相関なし** — `payment-service` は**別のルートトレース**として表示されます |
| **payment-proxy** | 通常は **storefront と同じトレース**に含まれます（storefront からのインバウンド）。分断は payment への**アウトバウンド**ホップで発生します |
| **payment-service → order-service** | **相関あり** — payment から order への HTTP は**1 つのトレース**（payment のルートトレース）にリンクされます |
| **order-service → RabbitMQ → fulfilment-service** | **RabbitMQ は推論サービスとして表示**されます（order トレース上の publish/receive スパン、`messaging.system=rabbitmq`、`server.address=rabbitmq`）。**order と fulfilment のトレースは切断されたまま**です — Phase 1 では AMQP メッセージにトレースコンテキストがありません |

{{% notice title="演習" style="green" icon="running" %}}

この非対称性は意図的なものです。HTTP 自動計装はヘッダーが保持される場所でコンテキストを伝播できますが、**メッセージバス**は Phase 2（Steps 7–8）で修正するまでトレースコンテキストを伝達しません。

{{% /notice %}}

### トレースが接続または分断される理由

{{% notice title="注意" style="info" %}}
**APM → Service map** では、Trace Analyzer ウォーターフォールが payment レッグで切断されている場合でも、依存関係が表示されます。
{{% /notice %}}

| ホップ | 動作の説明 |
| --- | ------------ |
| Client → edge proxy | storefront に到達する前に `traceparent` が削除されます |
| Storefront → **inventory**（直接 HTTP） | `filter_headers_for_mode()` が `inject_outbound_headers()` からヘッダーを削除しますが、Splunk OTel の **`requests` 自動計装**が W3C `traceparent` を注入します。**inventory-service**（`auto` モード）が W3C を抽出し、トレースがリンクされます。 |
| Storefront → **payment-proxy** | 同じ `requests` 計装により、インバウンドホップで storefront と payment-proxy がリンクされる場合があります |
| **payment-proxy → payment-service** | Proxy が W3C と `X-Workshop-Trace` を**削除**し、`suppress_instrumentation()` を使用します — **payment-service** は**新しいトレースルート**を開始します |
| **payment-service → order-service**（HTTP） | Payment が `inject_outbound_headers()` と **`requests` 自動計装**で order を呼び出し、order-service がインバウンド HTTP で抽出します — **payment と同じトレース**になります |
| **order-service → RabbitMQ** | Order が Splunk メッセージングタグ（`messaging.destination.name`、`server.address`）付きの **PRODUCER/CONSUMER** スパンを発行するため、トレースウォーターフォールで **RabbitMQ が推論サービスとして表示**されます |
| **RabbitMQ → fulfilment-service** | Phase 1: メッセージに**トレースヘッダーなし**、pika 自動計装は無効、fulfilment consumer は Step 7 でキャリアを公開しない限り**新しいルート**を使用します |
| Fulfilment → email | Phase 2 Steps 7–9 まで別々のルートが続きます |
