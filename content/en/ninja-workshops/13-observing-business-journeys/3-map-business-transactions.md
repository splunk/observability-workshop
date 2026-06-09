---
title: 3. Map Business Transactions
weight: 3
time: 25 minutes
---

The purpose of a business transaction map is to connect technical telemetry to a user-visible or business-visible outcome. Start with the customer journey, then map the services that support each step.

The lab mapping lives in:

```text
workshop/observing-business-journeys/mappings/astronomy-shop-business-map.yaml
```

## Transaction Inventory

| Business transaction | Customer outcome | Entry points | Primary supporting services | Impact statement |
|---|---|---|---|---|
| Browse Catalog | Customer can view products and recommendations. | `/`, `/api/products`, `/api/recommendations` | `frontend`, `product-catalog`, `recommendation`, `ad`, `currency` | Discovery and conversion are degraded. |
| Manage Cart | Customer can add, view, and clear cart items. | `/api/cart` | `frontend`, `cart`, `valkey-cart` | Customers cannot build an order. |
| Complete Checkout | Customer can place an order and payment can be authorized. | `/api/checkout` | `frontend`, `checkout`, `payment`, `shipping`, `currency`, `cart` | Revenue is directly at risk. |
| Confirm Order | Customer receives confirmation and order events are processed. | checkout completion, Kafka order events | `email`, `accounting`, `kafka`, `postgresql` | Fulfillment, compliance, and customer trust are at risk. |

## Mapping Questions

For each transaction, answer:

- What customer or business outcome does this transaction represent?
- Which route, span name, service, or message topic marks the start of the transaction?
- Which services are required for success?
- Which services are optional or can fail gracefully?
- Which team owns the business outcome?
- What severity should a technical issue become when this transaction is impacted?
- What numeric impact estimate can incident leaders understand?

## Mapping Exercise

Open the map file:

```bash
sed -n '1,220p' workshop/observing-business-journeys/mappings/astronomy-shop-business-map.yaml
```

Review the `transactions` list and update these fields for your own demo story:

- `owner`
- `criticality`
- `business_impact`
- `estimated_revenue_per_minute`
- `slo`

{{< tabs >}}
{{% tab title="Question" %}}
Why should checkout and cart be separate business transactions if checkout calls cart?
{{% /tab %}}
{{% tab title="Answer" %}}
Because they represent different customer outcomes and different response priorities. A cart issue blocks customers before revenue capture, while a checkout issue creates immediate revenue risk and usually needs higher ITSI importance.
{{% /tab %}}
{{< /tabs >}}

## What Good Looks Like

A useful map is small enough for responders to understand during an incident, but specific enough to drive detector routing, ITSI service dependencies, and business impact language. Do not model every internal call as a business transaction.
