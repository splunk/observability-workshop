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
2. **Filter Pane:** This pane allows you to filter on time, indexes, fields and source type. This pane also allows you to save or reuse previously saved searches.
3. **Log's Table Pane:** This pane shows you the Log Data, based on the Index and filter set on the Filter page.
4. **Fields Pane:** Here you can find all the fields that have been used in the current Index selection.

#### WIP WIP WIP  WIP

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

TBD

{{% notice title="Web Vitals infos" style="info" %}}
TBD
{{% /notice %}}

TBD
{{% /notice %}}

We will investigate RUM in more detail later, so let's have a look at how Splunk Log Observer works with Log data on the next page.

{{% notice title=" Splunk indexes" style="info" %}}
In Splunk, an "index" refers to a specific storage location where data is stored, organized, and made searchable. It is a fundamental component of the Splunk platform, which is widely used for collecting, indexing, and searching large volumes of machine-generated data, such as log files and events.

Here's a simple explanation of a Splunk index:

Storage Location: A Splunk index is a designated place where your data is stored. It's like a folder or container for your data.

Organization: Data within a Splunk index is organized and structured in a way that makes it easy to search and analyze.

Searchability: Splunk indexes are designed for fast and efficient searching, allowing users to quickly retrieve and analyze data based on search queries.

Data Types: Different indexes can be created to store specific types of data. For example, you might have one index for web server logs, another for application logs, and so on.

Retention and Configuration: You can configure various settings for each index, including how long data is retained, access controls, and data retention policies.

In summary, a Splunk index is a crucial component that enables the Splunk platform to efficiently store, manage, and retrieve large volumes of data, making it valuable for analyzing and gaining insights from diverse sources of machine-generated data.th
{{% /notice %}}
