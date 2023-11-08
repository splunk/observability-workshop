---
title: Checking Logs With Log Observer
linkTitle: 4. Log Observer Home Page
weight: 40
---
 
{{% button icon="clock" %}}5 minutes{{% /button %}}

We continue our tour of the Splunk Observability UI with Log Observer. Log Observer is a feature within Splunk Observability Cloud that allows you to seamlessly bring in log data from your Splunk Platform into an intuitive and codeless interface designed to help you find and fix problems quickly. You will be able to easily perform log-based analysis and seamlessly correlate your logs with Splunk Infrastructure Monitoring’s real-time metrics and Splunk APM traces in one place.

If you have not done so already, please select ![Log Observer](../../images/log-observer-icon.png?classes=inline&height=25px) from the Main menu. This will bring you to the Log Observer Home page.

This Page has 4 distinct sections that provide information or allow you to navigate the Log Observer UI and see log data from the selected Indexes.

![Lo Page](../images/lo-home.png?width=30vw)

1. **Onboarding Pane:** Here you will find videos and references to document pages of interest for Log Observer.
(Can be closed by the **X** on the right, if space is at a premium.)
2. **Filter Pane:** This pane allows you to filter on time, indexes (see below), fields and source type. This pane also allows you to save or reuse previously saved searches.
3. **Log's Table Pane:** This pane shows you the Log Data retrieved from the selected index as set in the Filter pane.
4. **Fields Pane:** Here you can find all the fields that have been used in the current Index selection including the active count of each field.

{{% notice title=" Splunk indexes" style="info" %}}
Generally, in Splunk, an "index" refers to a  designated place where your data is stored. It's like a folder or container for your data. Data within a Splunk index is organized and structured in a way that makes it easy to search and analyze. Different indexes can be created to store specific types of data. For example, you might have one index for web server logs, another for application logs, and so on.

Within the Splunk Observability cloud suite you can retrieve and search log data from "indexes" that have been preconfigured by the Administrators of your SObservability Org.
{{% /notice %}}

#### WIP WIP WIP  WIP

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

TBD

{{% /notice %}}

We will investigate Log observer in more detail later, so let's have a look at how Splunk Synthetics allows you to the next page.
