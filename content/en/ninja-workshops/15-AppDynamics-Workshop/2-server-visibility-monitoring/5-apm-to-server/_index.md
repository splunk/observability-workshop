---
title: Correlate Between Server and APM 
time: 3 minutes
weight: 5
description: You will review how to correlate between server metrics and the applications running on the server
---

## Navigate between Server and Application Contexts

The Server Visibility Monitoring agent automatically associates itself with any Splunk AppDynamics APM agents running on the same host.

With Server Visibility enabled, you can access server performance metrics in the context of your applications. You can switch between server and application contexts in different ways. Follow these steps to navigate from the server main dashboard to one of the Nodes running on the server.

1. Click the **Dashboard** tab to return to the main Server Dashboard.
2. Click the **APM Correlation** link.

![Server to APM](images/server-apm-link.png)

2. Click the down arrow on one of the listed Tiers.
3. Click the Node of the Tier link. 

![Dashboard Example](images/server-tier-link.png)

You are now on the **Node Dashboard**. 

4. Click the **Server** tab to see the related host metrics

![Dashboard Example](images/server-node-server.png)

When you have the Server Visibility Monitoring agent installed, the host metrics are always available within the context of the related Node.

You can read more about navigating between Server and Application Contexts [here](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/navigating-between-server-and-application-contexts).