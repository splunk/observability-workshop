---
title: 1. APM Service Map
weight: 1
---

The APM Service Map shows the backend services involved in processing a request and the connections between them. It helps you understand how a business operation travels through the application and where delays or errors occur.

You arrived here by selecting the `checkout:oteldemo.CheckoutService/PlaceOrder` **Business Operation** from the RUM session. Splunk Observability Cloud automatically applied the relevant filters, so the map focuses on the services involved in that operation during the selected time range.

Each circle represents a service, and the lines show how requests travel between services. The color of a circle indicates the service’s status. A *red* circle identifies the service where errors originate, while a *red* connection shows the path taken by failed requests.

The panel on the right initially summarizes the selected business operation. When you select a service on the map, the panel updates to show metrics for that service, including requests, errors, latency, dependencies, traces, and endpoint performance. 

{{% exercise title="Inspect payment service" %}}

* Select the *red* **payment** service **(1)** in the Service Map.

* Confirm that **payment** appears at the top of the right-hand panel **(3)**.

Examine the **Service Requests & Errors** chart **(2)**. Compare the number of requests with the number of errors.

![APM Explore](../images/apm-business-workflow.png)

{{< tabs >}}
{{% tab title="Question" %}}
**What does the *Service Requests & Errors* chart tell you about the reliability of the payment service?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The *payment* service is experiencing a high error rate. In this example, approximately half of its requests result in errors. Your exact values may differ, but the chart should show that a significant proportion of payment requests are failing.**
{{% /tab %}}
{{< /tabs >}}

The Service Map has identified **payment** as the source of the *checkout* errors. Next, you’ll open its *Service-Centric View* to examine the service, its endpoints, and the infrastructure on which it runs.
In the right-hand panel, select the blue **payment** service name **(3)** to open its *Service-Centric View*.

{{% /exercise %}}
