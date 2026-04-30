---
title: 2. Rank Instances by a Different Metric
weight: 2
---

Sorting by total duration finds the instances doing the most work. But sometimes you care about a different angle — for example, instances running an unusually high *number* of queries (which suggests a noisy application), or instances burning the most CPU (which suggests inefficient queries rather than just heavy load).

The chart at the top of the overview page lets you switch between three rankings:

- **Execution count** — how many queries ran.
- **Duration** — total time spent in queries.
- **CPU time** — total CPU consumed by queries.

{{% notice title="Exercise" style="green" icon="running" %}}

* In the top-5 trend chart, click the metric selector and switch from **Duration** to **Execution count**.
* Note which instances now appear in the top 5.
* Switch the selector to **CPU time** and note any new instances that appear.

<!-- TODO screenshot: top-5 chart with the metric selector dropdown open showing Execution count / Duration / CPU time options -->
![Rank instances by metric](../images/rank-by-metric.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Did the same instance stay at the top across all three rankings? What does it mean if it did — or didn't?**
{{% /tab %}}
{{% tab title="Answer" %}}
**If one instance dominates all three rankings, it is the obvious place to start.** If different instances lead each ranking, the problem may be split — e.g., one instance is busy (high execution count) while another is inefficient (high CPU per query).
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
