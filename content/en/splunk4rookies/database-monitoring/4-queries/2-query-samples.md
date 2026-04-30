---
title: 2. Query Samples
weight: 2
---

A **query sample** is a real captured execution of a query, complete with the actual parameter values and timing. Aggregated query metrics tell you "this query is slow on average". Query samples tell you "this *specific* execution, with these parameters, took 4.2 seconds".

Samples are how you reproduce a slow query in your own SQL client. They are also how you tell whether a query is uniformly slow or whether one set of parameters is dragging the average up.

{{% notice title="Exercise" style="green" icon="running" %}}

* With your candidate query selected, click the **Query samples** tab.
* You will see a list of individual captured executions of this query, each with its own duration and parameter values.
* Click on the **slowest** sample in the list **(1)**.

<!-- TODO screenshot: Query samples tab showing a list of captured executions, with the slowest sample highlighted (1) -->
![Query Samples](../images/query-samples.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Looking at the parameter values for the slowest sample versus a faster one, do they differ in any meaningful way?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Often the slow samples share a particular parameter value** — for example, a customer ID that owns far more rows than average. That is your first concrete clue about *why* the query is slow.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
