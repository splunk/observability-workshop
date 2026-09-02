---
title: 6. Conversion Funnels
weight: 6
time: 10 minutes
---

Individual actions and frustration signals tell part of the story. **Conversion funnel analyses** show whether users complete multi-step journeys — like browsing to checkout — and where they drop off.

See [Analyses in Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/analyses-in-digital-experience-analytics) and [Create conversion funnel analysis](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/analyses-in-digital-experience-analytics/create-conversion-funnel-analysis) for documentation.

{{% exercise title="Explore the checkout funnel" %}}

1. Return to the project **Analyses** tab and open the **`Homepage to Order Confirmation`** funnel.
2. Confirm the chart is filtered to show **All users**.

This funnel tracks users from the homepage through shopping and checkout. Drop-off between steps is captured automatically based on the event definitions you reviewed earlier.

{{% notice title="Keep in mind" style="primary" icon="lightbulb" %}}
Think about critical journeys in your own applications. How would you define the steps you want to monitor?
{{% /notice %}}

3. Review the funnel visualization and click drop-off segments to view relevant user sessions.

![Conversion funnel from homepage to order confirmation showing drop-off percentages at each checkout step](../images/funnel.png)

{{< tabs >}}
{{% tab title="Questions" %}}

1. How could a funnel like this be leveraged for your application?
1. Which drop-off segments seem more expected, and which are most worth investigating first?

{{% /tab %}}
{{% tab title="Answers" %}}

1. Funnels monitor expected user success, troubleshoot issues, and optimize apps for better conversion — a core tool for product and growth teams.
1. Visiting a homepage or product page, or abandoning a cart, are relatively expected. A high drop-off between **Place order** and **Order confirmation** is alarming — users who intend to buy should reach confirmation.

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

## Investigate the checkout drop-off

The most concerning segment is users who placed an order but never reached order confirmation. Let's find out why.

{{% exercise title="Examine the drop-off" %}}

1. On the **`Homepage to Order Confirmation`** funnel, click the drop-off segment between **Place order** and **Order confirmation**.
2. Open a session replay from that segment. Pause, click events in the timeline, and scrub through the playback.

{{< tabs >}}
{{% tab title="Questions" %}}

1. Which segment should you investigate?
1. What happened for the end user in the replay?

{{% /tab %}}
{{% tab title="Answers" %}}

1. The last drop-off segment — users who did not progress from **Place order** to **Order confirmation**.
1. In many workshop sessions, the user submits the order form but receives an error message with a phone number to call instead of a confirmation page. The user tried to complete a purchase and failed at the final step — a direct hit to conversion rate and revenue.

<!-- TODO screenshot: Session replay showing checkout error after placing an order -->

![Session replay showing a checkout error message after the user submits an order](../images/funnel-dropoff-replay.png)

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

Checkout failure affects all users — but not equally. **User segments** let you compare how different groups experience the same funnel.
