---
title: Splunk APM
weight: 9
---
{{% notice style="grey" title="Hover over the APM link" %}}
![APM link preview](../images/trace-preview.png)

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
![Workflow link to APM](../images/preview-workflow.png)

{{% /notice %}}

{{% notice style="grey" title="Viewing the service map" %}}
![APM service map with largest errors shown on paymentservice bubble](../images/map.png)

{{% /notice %}}

{{% notice style="blue" title="Say" icon="user" %}}
The service map confirms what we saw earlier, that the issues at this particular time are coming from the paymentservice. We can also see that it is relying on a external service.

We can use a capability called “Tag Spotlight” to understand if there is anything notable about these erroneous transactions.

{{% /notice %}}

{{% notice style="grey" title="Click on the paymentservice circle, and then click on “Tag Spotlight” on the right" %}}
![Service map with paymentservice selected and Tag Spotlight link](../images/paymentservice.png)

{{% /notice %}}

{{% notice style="blue" title="Say" icon="user" %}}
Tag Spotlight is a powerful capability in Splunk Observability Cloud that helps us make sense of the unique transactions flowing through our application.

Tags can be indexed, both on the service where they originate, as well as globally (covering the entire transaction), to help developers understand more about a subset of the transactions that are occurring.

{{% /notice %}}

{{% notice style="grey" title="Point out the tenant level and version" %}}
![Tenant level and version tags showing relevant requests and errors](../images/tags.png)

{{% /notice %}}

{{% notice style="blue" title="Say" icon="user" %}}
At a glance we can see that the different kinds of customers (gold, bronze, and silver) are all similarly impacted, but the new version of our code (v350.10) has 100% of the errors.

In many investigations we might filter on some of these tags to narrow our view, but we have a pretty good picture already of what’s going on.

{{% /notice %}}

{{% notice style="grey" title="Click on one of the higher peaks, on the errors line, to get exemplars with errors" %}}
![Example traces with relevant errors](../images/examples.png)

{{% /notice %}}

{{% notice style="blue" title="Say" icon="user" %}}
Now I can look at some of the specific traces that have errors, to understand precisely what happened.

{{% /notice %}}

{{% notice style="grey" title="Click on a trace that has root (solid red) errors on the paymentservice" %}}
![Trace detail showing multiple paymentservice requests with errors](../images/trace.png)

{{% /notice %}}

{{% notice style="blue" title="Say" icon="user" %}}
Now I’m starting to get a good picture of what’s going on. This checkout process is making an API call to an external service over and over again and failing.

I’d like to look at the logs to see precisely what the error is.

{{% /notice %}}
