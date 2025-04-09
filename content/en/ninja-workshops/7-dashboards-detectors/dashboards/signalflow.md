---
title: Using SignalFlow
linkTitle: 1.6 Signalflow
weight: 1.6
---

## 1. Introduction to SignalFlow

Now let’s take a closer look at **SignalFlow**, the powerful analytics language behind Splunk Observability Cloud. SignalFlow enables you to define monitoring logic as code, offering a flexible and real-time way to work with metrics and automate alerting.

At the core of **Splunk Infrastructure Monitoring** is the **SignalFlow analytics engine**, which processes streaming metric data in real time. SignalFlow is written in a Python-like syntax and allows you to build computations that take in **metric time series (MTS)**, perform transformations or calculations, and output new MTS.

Some common use cases for SignalFlow include:

* Comparing current values with historical trends, such as week-over-week comparisons
* Creating population-level insights using distributed percentile charts
* Monitoring rates of change or thresholds, such as detecting when a Service Level Objective (SLO) is breached
* Identifying correlated dimensions, like pinpointing which service is linked to an increase in low disk space alerts

You can create SignalFlow based computations directly in the **Chart Builder** interface by selecting metrics and applying analytical functions visually. For more advanced use cases, you can also write and execute SignalFlow programs directly using the **SignalFlow API**.

SignalFlow includes a robust set of built-in functions that operate on time series data—making it ideal for dynamic, real-time monitoring across complex systems.

{{% notice title="Info" style="info" %}}
For more information on SignalFlow see [Analyze incoming data using SignalFlow](https://docs.splunk.com/Observability/infrastructure/analytics/signalflow.html).
{{% /notice %}}

## 2. View SignalFlow

In the chart builder, click on **View SignalFlow**.

![SignalFlow](../../images/view-signalflow.png)

You will see the SignalFlow code that composes the chart we were working on. You can now edit the SignalFlow directly within the UI. Our documentation has the [full list](https://dev.splunk.com/observability/docs/signalflow/function_method_list) of SignalFlow functions and methods.

Also, you can copy the SignalFlow and use it when interacting with the API or with Terraform to enable Monitoring as Code.

![Code](../../images/show-signalflow.png)

{{< tabs >}}
{{% tab title="SignalFlow" %}}

```python
A = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).publish(label='A', enable=False)
B = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).timeshift('1w').publish(label='B', enable=False)
C = (A-B).publish(label='C')
```

{{% /tab %}}
{{< /tabs >}}

Click on **View Builder** to go back to the Chart **Builder** UI.

![View Builder](../../images/view-builder.png)

Let's save this new chart to our Dashboard!
