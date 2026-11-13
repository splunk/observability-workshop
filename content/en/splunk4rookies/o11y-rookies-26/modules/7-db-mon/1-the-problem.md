---
title: 1. The Problem
weight: 1
---

## “Why are recommendations taking so long?”

Customers can browse the Astronomy Shop, but product recommendations sometimes take several seconds to appear. The page eventually returns results, and the requests may show no errors. From the customer's perspective, though, the shop feels slow.

![Illustration of a shopper waiting for recommendations while an application request encounters a slow database](../images/slow-recommendations.png)

The recommendation service retrieves product information from PostgreSQL. Somewhere along that path, a request is doing more work than expected. A successful response tells us the request completed; it does not tell us whether the database handled it efficiently.

## Your investigation

You are the SRE on call. Your task is to move from **“recommendations are slow”** to an explanation the application and database teams can act on.

Start with three questions:

- **Where is the delay?** Use APM to locate the slow dependency behind the recommendation request.
- **What is the database doing?** Identify the expensive SQL query and examine how PostgreSQL executes it.
- **What should change?** Use the evidence and AI recommendations to propose a fix and explain how you would validate it.

By the end, you should be able to name the query, explain the work driving its latency, and hand the development team a concrete remediation proposal.

{{% notice title="Before you investigate" style="info" %}}
Sign in using the access details provided by your instructor. Use the assigned Astronomy Shop environment and PostgreSQL instance, starting with the **last 15 minutes** or the incident window your instructor specifies. Keep that environment and time window consistent as you move between APM and Database Monitoring.
{{% /notice %}}

Begin by following the recommendation request in the **APM service map**.
