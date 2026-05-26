---
title: 2. Navigate to Log Observer
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

* From the main navigation menu in Splunk Observability Cloud, click on **Log Observer**.
* Set the time range to **Last 15 minutes** using the time picker in the top-right corner.
* In the filter bar, add a filter for your workshop environment:
  * Click {{% button style="blue" %}}Add Filter{{% /button %}}
  * Select `deployment.environment`
  * Set the value to the environment name provided by your instructor

<!-- TODO screenshot: Log Observer landing page with time range and environment filter set -->

{{% /notice %}}

You should now see the Log Observer landing page with two main areas:

- **Timeline chart** (top) — A bar chart showing log volume over time, giving you an at-a-glance view of log activity
- **Log table** (bottom) — Individual log entries with timestamps, severity, service names, and messages

{{% notice title="Info" style="info" %}}
Log Observer works with **no-code** filtering — you never need to write SPL or query syntax. Everything is point-and-click, making it accessible to any team member regardless of their Splunk experience.
{{% /notice %}}
