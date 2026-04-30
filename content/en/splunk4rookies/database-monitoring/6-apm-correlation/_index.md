---
title: Correlate with APM Traces
linkTitle: 6. Correlate with APM Traces
weight: 6
archetype: chapter
time: 5 minutes
description: Jump from a slow database query to the .NET or Java application traces that called it via Splunk APM.
---

{{% notice icon="user" style="orange" title="Persona" %}}

You are the **DBA**, but the slow query is being driven by an application — and the developers will need a trace to start fixing the call site. You want to hand them a direct link.

> [!splunk] When the application is instrumented with Splunk APM, Database Monitoring can **correlate database queries with .NET and Java traces**. From a query in Database Monitoring you can pivot directly to the APM traces that executed it — so the application team gets the full back-end context, not just a SQL statement.

{{% /notice %}}

<!-- TODO screenshot: Database Monitoring query view with a "View in APM" / Related Content link visible to a Splunk APM trace -->
![Database to APM correlation](images/db-to-apm.png?width=750px)
