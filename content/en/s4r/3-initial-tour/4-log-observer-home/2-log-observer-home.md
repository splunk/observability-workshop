---
title: Log Observer Home Page
linkTitle: 2. Log Observer Home Page
weight: 2
---
 
{{% button icon="clock" color="#ed0090" %}}2 minutes{{% /button %}}

Click **Log Observer** in the main menu, the Log Observer Home Page is made up of 4 distinct sections:

![Lo Page](../images/log-observer-main.png)

1. **Onboarding Pane:** Training videos and links to documentation to get you started with Splunk Log Observer.
2. **Filter Bar:** Filter on time, indexes, and fields and also Save Queries.
3. **Logs Table Pane:** List of log entries that match the current filter criteria.
4. **Fields Pane:** List of fields available in the currently selected index.

{{% notice title=" Splunk indexes" style="info" %}}

Generally, in Splunk, an "index" refers to a  designated place where your data is stored. It's like a folder or container for your data. Data within a Splunk index is organized and structured in a way that makes it easy to search and analyze. Different indexes can be created to store specific types of data. For example, you might have one index for web server logs, another for application logs, and so on.

{{% /notice %}}

Let's run a little search exercise.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Set the time frame to  **-15m**.
* Click on {{% button style="gray" %}}Add Filter{{% /button %}} in the filter bar then click on **Fields** in the dialog.
* Type in **cardType** and select it.
* Under **Top values** click on **visa**, then click on **=** to add it to the filter.

![logo search](../images/log-filter-bar.png?width=920px)

* Click on one of the log entries in the Logs table to validate the entry contains `cardType: "visa"`.

{{% /notice %}}

We will revisit Log Observer in more detail later. Next, let's check out Synthetics.
