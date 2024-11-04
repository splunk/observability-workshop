---
tßitle: Viewing the Logs
linkTitle: 1. Viewing the Logs
weight: 2
---

In order to see logs click on the ![Logo](../../images/logo-icon.png?classes=inline&height=25px)  **Log Observer** in the left-hand menu. Once in Log Observer please ensure **Index** on the filter bar is set to **splunk4rookies-workshop**. **(1)**

Next, click **Add Filter** and search, using the *Fields* **(2)** option for the field `deployment.environment` **(3)**.   Then from the dropdown list, select your workshop instance, **(4)** and click `=` (to include). You will now see only the log messages from your PetClinic application.

![Log Observer sort](../../images/log-observer-sort.png)

Next search for the field  `service.name`, select the value `customers-service` and click `=` (to include). This should now appear in the filter bar **(1)**. Next click on the Button **Run Search** **(2)**.

![Log Observer run](../../images/log-observer-run.png)

This wil refresh the log entries and they will now be reduced to show the entries from your `customers-service` only.

![Log Observer](../../images/log-observer-trace-info.png)

Click on an entry that starts with *"Saving pet"* **(1)**. A side pane will open where you can see the detailed information, including the relevant trace and span IDs **(2)**.
