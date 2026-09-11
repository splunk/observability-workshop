---
title: 3. Viewing Log Entries
weight: 3
---

{{% exercise title="Investigate the Error Message" %}}

You have narrowed the results to error logs from the selected trace. Now examine an individual record to find the explanation behind the **payment** failure.

* Select an error entry in the **Logs table** to open its details.
* Check the record’s **service** or **hostname** fields to confirm that it came from the **payment** service. Other services involved in the trace may also have reported errors.
* Read the complete message and examine the associated fields. Scroll through the details if necessary.

{{< tabs >}}
{{% tab title="Question" %}}
**What does the log message reveal about the *payment* failure, and what should the development team check to resolve it?**
{{% /tab %}}
{{% tab title="Answer" %}}
* **The message reports that *ButtercupPayments* rejected an *invalid API token***. 
* **The development team should check the payment-provider credentials configured for version `v350.10`, correct or replace the invalid token, and verify that payment requests succeed afterward or rollback to `v350.9`**.
{{% /tab %}}
{{< /tabs >}}

  ![Log Message](../images/log-observer-log-message.png)
* When you have finished examining the record, select **X** in the log details pane to close it.

{{% /exercise %}}

{{% notice style="blue" title="Congratulations" icon="wine-bottle" %}}

**Investigation complete**  
You have followed a slow checkout interaction in the Astronomy Shop from the browser to its underlying payment failure:
- **RUM** revealed the poor user experience.
- **APM** located the failing service and affected version.
- *Logs* identified the invalid API token reported by the payment provider.
Along the way, **Tag Spotlight** helped you identify patterns, while **Related Content** kept the investigation connected as you moved between traces and logs.

**Transition to the next section**  
Next, you’ll explore Synthetic Monitoring and how scheduled tests can help detect problems before customers report them.
{{% /notice %}}


