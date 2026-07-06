---
title: 3. Viewing Log Entries
weight: 3
---

{{% exercise title="Open an error log" %}}

* Click on an error entry in the log table (make sure it says `hostname: "paymentservice-xxxx"` in case there is a rare error from a different service in the list too).
{{< tabs >}}
{{% tab title="Question" %}}
**Based on the message, what would you tell the development team to do to resolve the issue?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The development team needs to rebuild and deploy the container with a valid API Token or rollback to `v350.9`**.
{{% /tab %}}
{{< /tabs >}}

  ![Log Message](../images/log-observer-log-message.png)
* Click on the **X** in the log message pane to close it.

{{% /exercise %}}

{{% notice style="blue" title="Congratulations" icon="wine-bottle" %}}

You have **successfully** used Splunk Observability Cloud to understand why you experienced a poor user experience whilst shopping at the Astronomy Shop. You used RUM, APM and logs to understand what happened in your service landscape and subsequently, found the underlying cause, all based on the 3 pillars of Observability, **metrics**, **traces** and **logs**.

You also learned how to use Splunk's **intelligent tagging and analysis** with **Tag Spotlight** to detect patterns in your applications' behavior and to use the **full stack correlation** power of **Related Content** to quickly move between the different components whilst keeping in context of the issue.

{{% /notice %}}

In the next part of the workshop, we'll move from reactive troubleshooting into **proactive monitoring** with **Synthetics** — catching this failure before a customer does — and then hand the whole investigation to **AI** to see how much faster it can be.
