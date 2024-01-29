---
title: Summary
linkTitle: 5.8 Summary
weight: 8
---

{{% badge icon="clock" style="primary" %}}2 minutes{{% /badge %}} 

In this workshop we learned the following: 

* What are tags and why are they such a critical part of making an application observable.
* How to use [**OpenTelemetry**](https://opentelemetry.io) to capture tags of interest from your application.
* How to index tags in **Splunk Observability Cloud** and the differences between **Troubleshooting MetricSets** and **Monitoring MetricSets**.
* How to utilize tags in **Splunk Observability Cloud** to find “unknown unknowns” using the **Tag Spotlight** and **Dynamic Service Map** features.
* How to utilize tags for alerting and dashboards.

Collecting tags aligned with the best practices shared in this workshop will let you get even more value from the data you’re sending to **Splunk Observability Cloud**.  Now that you’ve completed this workshop, you have the knowledge you need to start collecting tags from your own applications!

To get started with capturing tags today, check out [how to add tags in various supported languages](https://docs.splunk.com/observability/en/apm/span-tags/add-context-trace-span.html#instrument-your-application-code-to-add-tags-to-spans), and then [how to use them to create Troubleshooting MetricSets](https://docs.splunk.com/observability/en/apm/span-tags/index-span-tags.html#apm-index-span-tags) so they can be analyzed in Tag Spotlight. For more help, feel free to [ask a Splunk Expert](https://www.splunk.com/en_us/about-splunk/contact-us.html).

{{% notice title="Tip for Workshop Facilitator(s)" style="primary"  icon="lightbulb" %}}
Once the workshop is complete, remember to delete the APM MetricSet you created earlier for the `credit.score.category` tag. 

  {{% /notice %}}