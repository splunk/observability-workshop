---
title: まとめ
linkTitle: 6. まとめ
weight: 6
archetype: chapter
time: 5 minutes
description: 主要なポイント、クリーンアップ手順、およびワークショップを拡張するためのアイデアについて説明します。
---

## 主要なポイント

1. **OBI はカーネルから計装を行います。** SDK も、コード変更も、再コンパイルも不要です。eBPF プローブはネットワークレベルで HTTP/gRPC トラフィックを監視します。

2. **コンテキストの伝播はネットワークレベルで行われます。** OBI は送信 HTTP リクエストに `Traceparent` ヘッダーを注入し、サービスがトレースについて何も知らなくても、サービス間でトレースをリンクします。

3. **デプロイパターンは一貫しています。** ベアメタル、Docker、Kubernetes のいずれであっても、アプローチは同じです。アプリと一緒に OBI を実行し、コレクターに向けるだけです。

4. **これは実際のエンタープライズの問題を解決します。** レガシーアプリ、コンパイル済みバイナリ、規制上の制約、開発者の抵抗 - OBI はコードを変更することなくオブザーバビリティを提供します。

## クリーンアップ

### Kubernetes

``` bash
helm uninstall splunk-otel-collector
kubectl delete namespace obi-workshop
```

### Docker

``` bash
cd ~/workshop/obi/02-obi-docker
docker-compose down
```

### Phase 0 (Python)

``` bash
sudo pkill -f ./obi 2>/dev/null
kill %1 2>/dev/null
```

## ワークショップの拡張

すべてのフェーズを完了したら、LLM（Cursor、Copilot、ChatGPT など）を使用してワークショップを拡張するアイデアをいくつか紹介します。

### 新しいエンドポイントの追加

LLM に `order-processor` に `GET /order-status/:id` エンドポイントを追加するよう依頼してください。OBI は自動的にトレースします。設定の変更は不要です（すでにポート 8080 を監視しています）。

### 新しいサービスの追加

LLM にポート 8082 で Python（Flask）の `inventory-service` を作成するよう依頼してください。以下を行う必要があります

- サービスコードと Dockerfile を作成する
- `docker-compose.yaml` に追加する
- `obi-config.yaml` にポート 8082 を追加する

### エラーシナリオの追加

LLM に `payment-service` が 20% の確率でランダムに 500 ステータスで失敗するようにしてもらいます。その後、`order-processor` にリトライロジックを追加します。Splunk APM でエラー率が表示されるのを確認してください。

### レイテンシシミュレーションの追加

LLM に `payment-service` にランダムな 100-500ms のレイテンシを追加するよう依頼してください。Splunk APM のサービスビューでレイテンシ分布が表示されるのを確認してください。

{{% notice title="Note" style="info" %}}
拡張する際の注意点

- OpenTelemetry SDK を追加**しないでください**：ゼロコード計装がポイントです
- サービスは Docker ネットワーク上に維持してください。サービス間呼び出しに `localhost` を使用しないでください
- 新しいポートを追加する場合は `obi-config.yaml` を更新してください
- コード変更後は再ビルドしてください`docker-compose up --build -d`
{{% /notice %}}
