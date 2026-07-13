---
title: Gateway修正の再デプロイ
weight: 1
time: 5 minutes

---

## 保存後のリビルドと再デプロイ

{{% notice title="注意" style="info" %}}
`server.js` を保存しただけでは、リビルドと再起動を行うまで実行中のPodは更新 **されません** 。
{{% /notice %}}

プロジェクトルートから実行します:

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

ヘルスチェックは、Spanがアクティブなときに `buildUpstreamHeaders()` が `traceparent` ヘッダーを追加するかどうかを検査します。`propagation.inject()` を追加すると自動的に `true` に変わります。

{{% /tab %}}
{{< /tabs >}}

#### 2. テスト注文を行いTraceを確認

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

```text
**APM → Traces** で、`payment-api` の最新のTraceを開きます。この修正後は以下のようになります:

| チェック項目 | 期待される結果 |
|-------|----------|
| `payment-api` SpanのParent | `payment-gateway` の子 |
| `payment-gateway` SpanのParent | frontend-apiの購入フローに接続 |
| 同じTrace内の `fulfillment-worker` | **いいえ** — ステップ09まで未修正 |
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="注意" style="info" %}}
このワークショップではNode.jsプロキシを使用して、 **アプリケーション層** のpropagationバグ（BFFやカスタムゲートウェイでよく見られる）を実践します。ステップ06のNGINX ConfigMapアプローチは、 **インフラストラクチャプロキシ** 層で断絶が発生している場合に適用されます。
{{% /notice %}}

## トラブルシューティング

{{< details summary="トラブルシューティングガイダンスはこちらをクリック" >}}

#### 問題1. 修正後もTraceが切断されたまま

- `services/payment-gateway/server.js` を **保存** し、 **`make fix-payment-gateway`** （リビルド + インポート + 再起動）を実行したことを確認します
- Podが最近のAGEで再起動されていることを確認します: `kubectl -n cosmic-shop get pods -l app=payment-gateway`
- ヘルスが `"propagation": true` を表示していることを確認します
- **新しい** トラフィックを生成します。古いTraceは遡って変更されません

#### 問題2. ヘルスが `"propagation": false` のまま

- `propagation.inject()` が `buildUpstreamHeaders()` 内にあり、`return headers` の **前に** 実行されることを確認します
- upstream fetchパスから `suppressTracing()` を削除したことを確認します
- フルリビルドチェーンを再実行します。イメージがリビルドされていない場合、再起動だけでは不十分です

#### 問題3. ゲートウェイのセットアップがNGINX / ConfigMapプロキシを使用している場合

一部のチームでは、Node.jsプロキシの代わりに **APIゲートウェイまたはNGINXサイドカー** で決済ルーティングを実装しています。障害モードはステップ06と同じで、`proxy_set_header traceparent` ディレクティブが欠落しています。

組織でそのパターンを使用している場合、修正はJavaScriptではなく **ConfigMap** の変更（`gateway-config.yaml`）になります:

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
