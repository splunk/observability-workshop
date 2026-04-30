---
title: 1. Top Queries on the Instance
weight: 1
---

The **Queries** tab in the Navigator lists the SQL statements running on this instance, ranked so that the worst offenders rise to the top. For each query you see aggregated metrics over the selected time range — typically execution count, total duration, total CPU time, and rows-read vs. rows-returned.

The **rows read vs. rows returned** ratio is one of the most useful columns. A query that reads a million rows to return ten is almost always doing a full scan or hitting a missing index — and it is costing you both CPU and I/O even when it looks fast in isolation.

{{% notice title="Exercise" style="green" icon="running" %}}

* On the **Queries** tab, scan the list and note the query text shown in the first column.
* Sort by **Total duration** if it is not already the active sort.
* Look for any query where **Rows read** is much larger than **Rows returned** — those are your inefficiency suspects.

<!-- TODO screenshot: Queries tab showing a list of SQL statements ranked by total duration, with a row where rows-read >> rows-returned highlighted -->
![Top Queries](../images/top-queries.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Why is a query with a high rows-read-to-rows-returned ratio a red flag, even if its average duration is reasonable?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The query is doing far more work than the result requires.** Under load it will get slower, and it is consuming I/O that other queries on the same instance also need.
{{% /tab %}}
{{< /tabs >}}

* Click the **query text** for the worst offender to open it. The right-hand pane will populate with details and we will continue from there in the next page.

{{% /notice %}}
