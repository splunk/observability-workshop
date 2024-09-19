---
title: Viewing the Logs
linkTitle: 1. Viewing the Logs
weight: 2
---

In order to see logs click on the **Log Observer** ![Logo](../../images/logo-icon.png?classes=inline&height=25px) in the left-hand menu. Once in Log Observer please ensure **Index** on the filter bar is set to **splunk4rookies-workshop**.

Next, click **Add Filter** and search for the field `deployment.environment`, select your workshop instance and click `=` (to include). You will now see only the log messages from your PetClinic application.

Next search for the field  `service.name`, select the value `customers-service` and click `=` (to include). Now the log entries will be reduced to show the entries from your `customers-service` only.

![Log Observer](../../images/log-observer-trace-info.png)

Click on an entry with an injected trace_id **(1)**. A side pane will open where you can see the detailed information, including the relevant trace and span IDs **(2)**.
