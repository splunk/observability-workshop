---
title: 2. Log Filtering
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

We need to focus on just the Error messages in the logs:

* Click on the **Group By** drop-down box and use the filter to find **Severity**.
* Once selected click the {{% button style="blue" %}}Apply{{% /button %}} button (notice that the chart legend changes to show debug, error and info).
  ![legend](../images/severity-logs.png)
* Selecting just the error logs can be done by either clicking on the word error (**1**) in the legend, followed by selecting **Add to filter**. Then click {{% button style="blue" %}}Run Search{{% /button %}}
* You could also add the service name, `sf_service=paymentservice`, to the filter if there are error lines for multiple services, but in our case, this is not necessary.
  ![Error Logs](../images/log-observer-errors.png)

{{% /notice %}}

Next, we will look at log entries in detail.
