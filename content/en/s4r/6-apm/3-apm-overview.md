---
title: 3. APM Services Overview
weight: 3
---

You can use the APM Service Map to identify dependencies, performance bottlenecks, and error propagation. To get a complete overview of the application click on the {{% button %}}< Overview{{% /button %}} button on the top left of the service map.

![APM Explore](../images/apm-overview.png)

The Overview page provides a high-level view of the health of your application. It includes a summary of the services, latency and errors in your application. It also includes a list of the top services by error rate and the top business workflows by error rate (a business workflow is the start-to-finish journey of the collection of traces associated with a given activity or transaction and enables monitoring of end-to-end KPIs and identifying root causes and bottlenecks).

{{% notice title="Exercise" style="green" icon="running" %}}

* What can you conclude from the **Top Services by Error Rate** chart?

{{% /notice %}}

If you scroll down the Overview Page you will notice some services listed have **Inferred Service** next to them.

Splunk APM can infer the presence of the remote service, or inferred service if the span calling the remote service has the necessary information. Examples of possible inferred services include databases, HTTP endpoints, and message queues. Inferred services are not instrumented, but they are displayed on the service map and the service list.
