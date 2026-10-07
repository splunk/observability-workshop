---
title: 3. APM Tag Spotlight
weight: 3
---

{{% exercise title="Find the bad version in Tag Spotlight" %}}

* Once in **Tag Spotlight** ensure the toggle **Show tags with no values** is off.

![APM Tag Spotlight](../images/apm-tag-spotlight.webp)

* This view displays a series of cards, each representing an indexed tag (such as Endpoint, Environment, Version, or custom tags like tenant.level). Within each card, you can see the distribution of tag values along with key metrics including request count, error count, root cause errors, and latency percentiles (P50, P90, P99).

{{< quiz question="Which card exposes the tag that identifies what the problem is?" >}}
{{< quiz-option correct=true >}}The version card. Requests for `v350.10` match the errors.{{< /quiz-option >}}
{{< quiz-option >}}The browser card.{{< /quiz-option >}}
{{< quiz-option >}}The region card.{{< /quiz-option >}}
{{< quiz-feedback >}}
**The *version* card. The number of requests against `v350.10` matches the number of errors, 100%.**
{{< /quiz-feedback >}}
{{< /quiz >}}

* Now that we have identified the tag that indicates the issue, let's see if we can find out more information about the error.
* Click the **APM** link above **paymentservice** at the top of the page to return to the **APM Overview**.
* In **APM Overview**, click on **Service Map** in the right-hand pane.
{{% /exercise %}}
