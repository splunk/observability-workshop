---
title: まとめ
linkTitle: 6. まとめ
weight: 6
archetype: chapter
time: 5 minutes
description: 重要なポイント、クリーンアップ手順、およびワークショップを拡張するためのアイデアです。
---

## 重要なポイント

1. **OBI はカーネルから計装します。** SDKも、コード変更も、再コンパイルも不要です。eBPFプローブはネットワークレベルでHTTP/gRPCトラフィックを監視します。

2. **コンテキスト伝播はネットワークレベルで行われます。** OBIは送信HTTPリクエストに `Traceparent` ヘッダーを注入し、サービス間でトレースを連携させます。これはサービスがトレースについて何も知らなくても機能します。

3. **デプロイパターンは一貫しています。** ベアメタル、Docker、Kubernetesのいずれであっても、アプローチは同じです。アプリケーションと一緒にOBIを実行し、コレクターに向けるだけです。

4. **これは実際の企業の問題を解決します。** レガシーアプリ、コンパイル済みバイナリ、規制上の制約、開発者の抵抗 -- OBIは誰にもコードを変更させることなくオブザーバビリティを提供します。

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

すべてのフェーズを完了したら、LLM（Cursor、Copilot、ChatGPTなど）を使用してワークショップを拡張するためのアイデアをご紹介します。

### 新しいエンドポイントの追加

LLMに `order-processor` へ `GET /order-status/:id` エンドポイントを追加するよう依頼します。OBIは自動的にトレースします -- 設定変更は不要です（すでにポート8080を監視しています）。

### 新しいサービスの追加

LLMにPython（Flask）でポート8082上に `inventory-service` を作成するよう依頼します。以下が必要です：

- サービスコードとDockerfileの作成
- `docker-compose.yaml` への追加
- `obi-config.yaml` へのポート8082の追加

### エラーシナリオの追加

LLMに `payment-service` を20% の確率でランダムに500ステータスで失敗させるよう依頼します。次に `order-processor` にリトライロジックを追加します。Splunk APMでエラー率が表示されるのを確認します。

### レイテンシシミュレーションの追加

LLMに `payment-service` にランダムな100-500msのレイテンシを追加するよう依頼します。Splunk APMのサービスビューでレイテンシ分布が表示されるのを確認します。

{{% notice title="注意" style="info" %}}
拡張する際の注意点：

- OpenTelemetry SDKを追加**しないでください** -- ゼロコード計装がポイントです
- サービスはDockerネットワーク上に維持してください。サービス間呼び出しに `localhost` を使用しないでください
- 新しいポートを追加する場合は `obi-config.yaml` を更新してください
- コード変更後は再ビルドしてください: `docker-compose up --build -d`
{{% /notice %}}
