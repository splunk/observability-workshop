---
title: Logs
linkTitle: 5. Logs
weight: 5
type: chapter
time: 20 minutes
description: Follow Related Content from an APM trace and use Logs to explain the payment failure.
aliases:
  - /splunk4rookies/o11y-rookies-26/modules/1-intro/5-logs/
---

{{< persona role="Back-end developer" >}}
{{< persona-situation >}}You are still investigating the Astronomy Shop issue, and the next evidence is in the logs.{{< /persona-situation >}}
{{< persona-goal >}}Explain why the payment request was rejected.{{< /persona-goal >}}
{{< /persona >}}

> [!IMPORTANT]
> Using the content related to the **APM** trace (logs), we will now use **Logs** to drill down further to understand exactly what the problem is. Related Content is a powerful feature that allows you to jump from one component to another and is available for **metrics**, **traces** and **logs**.

{{< webex chat="Robert Castley" date="Today • 02/01/2027" seenby="PH" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
I've checked APM and confirmed that version v350.10 of the payment service is returning 401 errors. The failing span reports “Invalid request.”

{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
I’ll use Related Content to open the logs for the trace and look for more detail about why the request was rejected.
{{< /webex-msg >}}
{{< /webex >}}
