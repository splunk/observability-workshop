---
title: Finding issues in the database
weight: 7
layout: chapter
time: 45 minutes
description: Follow a slow recommendation request into PostgreSQL, investigate its execution plan, and identify the root cause of a query regression with Database Monitoring.
draft: true
params:
  images:
    - images/slow-recommendations.png
---

<!-- Adapted from the Splunk DB-Mon demo. -->

{{< persona role="SRE on-call" >}}
{{< persona-situation >}}Customers report that product recommendations in the Astronomy Shop sometimes load slowly. The application still returns results, but a database call is taking seconds.{{< /persona-situation >}}
{{< persona-goal >}}Identify the expensive query, explain why it is slow, and give the development team an evidence-backed remediation plan.{{< /persona-goal >}}
{{< /persona >}}

**Database Monitoring** in Splunk Observability Cloud helps you investigate what happens inside a database after an application makes a call. In this module, you will follow a slow recommendation request from APM into PostgreSQL and uncover a query regression.

## Overview

In this hands-on module, you will:

- Locate the slow database dependency in the **APM service map**.
- Find the expensive query in **Database Monitoring**.
- Read its **normalized SQL** and **execution plan**.
- Evaluate **AI query summaries and recommendations** against the evidence.
- Explain the root cause and propose a way to validate the fix.

Allow approximately **45 minutes**. You do not need to be a database administrator or write SQL to complete the investigation.

{{% notice title="Workshop environment" style="info" %}}
Your instructor will provide an Astronomy Shop environment with PostgreSQL monitoring and the recommendation query scenario enabled. Screenshots show an example environment; names, timings, row counts, and AI responses may differ in your session. This exercise uses manual navigation between APM and Database Monitoring and does not depend on direct trace correlation.
{{% /notice %}}

{{< pager prev="/en/splunk4rookies/o11y-rookies-26/modules/" prevLabel="Back to Lessons" >}}

{{< presenter >}}
## Facilitator prerequisites

Before the session, verify that:

- The deployed Astronomy Shop version supports the Cartesian recommendation query scenario, with PostgreSQL telemetry and execution plans available in Database Monitoring.
- **Database Monitoring** with AI assistance is available.
- The **Summarize** button and **AI recommendations** tab work for participant access.

Confirm that **`recommendationCartesianQuery`** is **ON** and recent traffic includes the slow recommendation query. Feature flags can be checked at the Astronomy Shop frontend's `/feature` path; ask the environment owner to check shared environments.

Test **Summarize** and **Generate recommendations** before the session. An AI recommendations issue has been reported for this workshop; if generation fails, use the supplied example screenshots and clearly identify them as example evidence.

| Symptom | Facilitator check |
| --- | --- |
| Database Monitoring is absent | Confirm feature availability and participant access in the selected organization. |
| PostgreSQL instance is missing | Confirm database collection, environment filter, and time window. |
| Slow recommendation query is missing | Confirm the deployed scenario, `recommendationCartesianQuery` flag, and recent demo traffic; allow new telemetry to arrive. |
| Query is visible but no plan is available | Confirm execution-plan collection and a recent captured execution. |
| AI controls are unavailable | Confirm AI availability; participants can still interpret the supplied example screenshots and SQL, clearly distinguishing those from live evidence. |

{{< /presenter >}}
