---
title: 1. What is Database Monitoring?
weight: 1
---

**Splunk Database Monitoring** provides detailed performance visibility across multiple database platforms in a single, unified interface. Instead of jumping between SQL Server Management Studio, Oracle Enterprise Manager, and `pg_stat_statements`, you investigate every monitored instance from the same screen.

It collects three things you care about as a DBA:

- **Query performance analytics** — wait time, CPU time, rows read vs. rows returned, and the execution plans the optimiser actually chose.
- **Server metrics** — health and performance of the underlying database server.
- **Application correlation** — which applications, hosts, and APM traces are responsible for the queries you are looking at.

The supported platforms are **Microsoft SQL Server**, **Oracle Database**, and **PostgreSQL**.

{{% notice title="Realm availability" style="info" %}}
Database Monitoring availability depends on your Splunk realm and is not enabled in every region. If you cannot see the Database Monitoring entry point in the next exercise, check with your instructor that your workshop org is in a supported realm.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

Take a moment to think about your own environment before we open the product.

{{< tabs >}}
{{% tab title="Question" %}}
**Which of your database platforms (SQL Server, Oracle, PostgreSQL) would benefit most from a unified performance view, and why?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Any platform where you currently rely on a separate, vendor-specific tool to see query-level performance.** The unified view pays off most when you are responsible for more than one engine.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
