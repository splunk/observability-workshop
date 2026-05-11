---
title: まとめ
linkTitle: 6. まとめ
weight: 6
archetype: chapter
time: 5 minutes
description: 重要なポイント、クリーンアップ手順、およびワークショップを拡張するためのアイデアです。
---

## 重要なポイント

1. **OBI はカーネルからインストルメントします。** SDK もコード変更も再コンパイルも不要です。eBPF プローブがネットワークレベルで HTTP/gRPC トラフィックを観測します。

2. **コンテキスト伝播はネットワークレベルで行われます。** OBI は送信 HTTP リクエストに `Traceparent` ヘッダーを注入し、サービスがトレーシングについて一切認識していなくてもサービス間でトレースをリンクします。

3. **デプロイパターンは一貫しています。** ベアメタル、Docker、Kubernetes のいずれであっても、アプローチは同じです。アプリケーションと一緒に OBI を実行し、コレクターに向けるだけです。

4. **これは実際のエンタープライズの問題を解決します。** レガシーアプリ、コンパイル済みバイナリ、規制上の制約、開発者の抵抗 — OBI は誰にもコードの変更を求めることなくオブザーバビリティを提供します。

## クリーンアップ

### Kubernetes

``` bash
kill %1 2>/dev/null; # kill port forward
helm -n obi-workshop uninstall splunk-otel-collector
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

すべてのフェーズを完了したら、LLM（Cursor、Copilot、ChatGPT など）を使用してワークショップを拡張するアイデアをご紹介します

### 新しいエンドポイントの追加

LLM に `order-processor` へ `GET /order-status/:id` エンドポイントを追加するよう依頼します。OBI は自動的にトレースします — 設定変更は不要です（すでにポート 8080 を監視しています）。

### 新しいサービスの追加

LLM にポート 8082 で Python（Flask）の `inventory-service` を作成するよう依頼します。以下の作業が必要です

- サービスコードと Dockerfile の作成
- `docker-compose.yaml` への追加
- `obi-config.yaml` にポート 8082 を追加

### エラーシナリオの追加

LLM に `payment-service` が 20% の確率でランダムに 500 ステータスで失敗するようにしてもらいます。次に `order-processor` にリトライロジックを追加します。Splunk APM でエラー率が表示されるのを確認します。

### レイテンシシミュレーションの追加

LLM に `payment-service` にランダムな 100〜500ms のレイテンシを追加してもらいます。Splunk APM のサービスビューでレイテンシ分布が表示されるのを確認します。

{{% notice title="Note" style="info" %}}
拡張する際の注意事項

- OpenTelemetry SDK を追加**しないでください**：ゼロコードインストルメンテーションが目的です
- サービスは Docker ネットワーク上に保持し、サービス間通信に `localhost` を使用しないでください
- 新しいポートを追加する場合は `obi-config.yaml` を更新してください
- コード変更後はリビルドしてください`docker-compose up --build -d`
{{% /notice %}}
