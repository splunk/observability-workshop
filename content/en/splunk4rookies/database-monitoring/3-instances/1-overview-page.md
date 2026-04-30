---
title: 1. The Overview Page
weight: 1
---

The Database Monitoring **Overview** page is where every investigation begins. It shows two things at once:

- A **time-series chart** of the top 5 instances, ranked by your chosen metric.
- A **list** of every monitored instance below the chart, sorted by total query duration.

The key columns in the list are **Total duration** and **Total CPU time**. The gap between them is meaningful: when an instance has high duration but relatively low CPU time, the queries are spending their time *waiting* (on locks, on I/O, on the network) rather than doing useful work.

{{% notice title="Exercise" style="green" icon="running" %}}

* On the **Database Monitoring Overview** page, locate the time-series chart at the top of the page **(1)**.
* Below the chart, find the instance list **(2)**.
* Make sure the time picker in the top-right is set to a sensible window — **Last 1 hour** is a good default.

<!-- TODO screenshot: Database Monitoring overview page with the top-5 trend chart (1) and the instance list (2) annotated -->
![Database Monitoring Overview](../images/overview-page.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Looking at the instance list, which instance has the highest Total duration?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The top row of the list** — the table is sorted by Total duration in descending order by default, so the worst offender is always at the top.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
