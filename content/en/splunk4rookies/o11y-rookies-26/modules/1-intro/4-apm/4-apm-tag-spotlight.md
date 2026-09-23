---
title: 4. APM Tag Spotlight
weight: 4
---
**Tag Spotlight** groups service telemetry by indexed *tags*, such as endpoint, environment, customer attributes, and exception message. This helps you determine whether errors or latency are concentrated around a particular group of requests without writing a query.

Each card represents one *tag*. Because indexed tags can be configured for each environment, different users may see a different selection or order of cards. 

Within each card, you can compare tag values using request counts, error counts, root-cause errors, and latency percentiles. Within a card, you can compare its values using request counts, error counts, root-cause errors, and latency percentiles.

{{% exercise title="Identify the Error Pattern" %}}

You already know that the **payment** service is returning recurring *HTTP* **401** errors. You’ll now use **Tag Spotlight** to determine which requests are affected and find a more specific clue about the failure.
* Confirm that *Service* is set to *payment* and *Time* remains set to *Last 1 hour (-1h)*.
* Open the **card-display** options **(1)** and turn **off** *Show tags with no values* *(2)*. This hides empty cards and makes the relevant tags easier to find.
* Examine the available tag cards. Compare the request count, error count, root-cause-error count, and latency for each tag value.
* Identify the tag and value that most clearly separate the failed requests from the successful requests.

{{< notice >}}
**Tag Spotlight** is configurable. The *indexed tags*, *card order* and available *values* may differ from the screenshots. Focus on finding the tag value that has errors while its other values do not.
{{< /notice >}}

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Which tag and value are most strongly associated with the payment errors, and what evidence supports your conclusion?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The *version* tag shows that version *v350.10* is associated with the errors. In this example, all six requests for *v350.10* failed, while the requests for *v350.9* completed without errors. This suggests that the problem was introduced in, or is specific to, version *v350.10*. Your counts and version names may differ, but the same pattern should be visible.**
{{% /tab %}}
{{< /tabs >}}

* Now that we have identified the tag that indicates the issue, let's see if we can find out more information about the error.
* Click the **APM** link above **payment (3)** at the top of the page to return to the **APM Overview**.
* In **APM Overview**, select **Service Map** in the right-hand pane. This opens the full *Service Map*, showing the services in your application and the dependencies between them.
{{% /exercise %}}
