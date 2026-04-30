---
title: Database Instances
linkTitle: 3. Database Instances
weight: 3
archetype: chapter
time: 15 minutes
description: Use the Database Monitoring overview dashboard to rank instances and pick the one that is hurting most.
---

{{% notice icon="user" style="orange" title="Persona" %}}

You are still the **DBA** triaging the slow-database complaint. You manage many database instances across SQL Server, Oracle, and PostgreSQL — you need to find the one (or two) instances that are most likely to be the source of the problem before you go any deeper.

> [!splunk] The **Database Monitoring Overview** page ranks every monitored database instance by *execution count*, *total duration*, or *total CPU time*. We will use it to spot the busiest and slowest instances, then drop into a **Navigator** view to start the real investigation.

{{% /notice %}}

<!-- TODO screenshot: Database Monitoring overview page with multiple instances listed -->
![Database Instances](images/db-instances-overview.png?width=750px)
