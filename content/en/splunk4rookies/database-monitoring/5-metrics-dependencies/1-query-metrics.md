---
title: 1. Query Metrics Over Time
weight: 1
---

The **Query metrics** tab plots the per-query trends — execution count, average duration, CPU time, rows read — over the selected time range. The aggregated numbers on the **Queries** tab tell you what the query has been doing *in total*; the metrics tab tells you *how that has changed*.

This matters because two questions look identical until you see the trend:

- "This query has always been slow." → Likely a missing index or bad design from day one.
- "This query was fast last week and is slow now." → Likely a data growth issue, a stats problem, or a recent code change.

{{% notice title="Exercise" style="green" icon="running" %}}

* In the Navigator, click the **Query metrics** tab.
* Pick a longer time window in the time picker (e.g. **Last 24 hours**) so any trend is visible.
* Look at the **Average duration** chart for your candidate query.

<!-- TODO screenshot: Query metrics tab showing trend charts for execution count, average duration and CPU time over 24 hours -->
![Query Metrics](../images/query-metrics.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Is the query's average duration steady, trending up, or spiking at specific times?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Trending up usually means data growth or stale statistics. Spikes at specific times usually mean contention with a scheduled job — for example, a backup or an ETL run.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
