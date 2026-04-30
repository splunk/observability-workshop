---
title: Query Metrics & Dependencies
linkTitle: 5. Query Metrics & Dependencies
weight: 5
archetype: chapter
time: 10 minutes
description: Use Query Metrics, Dependencies, and Metadata tabs to see how a query trends over time and which applications call it.
---

{{% notice icon="user" style="orange" title="Persona" %}}

You are the **DBA**, and you have a candidate query in mind. Before you ask the application team to change anything, you want to confirm that the query is genuinely getting slower over time — and you want to know exactly which applications and hosts are calling it.

> [!splunk] The **Query metrics**, **Dependencies**, and **Metadata** tabs answer those questions: how the query is trending, which client applications and hosts depend on it, and what the database engine knows about the instance itself.

{{% /notice %}}

<!-- TODO screenshot: Query metrics tab showing trend charts for execution count and duration -->
![Query Metrics](images/query-metrics-tab.png?width=750px)
