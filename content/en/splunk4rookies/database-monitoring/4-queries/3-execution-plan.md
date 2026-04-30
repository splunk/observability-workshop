---
title: 3. Execution Plans
weight: 3
---

The **execution plan** is the database optimiser's chosen strategy for running a query — which indexes to use, which join algorithm to apply, in what order, and so on. When a query is slow, the plan usually tells you why.

Splunk Database Monitoring captures the plan that was used for each query sample, so you can see what the engine actually did rather than guessing from the SQL.

{{% notice title="What to look for in a plan" style="info" %}}
The most common red flags are **table scans** (the engine reading the whole table because no usable index exists), **expensive sorts** that could be avoided with a better index, and **nested loop joins** over large row counts. You don't need to be a query-tuning expert to spot these — the plan visualisation calls them out.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* With your slow sample still selected, scroll down to the **Execution plan** section in the right-hand pane.
* Inspect the plan and note the dominant operation — is it an **Index Seek**, an **Index Scan**, or a **Table Scan**?

<!-- TODO screenshot: Execution plan view for a query sample, ideally showing a Table Scan or other expensive operation -->
![Execution Plan](../images/execution-plan.png)

{{< tabs >}}
{{% tab title="Question" %}}
**If the plan shows a Table Scan on a large table, what is the likely fix?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Add a covering index on the columns in the WHERE clause** — and confirm afterwards that the optimiser actually picks it up.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
