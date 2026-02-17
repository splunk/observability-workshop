---
title: 3. Viewing Log Entries
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

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

{{% /notice %}}

{{% notice style="blue" title="Congratulations" icon="wine-bottle" %}}

You have **successfully** used Splunk Observability Cloud to understand why you experienced a poor user experience whilst shopping at the Online Boutique. You used RUM, APM and logs to understand what happened in your service landscape and subsequently, found the underlying cause, all based on the 3 pillars of Observability, **metrics**, **traces** and **logs**.

You also learned how to use Splunk's **intelligent tagging and analysis** with **Tag Spotlight** to detect patterns in your applications' behavior and to use the **full stack correlation** power of **Related Content** to quickly move between the different components whilst keeping in context of the issue.

{{% /notice %}}

In the next part of the workshop, we will move from **problem-finding mode** into **mitigation**, **prevention** and **process improvement mode**.
