---
title: 2. Viewing Log Entries
weight: 2
---

Let's quickly recap on what we have done so far using the 3 pillars of Observability:

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

* Using metrics we identified **we have a problem** with our application. The error rate in the Service Dashboards was higher than it should be.
* Using traces and span tags we found **where the problem is**. The **paymentservice** comprises two versions, `v350.9` and `v350.10`, and the error rate was **100%** for `v350.10`.
* Using the power of Related Content we have arrived at the log entries for the failing **paymentservice** version. Now, we can determine **what the problem is**.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Click on an error entry in the log table.
* What is the error?

{{% /notice %}}

![Log Message](../images/log-observer-log-message.png)