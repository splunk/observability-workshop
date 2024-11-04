---
title: APM Service Map
linkTitle: 1. APM Service Map
weight: 1
---

![apm map](../../images/zero-config-first-services-map.png)

The above map shows all the interactions between all of the services. The map may still be in an interim state as it will take the Petclinic Microservice application a few minutes to start up and fully synchronize. Reducing the time filter to a custom time of **2 minutes** will help. You can click on the **Refresh** button **(1)** on the top right of the screen. The initial startup-related errors (red dots) will eventually disappear.

Next, let's examine the metrics that are available for each service that is instrumented and visit the request, error, and duration (RED) metrics Dashboard

For this exercise we are going to use a common scenario you would use if the service operation was showing high latency, or errors for example.

Select (click) on the **Customer Service** in the Dependency map **(1)**, then make sure the `customers-service` is selected in the **Services** dropdown box **(2)**. Next, select `GET /Owners` from the Operations dropdown **(3**)**.

This should give you the workflow with a filter on `GET /owners` **(1)** as shown below.

![select a trace](../../images/select-workflow.png)
