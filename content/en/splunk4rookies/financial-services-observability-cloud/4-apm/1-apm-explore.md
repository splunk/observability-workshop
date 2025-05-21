---
title: 1. APM Explore
weight: 1
---

When you click into the APM section of Splunk Observability Cloud you are greated with an overview of your APM data including top services by error rates, and R.E.D. metrics for services and workflows.

The APM Service Map displays the dependencies and connections among your instrumented and inferred services in APM. The map is dynamically generated based on your selections in the time range, environment, workflow, service, and tag filters.

You can see the services involved in any of your APM user workflows by clicking into the **Service Map**. When you select a service in the **Service Map**, the charts in the **Business Workflow** sidepane are updated to show metrics for the selected service. The **Service Map** and any indicators are syncronized with the time picker and chart data displayed. 

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on the **wire-transfer-service** in the Service Map.

{{% /notice %}}

![APM Explore](../images/apm-business-workflow.png)

Splunk APM also provides built-in **Service Centric Views** to help you see problems occurring in real time and quickly determine whether the problem is associated with a service, a specific endpoint, or the underlying infrastructure. Let's have a closer look.

{{% notice title="Exercise" style="green" icon="running" %}}

* In the right hand pane, click on **wire-transfer-service** in blue.

{{% /notice %}}

![APM Service](../images/apm-service.png)
