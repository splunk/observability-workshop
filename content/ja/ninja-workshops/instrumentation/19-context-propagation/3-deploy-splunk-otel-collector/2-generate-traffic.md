---
title: 2. (オプション) トラフィックの生成
weight: 2
---

{{% exercise title="トラフィックの生成" %}}

## Collector の正常性を確認する

```bash
curl -s http://localhost:13133/
```

---

### トラフィックを生成する

最初のリクエスト後、サービスが表示されるまで **2〜5分** お待ちください。

```bash
curl -s http://localhost:8080/api/order | jq '{order_id, product, tier, amount, inventory: .inventory.reserved, payment: .payment.approved, fulfilment: .fulfilment.carrier}'
```

または、継続的な負荷を送信します（推奨）:

```bash
./scripts/4-start-load.sh
```

以下のような JSON レスポンスが表示されます:

``` json
{
  "order_id": "ord-56584",
  "product": "widget",
  "tier": "enterprise",
  "amount": 999.98,
  "inventory": true,
  "payment": true,
  "fulfilment": "fedex"
}
```

リクエストはすべてのサービスを通過します。しかし、現時点では Splunk 上のデータは断片化されています。

{{% /exercise %}}
