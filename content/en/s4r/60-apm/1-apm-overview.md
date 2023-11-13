---
title: 1. APM Overview
weight: 1
---

The service map displays the dependencies and connections among your instrumented and inferred services in APM. The map is dynamically generated based on your selections in the time range, environment, workflow, service, and tag filters.

When we clicked on the APM link in the RUM waterfall, filters were automatically added to the service map view to show the services that were involved in that particular trace.

You can use the service map to identify dependencies, performance bottlenecks, and error propagation. To get a complete overview of the application click on **Overview** button on the top left of the service map.

![APM Explore](../images/apm-overview.png)

The Overview page provides a high-level view of the health of your application. It includes a summary of the services, latency and errors in your application. It also includes a list of the top services by error rate and the top business workflows by error rate (a business workflow is the start-to-finish journey of the collection of traces associated with a given activity or transaction and enables monitoring of end-to-end KPIs and identifying root causes and bottlenecks).

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* What can you conclude from the **Top Services by Error Rate** chart?

{{% /notice %}}

If you scroll down the Overview Page you will notice some services listed have **Inferred Service** next to them.

Splunk APM can infer the presence of the remote service, or inferred service if the span calling the remote service has the necessary information. Examples of possible inferred services include databases, HTTP endpoints, and message queues. Inferred services are not instrumented, but they are displayed on the service map and the service list.
