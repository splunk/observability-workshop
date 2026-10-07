---
title: 1. APM Service Map
weight: 1
---

The APM Service Map displays the dependencies and connections among your instrumented and inferred services in APM. The map is dynamically generated based on your selections in the time range, environment, business transaction, service, and tag filters.

When we clicked on the APM link in the RUM waterfall, filters were automatically added to the service map view to show the services that were involved in that **Transaction** (`frontend:/cart/checkout`).

You can see the services involved in the workflow in the **Service Map**. In the side pane, charts for the selected transaction are displayed. When you select a service in the **Service Map**, the charts in the side pane are updated to show metrics for the selected service.

{{% exercise title="Inspect paymentservice on the map" %}}

* Click on the **paymentservice** in the Service Map to select it.

![APM Explore](../images/apm-business-workflow.webp)

{{< quiz question="With the paymentservice selected, what can you conclude from the Service Requests and Errors chart in the side pane?" >}}
{{< quiz-option correct=true >}}The error percentage is very high.{{< /quiz-option >}}
{{< quiz-option >}}The error percentage is near zero.{{< /quiz-option >}}
{{< quiz-option >}}The chart shows latency only, with no errors.{{< /quiz-option >}}
{{< quiz-feedback >}}
**The error percentage is very high.**
{{< /quiz-feedback >}}
{{< /quiz >}}

* Splunk APM also provides built-in **Service Centric Views** to help you see problems occurring in real time and quickly determine whether the problem is associated with a service, a specific endpoint, or the underlying infrastructure. Let's have a closer look.
* In the right-hand pane, click on **paymentservice** in blue **(2)**.

{{% /exercise %}}
