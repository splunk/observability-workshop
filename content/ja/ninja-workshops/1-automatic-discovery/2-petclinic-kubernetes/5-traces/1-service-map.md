---
title: APM Service Map
linkTitle: 1. APM Service Map
weight: 1
---

![apm map](../../images/zero-config-first-services-map.png)

The above map shows all the interactions between all the services. The map may still be in an interim state as it will take the PetClinic Microservice application a few minutes to start up and fully synchronize. Reducing the time filter to a custom time of **2 minutes** by entering **-2m** will help. You can click on the **Refresh** button **(1)** in the top right-hand corner of the screen. The initial startup-related errors indicated by red circles will eventually disappear.

Next, let's examine the metrics that are available for each service that is instrumented by visiting the request, error, and duration (RED) metrics Dashboard.

For this exercise, we are going to use a common scenario you would use if your service operation was showing high latency or errors.

Click on **customers-service** in the Dependency map, then make sure the `customers-service` is selected in the **Services** dropdown box **(1)**. Next, select `GET /owners` from the Operations dropdown **(2)** adjacent to the Service name.

This should give you the workflow with a filter on `GET /owners` as shown below:

![select a trace](../../images/select-workflow.png)
