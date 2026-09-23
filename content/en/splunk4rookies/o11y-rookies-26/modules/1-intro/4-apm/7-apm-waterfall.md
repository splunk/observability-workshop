---
title: 7. APM Waterfall
weight: 7
---

The **Trace Waterfall** displays every span in a trace as a hierarchical timeline. Each row represents one unit of work, such as a service request or API call. Its position shows when it occurred, and its duration shows how long it took.

The hierarchy shows how work moved between services. Error badges, such as *401*, highlight the spans associated with a failure. Selecting a span opens its details and tags in the right-hand pane.

{{< notice >}}
The **Trace View** may open with both the *analysis panel* and *Span properties* pane displayed, leaving less room for the waterfall. To create more space, select the panel toggle **(1)** to collapse the analysis panel, and select X **(2)** to close Span properties. You can reopen *Span properties* at any time by selecting a span in the waterfall.
![panes_open](../images/apm-waterfall-panes-open.png)
{{< /notice >}}

{{% exercise title="Inspect the Failing Payment Span" %}}

* In the waterfall, locate the checkout branch containing the `PaymentService/Charge` operation.

* Expand the branch if necessary & look for spans marked with a red error badge or HTTP status **401**.

* Select the failing 'payment: charge' span. The *Span* properties pane opens on the right.

* Review the span details and tags. Scroll through the pane if necessary to find the error information and service version.

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{< tabs >}}
{{% tab title="Question" %}}
**What is the error message and version being reported in the Span Details?**
{{% /tab %}}
{{% tab title="Answer" %}}
**`Invalid request` and `v350.10`**.
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

You have identified the failing span and affected service version. Next, use **Related Content** to open the associated logs and investigate the error further.