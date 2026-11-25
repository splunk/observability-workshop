---
title: 6. Conversion Funnels
weight: 6
---

Individual actions and frustration signals tell part of the story. **Conversion funnel analyses** show whether users complete multi-step journeys — like browsing to checkout — and where they drop off.

See [Analyses in Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/analyses-in-digital-experience-analytics) and [Create conversion funnel analysis](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/analyses-in-digital-experience-analytics/create-conversion-funnel-analysis) for documentation.

{{% exercise title="Explore the checkout funnel" %}}

1. Return to the project **Analyses** tab and open the **`Homepage to Order Confirmation`** funnel.
2. Confirm the chart is filtered to show **All users**.

This funnel tracks users from the homepage through shopping and checkout. Drop-off between steps is captured automatically based on the event definitions we reviewed earlier.

{{% notice title="Keep in mind" style="primary" icon="lightbulb" %}}
Think about critical journeys in your own applications. How would you define the steps you want to monitor?
{{% /notice %}}

3. Review the funnel visualization and click drop-off segments to view relevant user sessions.

![Conversion funnel from homepage to order confirmation showing drop-off percentages at each checkout step](../images/funnel.webp)

Funnels like this help teams monitor whether users succeed, troubleshoot where they fail, and optimize journeys for better conversion.

{{< quiz question="Which drop-off segment is most worth investigating first?" >}}
{{< quiz-option >}}Between Homepage and Click product.{{< /quiz-option >}}
{{< quiz-option >}}Between Click product and Add to cart.{{< /quiz-option >}}
{{< quiz-option >}}Between Add to cart and Place order.{{< /quiz-option >}}
{{< quiz-option correct=true >}}Between Place order and Order confirmation.{{< /quiz-option >}}
{{< quiz-feedback >}}
Leaving from the homepage or a product page, or abandoning a cart, is relatively expected. A high drop-off between **Place order** and **Order confirmation** is alarming, because users who intend to buy should reach confirmation.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

## Investigate the checkout drop-off

The most concerning segment is users who placed an order but never reached order confirmation. Let's find out why.

{{% exercise title="Examine the drop-off" %}}

1. On the **`Homepage to Order Confirmation`** funnel, click the drop-off segment between **Place order** and **Order confirmation**.
2. Open a session replay from that segment. Pause, click events in the timeline, and scrub through the playback.

{{< quiz question="What happened for the end user in the replay?" >}}
{{< quiz-option >}}The order was confirmed, but the confirmation page took a long time to load.{{< /quiz-option >}}
{{< quiz-option correct=true >}}The user submitted the order form but received an error message with a phone number to call instead of a confirmation page.{{< /quiz-option >}}
{{< quiz-option >}}The user abandoned the cart before submitting the order form.{{< /quiz-option >}}
{{< quiz-feedback >}}
In many workshop sessions, the user submits the order form but receives an error message with a phone number to call instead of a confirmation page. The user tried to complete a purchase and failed at the final step, which is a direct hit to conversion rate and revenue.

![Session replay showing a checkout error message after the user submits an order](../images/funnel-dropoff-replay.webp)
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

Checkout failure affects all users — but not always equally. **User segments** let us compare how different groups experience the same funnel.
