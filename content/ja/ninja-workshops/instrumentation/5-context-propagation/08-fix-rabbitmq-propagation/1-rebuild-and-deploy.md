---
title: RabbitMQ修正の再デプロイ
weight: 1
time: 5 minutes

---

## 保存後のリビルドと再デプロイ

プロジェクトルートから以下を実行します

```bash
bash scripts/build-images.sh payment-api fulfillment-worker
bash scripts/import-images-k3d.sh payment-api fulfillment-worker
kubectl -n cosmic-shop rollout restart deployment/payment-api
kubectl -n cosmic-shop rollout restart deployment/fulfillment-worker
kubectl -n cosmic-shop rollout status deployment/payment-api --timeout=180s
kubectl -n cosmic-shop rollout status deployment/fulfillment-worker --timeout=180s
```

## 検証チェックリスト

再デプロイが完了した後、以下のコマンドを実行します。

#### 1. ヘルスエンドポイントがpropagation有効を報告していることを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
kubectl -n cosmic-shop get pods -l app=fulfillment-worker
kubectl -n cosmic-shop exec deploy/fulfillment-worker -- wget -qO- http://localhost:3006/health
kubectl -n cosmic-shop exec deploy/payment-api -- wget -qO- http://localhost:3005/health
```

{{% /tab %}}
{{% tab title="出力例" %}}

```json
{"status":"ok","service":"payment-api","stage":"payment","rabbitmq":true,"propagation":true}
{"status":"ok","service":"fulfillment-worker","stage":"fulfillment","propagation":true}
```

{{% /tab %}}
{{< /tabs >}}

#### 2. ロールアウトが完了したことを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
kubectl -n cosmic-shop rollout status deployment/payment-api
kubectl -n cosmic-shop rollout status deployment/fulfillment-worker
```

{{% /tab %}}
{{< /tabs >}}

#### 3. 起動ログにpropagationが記載されていることを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
kubectl -n cosmic-shop logs deployment/payment-api --tail=3
kubectl -n cosmic-shop logs deployment/fulfillment-worker --tail=3
```

{{% /tab %}}
{{% tab title="出力例" %}}

```
RabbitMQ context propagation: ENABLED
RabbitMQ context propagation: ENABLED
```

{{% /tab %}}
{{< /tabs >}}

## トラブルシューティング

{{< details summary="トラブルシューティングガイダンスはこちら" >}}

#### 考えられる問題 1. Fulfillment workerがまだ孤立したトレースを表示する

- **両方** のファイルが編集されていることを確認します（producerのinject + consumerのextract）
- **`make fix-rabbitmq`** を実行したことを確認します（両方のイメージをリビルドします。再起動だけでは不十分です）
- 両方のヘルスエンドポイントが `"propagation": true` を表示していることを確認します
- 修正後に **新しい** 注文を生成します

#### 考えられる問題 2. payment-apiのヘルスのみがtrueになる

consumerのスタブを `extractTraceContext()` に置き換える必要があります。producerのみの修正では不十分です。

#### 考えられる問題 3. 別のパターン: 自動計装

一部のチームでは、手動のinject/extractの代わりに **`@opentelemetry/instrumentation-amqplib`**（OpenTelemetry JS contrib）を使用しています。

障害モードは同じで、計装が無効または設定が誤っている場合ですが、publish/consumeコードを編集する代わりに `instrumentation.js` でライブラリを有効にすることで問題が解決されます。

このワークショップでは生の `amqplib` を使用しています。これはNode.jsサービスでまだ一般的であり、inject/extractのコントラクトを明示的にするためです。
{{< /details >}}
