---
title: Application Performance Monitoring Home page
linkTitle: 3.1 APM Home Page 
weight: 2
---
 
Click **APM** in the main menu, the APM Home Page is made up of 3 distinct sections:

![APM page](../images/apm-main.png)

1. **Onboarding Pane Pane:** Training videos and links to documentation to get you started with Splunk APM.
2. **APM Overview Pane:** Real-time metrics for the Top Services and Top Business Workflows.
3. **Functions Pane:** Links for deeper analysis of your services, tags, traces, database query performance and code profiling.

The **APM Overview** pan provides a high-level view of the health of your application. It includes a summary of the services, latency and errors in your application. It also includes a list of the top services by error rate and the top business workflows by error rate (a business workflow is the start-to-finish journey of the collection of traces associated with a given activity or transaction and enables monitoring of end-to-end KPIs and identifying root causes and bottlenecks).

{{% notice title=" About Environments" style="info" %}}

To easily differentiate between multiple applications, Splunk uses **environments**. The naming convention for workshop environments is **[NAME OF WORKSHOP]-workshop**. Your instructor will provide you with the correct one to select.

{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* Verify that the time window we are working with is set to the last 15 minutes (**-15m**).
* Change the environment to the workshop one by selecting its name from the drop-down box and make sure that is the only one selected.
{{< tabs >}}
{{% tab title="Question" %}}
**What can you conclude from the *Top Services by Error Rate* chart?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The *paymentservice* has a high error rate**
{{% /tab %}}
{{< /tabs >}}
<!--
* Click on the Explore Tile in the Function Pane. This will bring us to the automatically generated map of our services. This map shows how the services interact together based on the trace data being sent to Splunk Observability Cloud.
-->
{{% /notice %}}

If you scroll down the Overview Page you will notice some services listed have **Inferred Service** next to them.

Splunk APM can infer the presence of the remote service, or inferred service if the span calling the remote service has the necessary information. Examples of possible inferred services include databases, HTTP endpoints, and message queues. Inferred services are not instrumented, but they are displayed on the service map and the service list.

Next, let's check out **Splunk Log Observer (LO)**.
