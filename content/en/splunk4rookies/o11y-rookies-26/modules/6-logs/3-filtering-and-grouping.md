---
title: 3. Find the business event
weight: 3
time: 6 minutes
---

Checkout emits several messages while processing a purchase. Use its **`order placed`** event to focus on completed purchases, then inspect the fields you will use to compare each order's value with its charge.

{{% exercise title="Inspect the order's business fields" %}}

1. Keep the search scope and investigation window from Step 2.
2. Select **Add Filter → Keyword**, enter **`order placed`**, and select **include**. Select **Run search**.
3. Open a row in the **Logs table** and confirm that the `message` field in its JSON body is `order placed`.

These completion events give you a consistent set of purchases to investigate.

4. Locate **`app.order.amount.usd`** and **`app.order.amount.charged.usd`** in the JSON body or **Fields** list. These are the two fields you will add as columns in Step 4. Use the reference below to distinguish them from the native-currency amounts.

| Field | Meaning |
|---|---|
| `app.order.id` | Identifies the order |
| `app.order.currency` | The shopper's currency |
| `app.order.amount` | Full order value in that currency |
| `app.order.amount.charged` | Amount charged in that currency |
| `app.order.amount.usd` | Full order value expressed in USD |
| `app.order.amount.charged.usd` | Amount charged expressed in USD |

Use the two USD fields to compare order values and charges on a consistent currency basis across rows. Native amounts can be in different currencies, so a JPY value and a USD value are not directly comparable.

![A completed order with matching full and charged amounts in its structured business fields](../images/order-fields-healthy.jpg "Example: an unaffected completed order. Your order IDs and amounts will differ.")

Close the event details pane to return to the results table. Keep the search filters and time window unchanged.

{{% /exercise %}}

An individual order may be unaffected. Next, add the amount fields as columns so you can compare more orders in the same search.
