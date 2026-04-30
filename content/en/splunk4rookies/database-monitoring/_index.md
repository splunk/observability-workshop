---
title: Database Monitoring
weight: 4
authors: ["Robert Castley"]
time: 60 minutes
description: Get hands-on with Splunk Database Monitoring to investigate slow queries, view execution plans, and correlate database performance with the applications that depend on them.
params:
  images:
    - images/featured-dbm.png
hidden: true
---

## Introduction

Databases sit at the heart of almost every application — and when they slow down, everything slows down with them. **Splunk Database Monitoring** gives you a unified view across Microsoft SQL Server, Oracle Database, and PostgreSQL so you can pinpoint the queries, instances, and applications that are causing problems.

In this hands-on session, you'll act as a database administrator (DBA) responding to a performance complaint. You'll work through the same screens you'd use in production: ranking instances, drilling into the slowest queries, inspecting query samples and execution plans, and connecting the dots back to the applications calling those queries.

## Workshop Overview

In this 1-hour hands-on session, you'll cover:

- **Database Monitoring Overview** - Learn what Database Monitoring is, which platforms are supported, and where to find it in Splunk Observability Cloud
- **Database Instances** - Use the overview dashboard to rank instances by execution count, duration, and CPU time
- **Queries & Query Samples** - Identify the slowest queries on an instance and inspect query samples and execution plans
- **Query Metrics & Dependencies** - Examine per-query performance metrics and see which applications depend on each query
- **Correlate with APM Traces** - Jump from a slow database query to the .NET or Java application traces that triggered it

<!-- TODO screenshot: featured/hero image for the workshop, e.g., a Database Monitoring overview dashboard showing instance ranking and query duration trends -->
![Database Monitoring](images/featured-dbm.png)

**Let's dig into the database!**
