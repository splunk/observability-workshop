---
title: 9. APM preview
weight: 9
---
{{% notice style="grey" title="Hover over the APM link" %}}
![APM link preview](../img/trace-preview.png?width=50vw)

{{% /notice %}}

{{% notice style="blue" title="Say" icon="user" %}}
This is where the end to end value of the Splunk Observability Cloud starts to show. We can hover over this APM link to reveal some quick, at a glance, info about what’s happening on the backend.

This performance summary is clearly showing two actionable things:

1. Time is being spent in the app (not db, network, or external); and
1. There are errors occurring in these back-end services, and I can see precisely which service is producing the “root cause” for this particular trace (in this case the payment service in dark red).

To dig further, I can explore two different paths, depending on the questions I want to ask.

Let’s explore both to understand why I might want to do one or the other.

{{% /notice %}}

{{% notice style="grey" title="Click on the Workflow Name “frontend:/cart/checkout” or open both links in new tabs" %}}
![Workflow link to APM](../img/preview-workflow.png?width=50vw)

{{% /notice %}}