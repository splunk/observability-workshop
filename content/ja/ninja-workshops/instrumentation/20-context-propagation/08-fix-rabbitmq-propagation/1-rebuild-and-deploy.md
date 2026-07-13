---
title: RabbitMQ修正の再デプロイ
weight: 1
time: 5 minutes

---

## 保存後のリビルドと再デプロイ

プロジェクトルートから以下の手順を実行します。

```bash
bash scripts/build-images.sh payment-api fulfillment-worker
bash scripts/import-images-k3d.sh payment-api fulfillment-worker
kubectl -n cosmic-shop rollout restart deployment/payment-api
kubectl -n cosmic-shop rollout restart deployment/fulfillment-worker
kubectl -n cosmic-shop rollout status deployment/payment-api --timeout=180s
kubectl -n cosmic-shop rollout status deployment/fulfillment-worker --timeout=180s
```

## 検証チェックリスト

再デプロイ完了後に以下のコマンドを実行します。

#### 1. ヘルスエンドポイントでpropagationが有効であることを確認

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

#### 2. ロールアウトの完了を確認

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

#### 4. テスト注文を行い、ワーカーの処理を確認

{{% notice title="検証" style="green" icon="running" %}}
再デプロイ後に **新しい** 注文を行ってください。修正前に発行されたメッセージにはトレースコンテキストが含まれていません。
{{% /notice %}}

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
curl -s -X POST http://localhost:30080/api/purchases \
  -H "Content-Type: application/json" \
  -d '{"productId":"filter-nebula-uhc","quantity":1,"customerEmail":"propagation-test@cosmic.shop"}' \
  | python3 -m json.tool

sleep 2
kubectl -n cosmic-shop logs deployment/fulfillment-worker --tail=3
```

{{% /tab %}}
{{< /tabs >}}

## トラブルシューティング

{{< details summary="トラブルシューティングガイダンスはこちら" >}}

#### 問題1. Fulfillment workerがまだ孤立したトレースを表示する

- **両方** のファイルが編集されていることを確認します（producerのinject + consumerのextract）
- **`make fix-rabbitmq`** を実行したことを確認します（両方のイメージをリビルドします。再起動だけでは不十分です）
- 両方のヘルスエンドポイントで `"propagation": true` が表示されることを確認します
- 修正後に **新しい** 注文を生成します

#### 問題2. payment-apiのヘルスのみがtrueになる

consumerのスタブを `extractTraceContext()` に置き換える必要があります。producerのみを修正するだけでは不十分です。

#### 問題3. 代替パターン: 自動計装

一部のチームでは、手動のinject/extractの代わりに **`@opentelemetry/instrumentation-amqplib`**（OpenTelemetry JS contrib）を使用しています。

障害モードは同じで、計装が無効または設定ミスの場合ですが、publish/consumeコードを編集する代わりに `instrumentation.js` でライブラリを有効にすることで解決します。

このワークショップでは生の `amqplib` を使用しています。これはNode.jsサービスでまだ一般的であり、inject/extractの契約を明示的にするためです。
{{< /details >}}
