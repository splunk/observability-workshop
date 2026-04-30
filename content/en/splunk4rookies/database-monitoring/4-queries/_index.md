---
title: Queries & Query Samples
linkTitle: 4. Queries & Query Samples
weight: 4
archetype: chapter
time: 15 minutes
description: Identify the slowest queries running on an instance and inspect individual query samples and execution plans.
---

{{% notice icon="user" style="orange" title="Persona" %}}

You are the **DBA**, and you have picked the instance that is consuming the most database time. Now you need to know *which queries* are responsible — and for the worst offender, *what an individual execution actually looked like*.

> [!splunk] The **Queries** tab shows the top SQL statements ordered by wait time, CPU time, or rows read. The **Query samples** tab shows real captured executions of those queries, including parameters, duration, and the **execution plan** the database optimiser chose. Together they let you go from "the database is slow" to "this specific query, with these parameters, is doing a full table scan".

{{% /notice %}}

<!-- TODO screenshot: Queries tab with a list of top SQL statements ranked by duration -->
![Top Queries](images/queries-tab.png?width=750px)
