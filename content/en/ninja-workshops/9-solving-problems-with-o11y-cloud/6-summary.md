---
title: Summary
linkTitle: 6. Summary
weight: 6
time: 2 minutes
---

This workshop provided hands-on experience with the following concepts: 

* How to deploy the **Splunk Distribution of the OpenTelemetry Collector** using Helm. 
* How instrument an application with [**OpenTelemetry**](https://opentelemetry.io). 
* How to capture tags of interest from your application using an OpenTelemetry SDK. 
* How to index tags in **Splunk Observability Cloud** using **Troubleshooting MetricSets**.
* How to utilize tags in **Splunk Observability Cloud** to find “unknown unknowns” using the **Tag Spotlight** and **Dynamic Service Map** features.

Collecting tags aligned with the best practices shared in this workshop will let you get even more value from the data you’re sending to **Splunk Observability Cloud**.  Now that you’ve completed this workshop, you have the knowledge you need to start collecting tags from your own applications!

To get started with capturing tags today, check out [how to add tags in various supported languages](https://docs.splunk.com/observability/en/apm/span-tags/add-context-trace-span.html#instrument-your-application-code-to-add-tags-to-spans), and then [how to use them to create Troubleshooting MetricSets](https://docs.splunk.com/observability/en/apm/span-tags/index-span-tags.html#apm-index-span-tags) so they can be analyzed in Tag Spotlight. For more help, feel free to [ask a Splunk Expert](https://www.splunk.com/en_us/about-splunk/contact-us.html).

{{% notice title="Tip for Workshop Facilitator(s)" style="primary"  icon="lightbulb" %}}
Once the workshop is complete, remember to delete the APM MetricSet you created earlier for the `credit.score.category` tag.
{{% /notice %}}
