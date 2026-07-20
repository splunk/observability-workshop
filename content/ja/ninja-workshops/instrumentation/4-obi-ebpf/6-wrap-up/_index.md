---
title: まとめ
linkTitle: 6. まとめ
weight: 6
archetype: chapter
time: 5 minutes
description: 主なポイント、クリーンアップ手順、ワークショップを拡張するアイデア。
---

## 主なポイント

1. **OBIはカーネルから計装します。** SDKもコード変更も再コンパイルも不要です。eBPFプローブがネットワークレベルでHTTP/gRPCトラフィックを観測します。

2. **コンテキスト伝播はネットワークレベルで行われます。** OBIは送信HTTPリクエストに `Traceparent` ヘッダーを挿入し、サービスがトレーシングについて何も知らなくても、サービス間のTraceを関連付けます。

3. **デプロイパターンは一貫しています。** ベアメタル、Docker、Kubernetesのいずれでも、アプローチは同じです。アプリケーションと一緒にOBIを実行し、Collectorに向けるだけです。

4. **実際のエンタープライズの課題を解決します。** レガシーアプリケーション、コンパイル済みバイナリ、規制上の制約、開発者の抵抗感。OBIはコードを変更することなくオブザーバビリティを実現します。

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

すべてのフェーズを完了したら、LLM（Cursor、Copilot、ChatGPTなど）を使用してワークショップを拡張するアイデアを紹介します。

### 新しいエンドポイントの追加

LLMに `order-processor` へ `GET /order-status/:id` エンドポイントを追加するよう依頼します。OBIは自動的にトレースします。設定変更は不要です（すでにポート8080を監視しています）。

### 新しいサービスの追加

LLMにポート8082でPython（Flask）の `inventory-service` を作成するよう依頼します。以下が必要です。

- サービスコードとDockerfileの作成
- `docker-compose.yaml` への追加
- `obi-config.yaml` にポート8082を追加

### エラーシナリオの追加

LLMに `payment-service` がランダムに20%の確率で500ステータスを返すように依頼します。次に `order-processor` にリトライロジックを追加します。Splunk APMでエラー率を確認します。

### レイテンシシミュレーションの追加

LLMに `payment-service` にランダムな100〜500msのレイテンシを追加するよう依頼します。Splunk APMのサービスビューでレイテンシ分布を確認します。

{{% notice title="注意" style="info" %}}
拡張する際の注意点

- OpenTelemetry SDKを追加 **しないでください** 。ゼロコード計装がこのワークショップの目的です
- サービスはDockerネットワーク上に配置し、サービス間呼び出しに `localhost` を使用しないでください
- 新しいポートを追加する場合は `obi-config.yaml` を更新してください
- コード変更後はリビルドしてください: `docker-compose up --build -d`
{{% /notice %}}
