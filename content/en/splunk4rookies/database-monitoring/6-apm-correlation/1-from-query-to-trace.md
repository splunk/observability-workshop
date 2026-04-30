---
title: 1. From a Slow Query to an APM Trace
weight: 1
---

When the application calling your slow query is instrumented with **Splunk APM** (.NET or Java), Database Monitoring exposes a **Related Content** link that takes you straight to the APM traces that executed the query. You don't have to copy a query ID into another tool or guess the right trace search.

This is the moment that closes the loop: you started with "the database feels slow", you ended with a specific application trace your developers can open and fix.

{{% notice title=".NET and Java" style="info" %}}
Query-to-trace correlation requires that the calling application is instrumented with the Splunk distribution of OpenTelemetry for **.NET** or **Java**, and that database query correlation is enabled. If you don't see the Related Content link, the application is either not instrumented or the correlation feature has not been turned on for it.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* Return to the **Queries** tab in the Navigator and select your candidate query again.
* In the right-hand details pane, look for the **Related Content** section at the bottom of the page.
* Click the **APM** link to jump to a list of traces that executed this query **(1)**.
* Pick a trace and click into the **Trace Waterfall** to see the full back-end call chain that led to the query.

<!-- TODO screenshot: Database Monitoring query view with the Related Content → APM link annotated (1), and a follow-up screenshot of the resulting Trace Waterfall view -->
![Database to APM correlation](../images/db-to-apm-link.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Looking at the trace waterfall, can you see which application service issued the query, and what other work the request did before reaching the database?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Yes — the waterfall shows every span in the request, with the database call appearing as a leaf span.** That gives the application team the full context they need to fix the call site.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
