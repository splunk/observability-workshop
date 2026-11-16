---
title: 4. Find and explain the discrepancy
weight: 4
time: 6 minutes
---

Use the completed-order search from Step 3. You will add columns to the **Logs table** so each row shows an order's value, charge, and eventually the reason for the difference.

Keep the same connection, index, environment, checkout service, `order placed` event, and investigation window. Retain any required USD currency filter. Keep all completed orders in the results; adding columns changes the table display without changing your search.

{{% exercise title="Show the order value and amount charged" %}}

1. Select the **Configure Table** gear above the Logs table to open **Table Settings**. Deselect `_raw` to make room for the business fields; Severity and Time remain visible.
2. Select **`app.order.amount.usd`**, then **`app.order.amount.charged.usd`**. Use the settings search box to find each field, keeping both selected.

   ![Table Settings with both USD amount fields selected alongside the default Severity and Time columns](../images/order-column-settings.jpg "Select the two USD amount fields in Table Settings.")

3. Select **Apply Changes**. Read the two amounts side by side on each row. Scan the results for an order whose amounts differ and one whose amounts match.

![Completed-order results with full USD value and charged USD value in adjacent columns](../images/order-amount-columns.jpg "The two amount columns appear together in the results table. Your amounts will differ.")

Some rows have a positive full order value but **zero charged**. Other rows show matching amounts. You can see affected and unaffected purchases together in the same search results.

The difference shows what needs investigating, but does not yet explain why it happened. A blank cell is missing data, not a zero charge.

{{% /exercise %}}

{{% exercise title="Add the discount percentage" %}}

Add the discount percentage to see whether a discount accounts for the smaller charges.

1. Reopen **Configure Table**, find and select **`app.order.discount.pct`**, then select **Apply Changes**. Keep the two amount columns selected.
2. Read the discount percentage alongside the amounts on the same rows.

![The same completed-order results with a discount percentage column added](../images/order-discount-column.jpg "The discount percentage appears beside the two amount columns.")

The displayed zero-charge orders have a **100% discount**. The full-price orders have a **0% discount**. You may also see orders with a **10% discount**. This explains the arithmetic, but you still need to understand which promotion applied and whether it was intended.

{{% /exercise %}}

{{% exercise title="Identify the promotion" %}}

1. Reopen **Configure Table**, find and select **`app.promo.code`**, then select **Apply Changes**. Keep the amount and discount columns selected.
2. Scan several zero-charge and full-price rows. Look for a recurring relationship between the promotion, discount, and charge. Drag column borders if needed to read the full field names.

![The same results with full value, charged amount, discount percentage, and promotion code visible together](../images/order-promo-column.jpg "The promotion code completes the four-column view of each order.")

The zero-charge rows show **PROMOTEST100** with a **100% discount**. The full-price rows show **NONE** with a **0% discount**. Any **SPRING10** rows show a **10% discount**. The repeated association points the investigation toward the promotion rules.

{{% /exercise %}}

{{% exercise title="Explain the discrepancy" %}}

Use one zero-charge row and one full-price row in your table to summarize the relationship between the order value, charged amount, discount percentage, and promo code. Use this evidence to explain the payment discrepancy and recommend what the development team should correct.

The requests complete successfully, so request errors and latency do not explain the incorrect charge. The business fields in the logs reveal the discrepancy.

In this scenario, the intended marketing promotion is **SPRING10**, offering **10% off**. An internal test promotion, **PROMOTEST100**, remains in the pricing rules. When a shopper's promotion resolves to the test code, the charge becomes zero.

The logs establish the observed pattern. **Recommend correcting the promotion selection and pricing rules to prevent the test promotion from applying while preserving the legitimate 10% campaign.**

{{% /exercise %}}

Logs let you investigate a business outcome even when request-health signals look normal. Next, you will save a reusable search for orders with an unexpected zero charge and plan how to verify recovery.

{{< presenter >}}
Begin with the default columns so learners reveal the amounts, discount percentage, and promotion in sequence. Use the prepared window containing affected and unaffected orders. If no zero-charge orders appear, confirm the scenario and window before continuing; do not treat normal transactions or legitimate discounts as evidence of the leak. The examples use recorded scenario data from 10 November 2026, 16:40–16:45 UTC (11:40–11:45 EST), including full-price orders, legitimate 10% discounts, and the faulty 100% discounts.
{{< /presenter >}}
