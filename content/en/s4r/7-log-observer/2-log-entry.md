---
title: 2. Viewing Log Entries
weight: 2
---

Before we look at a specific log line, let's quickly recap on what we have done so far and why we are here based on the the 3 pillars of Observability:

{{< mermaid >}}

---
title: The 3 Pillars of Observability

---

%%{
  init:{
    "theme": "neutral",
    "themeVariables": {
      "lineColor": "#ffffff"
    }
  }
}%%

graph LR;
    A["`_Metrics_
    **Do I have a problem?**`"]
    B["`_Traces_
    **Where is the problem?**`"]
    C["`_Logs_
    **What is the problem?**`"]
    A --> B --> C
{{< /mermaid >}}

* Using metrics we identified **we have a problem** with our application. This was obvious from the error rate in the Service Dashboards as it was higher than it should be.
* Using traces and span tags we found **where the problem is**. The **paymentservice** comprises of  two versions, `v350.9` and `v350.10`, and the error rate was **100%** for `v350.10`.
* We did see that this error from the paymentservice version **350.10** cause multiple retries and a long delay in the response back to the Online Boutiques. website for a checkout.
* From the at trace, using the power of Related Content, we have arrived at the log entries for the failing **paymentservice** version. Now, we can determine **what the problem is**.

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on an error entry in the log table (make sure it says *hostname":"paymentservice-* * (1)) as in case there is a rare error from a different service in the list too.
* Based on the Message,  what would you tell the developer to fix to resolve the issue?

![Log Message](../images/log-observer-log-message.png)

{{% /notice %}}

{{% notice style="blue" title="Congratulations" icon="wine-bottle" %}}

You have successfully used the Splunk Observability Suite to detect an issue you experienced when using the Online Boutique, search for where it happened in your service landscape and found the underlying cause for it, all based on the three signals of Observability, *Metrics, Traces & Logs*

You also learned how to use Splunk's **Intelligent tagging and analysis** with **Tag Spotlight** to detect patterns in your applications behaviour and  to use the  **Full stack correlation** power of *Related Content* to quickly move between the different components of the Suite while keeping in context of your issue.

{{% /notice %}}

In the next part of the workshop, we will focus on how to use dashboards & Splunk Synthetics to give you options to be alerted sooner in case of an issue like you experienced with the online boutique.

Next up, Log chart in dashboards.
