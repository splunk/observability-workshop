---
title: 4. APM Tag Spotlight
weight: 4
---
**Tag Spotlight** groups service telemetry by indexed *tags*, such as endpoint, environment, customer attributes, and exception message. This helps you determine whether errors or latency are concentrated around a particular group of requests without writing a query.

Each card represents one *tag*. Because indexed tags can be configured for each environment, different users may see a different selection or order of cards. 

Within each card, you can compare tag values using request counts, error counts, root-cause errors, and latency percentiles. Within a card, you can compare its values using request counts, error counts, root-cause errors, and latency percentiles.

{{% exercise title="Identify the Error Pattern" %}}

You already know that the **payment** service is returning recurring HTTP **401** errors. You’ll now use **Tag Spotlight** to determine which requests are affected and find a more specific clue about the failure.
* Confirm that *Service* is set to *payment* and *Time* remains set to *Last 1 hour (-1h)*.
* Open the **card-display** options **(1)** and turn **off** *Show tags with no values* *(2)*. This hides empty cards and makes the relevant tags easier to find.
* Locate the app.loyalty.level card (3). Compare the request and error counts for each loyalty level.

* Locate the exception.message card (4). Review the messages associated with the errors. If a message is truncated, hover over or select it to display the complete value.

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

* This view displays a series of cards, each representing an indexed tag (such as Endpoint, Environment, Version, or custom tags like tenant.level). Within each card, you can see the distribution of tag values along with key metrics including request count, error count, root cause errors, and latency percentiles (P50, P90, P99).

{{< tabs >}}
{{% tab title="Question" %}}
**Which card exposes the tag that identifies what the problem is?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The *version* card. The number of requests against `v350.10` matches the number of errors i.e. 100%**
{{% /tab %}}
{{< /tabs >}}

* Now that we have identified the tag that indicates the issue, let's see if we can find out more information about the error.
* Click the **APM** link above **paymentservice** at the top of the page to return to the **APM Overview**.
* In **APM Overview**, click on **Service Map** in the right-hand pane.
{{% /exercise %}}
