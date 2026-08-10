---
title: Gateway修正の再デプロイ
weight: 1
time: 5 minutes

---

## 保存後のリビルドと再デプロイ

{{% notice title="注意" style="info" %}}
`server.js` を保存しただけでは、リビルドと再起動を行うまで実行中のPodは更新 **されません**。
{{% /notice %}}

プロジェクトルートから実行します

```bash
bash scripts/build-images.sh payment-gateway
bash scripts/import-images-k3d.sh payment-gateway
kubectl -n cosmic-shop rollout restart deployment/payment-gateway
kubectl -n cosmic-shop rollout status deployment/payment-gateway --timeout=180s
```

## 検証チェックリスト

再デプロイが完了した後、以下のコマンドを実行します。

#### 1. ヘルスエンドポイントがpropagationを報告していることを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
kubectl -n cosmic-shop exec deploy/payment-gateway -- wget -qO- http://localhost:3004/health
```

{{% /tab %}}
{{% tab title="出力例" %}}

```json
{"status":"ok","service":"payment-gateway","stage":"proxy","propagation":true}
```

ヘルスチェックは、Spanがアクティブなときに `buildUpstreamHeaders()` が `traceparent` ヘッダーを追加するかどうかを検査します。`propagation.inject()` を追加すると自動的に `true` に切り替わります。

{{% /tab %}}
{{< /tabs >}}

#### 2. テスト注文を行いトレースを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
curl -s -X POST http://localhost:30080/api/purchases \
  -H "Content-Type: application/json" \
  -d '{"productId":"telescope-orion-8","quantity":1,"customerEmail":"gateway-test@cosmic.shop"}' \
  | python3 -m json.tool
```

{{% /tab %}}
{{% tab title="出力例" %}}

```json
{
    "message": "Purchase complete — order placed and payment submitted for fulfillment",
    "order": {
        "orderId": "ORD-1783667419611",
        "productId": "telescope-orion-8",
        "productName": "Orion 8\" Dobsonian Telescope",
        "quantity": 1,
        "total": 449.99,
        "customerEmail": "gateway-test@cosmic.shop",
        "createdAt": "2026-07-10T07:10:19.611Z",
        "requestTraceId": "6891d2d87734d4959214491bb2c600af"
    },
    "payment": {
        "paymentId": "PAY-1783667419703",
        "orderId": "ORD-1783667419611",
        "amount": 449.99,
        "status": "authorized",
        "method": "stellar-credits",
        "processedAt": "2026-07-10T07:10:19.703Z"
    }
}
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="注意" style="info" %}}
このワークショップではNode.jsプロキシを使用しており、**アプリケーション層** のpropagationバグ（BFFやカスタムゲートウェイでよく見られる）を実践します。Step 06のNGINX ConfigMapアプローチは、問題が **インフラストラクチャプロキシ** 層にある場合に適用されます。
{{% /notice %}}

## トラブルシューティング

{{< details summary="トラブルシューティングガイダンスはこちらをクリック" >}}

#### 考えられる問題 1. 修正後もトレースが切断されたまま

- `services/payment-gateway/server.js` を **保存** し、**`make fix-payment-gateway`**（リビルド＋インポート＋再起動）を実行したことを確認してください
- Podが最近のAGEで再起動されたことを確認します: `kubectl -n cosmic-shop get pods -l app=payment-gateway`
- ヘルスが `"propagation": true` を示していることを確認します
- **新しい** トラフィックを生成します。古いトレースは遡って変更されません

#### 考えられる問題 2. ヘルスが依然として `"propagation": false` を示す

- `propagation.inject()` が `buildUpstreamHeaders()` 内にあり、`return headers` の **前に** 実行されることを確認してください
- アップストリームfetchパスから `suppressTracing()` を削除したことを確認してください
- フルリビルドチェーンを再実行します。イメージがリビルドされていない場合、再起動だけでは不十分です

#### 考えられる問題 3. GatewayセットアップがNGINX / ConfigMapプロキシを使用している場合

一部のチームではNode.jsプロキシの代わりに **APIゲートウェイまたはNGINXサイドカー** でペイメントルーティングを実装しています。障害モードはStep 06と同じで、`proxy_set_header traceparent` ディレクティブが欠落しています。

組織でそのパターンを使用している場合、修正はJavaScriptではなく（`gateway-config.yaml`への）**ConfigMap** の変更になります

```nginx
location /payments/ {
    proxy_set_header Host $host;
    proxy_set_header traceparent $http_traceparent;
    proxy_set_header tracestate $http_tracestate;
    proxy_set_header baggage $http_baggage;
    proxy_pass http://payment_api;
}
```

{{< /details >}}
