---
title: 3. Filtering and Grouping
weight: 3
---

With Log Observer open and your environment filter set, you're looking at all logs from all services. That's a lot of noise. Let's narrow it down.

{{% notice title="Exercise" style="green" icon="running" %}}

**Step 1: Group by Severity**

* Click on the **Group By** drop-down box **(1)**.
* Use the search to find and select `severity`.
* Click the {{% button style="blue" %}}Apply{{% /button %}} button.

Notice that the timeline chart legend now shows the distribution of log levels — **debug**, **info**, **warn**, and **error**.

<!-- TODO screenshot: Timeline chart grouped by severity showing legend -->

**Step 2: Filter to Errors Only**

* In the timeline chart legend, click on the word **error** **(2)**.
* Select **Add to filter**.
* Click {{% button style="blue" %}}Run Search{{% /button %}} at the top of the page.

You are now viewing only error-level logs from your environment.

<!-- TODO screenshot: Log Observer filtered to errors only -->

**Step 3: Identify the Noisy Service**

* Look at the log entries in the table below. Scan the `service.name` column.

{{< tabs >}}
{{% tab title="Question" %}}
**Which service is generating the most error logs?**
{{% /tab %}}
{{% tab title="Answer" %}}
<!-- TODO: Update with actual service name from OTel Demo v2.0.1 -->
Look for the service name that appears most frequently in the error log entries. This is your primary suspect.
{{% /tab %}}
{{< /tabs >}}

**Step 4: Filter by Service**

* Click on the service name in one of the log entries.
* Select **Add to filter**.
* Click {{% button style="blue" %}}Run Search{{% /button %}}.

You are now looking at error logs from a single service. The noise is gone.

<!-- TODO screenshot: Log Observer filtered to errors from a single service -->

{{% /notice %}}

{{% notice title="Info" style="info" %}}
In just four clicks, you went from thousands of log lines across all services to a focused view of errors from a single suspect service. This is the power of Log Observer's no-code filtering — fast triage without writing queries.
{{% /notice %}}
