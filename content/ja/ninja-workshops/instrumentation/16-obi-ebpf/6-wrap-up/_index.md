---
title: Wrap Up
linkTitle: 6. Wrap Up
weight: 6
archetype: chapter
time: 5 minutes
description: 主な学びのポイント、クリーンアップ手順、ワークショップを発展させるためのアイデアを紹介します。
---

## 主な学びのポイント

1. **OBI はカーネルから計装します。** SDK もコード変更も再コンパイルも不要です。eBPF プローブがネットワークレベルで HTTP/gRPC トラフィックを観測します。

2. **コンテキスト伝播はネットワークレベルで行われます。** OBI は送信される HTTP リクエストに `Traceparent` ヘッダーを注入し、トレーシングをまったく認識していないサービス間でもトレースを連結します。

3. **デプロイメントパターンは一貫しています。** ベアメタル、Docker、Kubernetes のいずれの場合でも、アプローチは同じです。アプリと並べて OBI を実行し、コレクターを指し示すだけです。

4. **これは現実のエンタープライズの課題を解決します。** レガシーアプリ、コンパイル済みバイナリ、規制上の制約、開発者からの抵抗 OBI はコードを変更せずにオブザーバビリティを実現します。

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

## ワークショップを発展させる

すべてのフェーズを完了したら、LLM（Cursor、Copilot、ChatGPT など）を使ってワークショップを発展させるアイデアをいくつか紹介します。

### 新しいエンドポイントを追加する

LLM に依頼して `order-processor` に `GET /order-status/:id` エンドポイントを追加してみてください。OBI は設定変更なしで自動的にトレースします（すでにポート 8080 を監視しています）。

### 新しいサービスを追加する

LLM に依頼してポート 8082 で動作する Python（Flask）の `inventory-service` を作成してみてください。以下の作業が必要です。

- サービスのコードと Dockerfile を作成する
- `docker-compose.yaml` に追加する
- `obi-config.yaml` にポート 8082 を追加する

### エラーシナリオを追加する

LLM に依頼して `payment-service` が 20% の確率でランダムに 500 ステータスで失敗するようにしてみてください。そして `order-processor` にリトライロジックを追加します。Splunk APM にエラー率が表示されるのを確認してください。

### レイテンシーシミュレーションを追加する

LLM に依頼して `payment-service` に 100〜500ms のランダムなレイテンシーを追加してみてください。Splunk APM のサービスビューにレイテンシー分布が表示されるのを確認してください。

{{% notice title="Note" style="info" %}}
発展させる際の注意点

- OpenTelemetry SDK は **追加しないでください**。ゼロコード計装こそがポイントです
- サービスは Docker ネットワーク上に保ち、サービス間通信に `localhost` を使わないでください
- 新しいポートを追加する際は `obi-config.yaml` を更新してください
- コード変更後は再ビルドしてください: `docker-compose up --build -d`
{{% /notice %}}
