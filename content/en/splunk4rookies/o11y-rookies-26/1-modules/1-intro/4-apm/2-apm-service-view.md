---
title: 2. APM Service View
weight: 2
---

The **Service View** brings together the health, performance, dependencies, and troubleshooting data for one backend service. You arrived here by selecting the payment service from the Service Map, so the page is already filtered to that service and your workshop environment.

**This needs completing**
The Overview tab provides a quick health summary. It includes the service’s success rate, service-level indicators, request and error activ

The overview confirms that the **payment** service has recurring *authentication* failures, but it does not yet show what the affected requests have in common. To look for a pattern, select the **Tag Spotlight** tab **(4)**.ity, latency, and a map of its immediate dependencies.

The navigation bar contains several additional ways to investigate the service:

* *Tag Spotligh*t — Compare performance and errors across tag values to identify patterns.
* Errors — Examine the errors reported by the service.
* *Endpoints* — Compare the operations provided by the service and identify slow or failing endpoints.
* *Instances* — Compare individual service instances to find unhealthy or unusual instances.
* *Logs* — View logs associated with the service and selected time range.
* *Traces* — Inspect distributed traces that passed through the service.
* *Application Security* — Investigate security findings associated with the application.
* *Code Profiling and Memory Profiling* — Analyze code execution and memory usage when profiling is configured.

You’ll use some of these views in other workshop lessons. In this introductory lesson, you’ll focus on the Overview and Tag Spotlight tabs.

{{< notice >}}
The tabs and available data depend on how your environment is configured. Some views may contain little or no data if the corresponding capability has not been enabled.
{{< /notice >}}

{{% exercise title="Identify the Payment Error" %}}
First, confirm that the dashboard is showing the correct data.
* In the filter bar highlighted in red **(1)**, verify the following:
     * **Time** is set to Last *1 hour (-1h)*.
    * **Environment** is set to your workshop environment.
    * **Service** is set to *payment*.    
The one-hour time range provides enough data to determine whether the problem is recurring rather than limited to one request.

Review the service health:
* Examine the **Success rate (2)**. A value below *100%* means that some requests were unsuccessful during the selected period.
* Review the **Service errors (3)** chart. Repeated spikes show that the errors occurred several times and were not limited to a single request.

![Service Dashboard](../images/apm-service-dashboard-top.png)

{{% /exercise %}}

The service overview confirms that **payment** service has a low success rate and recurring errors. On the next page, you’ll examine the *Error* breakdown to identify the type of failure.