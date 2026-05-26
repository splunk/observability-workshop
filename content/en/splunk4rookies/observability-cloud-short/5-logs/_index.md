---
title: Logs
linkTitle: 5. Logs
weight: 5
archetype: chapter
time: 20 minutes
description: In this section, we will use Log Observer to drill down and identify what the problem is.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Remaining in your **back-end developer** role, you need to inspect the logs from your application to determine the root cause of the issue.

{{% /notice %}}

> [!IMPORTANT]
> Using the content related to the **APM** trace (logs) we will now use **Logs** to drill down further to understand exactly what the problem is. Related Content is a powerful feature that allows you to jump from one component to another and is available for **metrics**, **traces** and **logs**.

{{< webex chat="Robert Castley" date="Today • 28/01/2026" seenby="PH" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
I've checked APM and confirmed the issue is with the paymentservice. There's a signifcant latency spike in the traces
{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
I'll use Related Content to jump to the logs and see if I can find any errors or anomalies that could explain the latency spike.
{{< /webex-msg >}}
{{< /webex >}}
