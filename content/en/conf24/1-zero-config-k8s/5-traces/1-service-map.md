---
title: APM Service Map
linkTitle: 1. APM Service Map
weight: 1
---

For this exercise we are going to use a common scenario you would use if the service operation was showing high latency, or errors for example.

## I THINK WE SHOULD HAVE SOMETHING GENERATING ERRORS TO SHOW THE BENEFIT OF THIS SECTION

Select the **Customer Service** in the Dependency map **(1)**, then make sure the `customers-service` is selected in the **Services** dropdown box **(2)**. Next, select `GET /Owners` from the Operations dropdown **(3**)**.

![select a trace](../../images/select-workflow.png)

This should give you the workflow with a filter on `GET /owners` **(1)** as shown below. To pick a trace, select a line in the `Service Requests & Errors` chart **(2)**, when the dot appears click to get a list of sample traces:

![workflow-trace-pick](../../images/selecting-a-trace.png)

Once you have the list of sample traces, click on the blue **(3)** Trace ID Link. (Make sure it has the same three services mentioned in the Service Column.)

This brings us the the Trace selected in the Waterfall view:

![waterfall](../../images/waterfall-view.png)

Here we find several sections:  

* The actual Waterfall Pane **(1)**, where you see the trace and all the instrumented functions visible as spans, with their duration representation and order/relationship showing.
* The Trace Info Pane  **(2),  by default, shows the selected Span information. (Highlighted with a box around the Span in the Waterfall Pane.)
* The Span Pane **(3)**,   here you can find all the Tags that have been sent in the selected Span, You can scroll down to see all of them.
* The process Pane, with tags related to the process that created the Span (Scroll down to see as it is not in the screenshot.)
* The Trace Properties at the top of the right-hand pane by default is collapsed as shown.
