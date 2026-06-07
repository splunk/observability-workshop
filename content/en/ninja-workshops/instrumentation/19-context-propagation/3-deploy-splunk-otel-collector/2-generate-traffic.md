---
title: 2. (Optional) Generate Traffic
weight: 2
---

{{% exercise title="Generate Traffic" %}}

## Confirm Collector Health

```bash
curl -s http://localhost:13133/
```

---

### Generate Traffic

Allow **2–5 minutes** after the first request for services to appear.

```bash
curl -s http://localhost:8080/api/order | jq '{order_id, product, tier, amount, inventory: .inventory.reserved, payment: .payment.approved, fulfilment: .fulfilment.carrier}'
```

OR send Continuous load (recommended):

```bash
./scripts/4-start-load.sh
```

You should see a JSON response like:

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

The request flows through all services. But right now, the data is fragmented in Splunk.

{{% /exercise %}}
