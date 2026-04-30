---
title: 2. Dependencies
weight: 2
---

The **Dependencies** tab answers a question that classic database tools cannot: *which applications and hosts are actually calling this database?* Database Monitoring correlates the connections it sees with the application telemetry already in Splunk Observability Cloud, so you get a list of clients rather than a list of anonymous connection strings.

This is what turns a database investigation into an *engineering* investigation: instead of paging the on-call DBA, you can route the issue straight to the team that owns the noisy caller.

{{% notice title="Exercise" style="green" icon="running" %}}

* Click the **Dependencies** tab in the Navigator.
* Review the list of applications and hosts that have connected to this instance over the selected time range.
* Identify the application responsible for the largest share of query volume.

<!-- TODO screenshot: Dependencies tab showing a list of client applications and hosts ranked by query volume -->
![Dependencies](../images/dependencies.png)

{{< tabs >}}
{{% tab title="Question" %}}
**You have a candidate query and you know which application is calling it. Who do you talk to next?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The team that owns the calling application** — and you can hand them not just a query but, in the next chapter, a direct link to a trace.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
