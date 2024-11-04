---
title: RUM trace Waterfall view & linking to APM 
linkTitle: 3. RUM Waterfall
weight: 3
---

We are now looking at the RUM Trace waterfall, this will tell you what happened during the session on the user device as they visited the page of our petclinic application.

If you scroll down the waterfall find click on the **#!/owners/details** segment on the right **(1)**, you see a list of action that occurred during the handling of the Vets request. Note, that the HTTP request have a blue **APM** link before the return code. Pick one, and click on the APM link.  This will show you the APM info for this Ser vice call to our Microservices in Kubernetes.

![rum apm link](../../images/rum-trace.png)

Note , that there give you the information what happened during action in the Microservices, and if you want to   drill down to verify what happened with the request, click on the Trace ID url.

This will show you the trace related to your request from RUM:

![RUm-apm linked](../../images/rum-apm-waterfall.png)

You can see that the entry point into your service now has a **RUM (1)** related content link added, allowing you to return back to your RUM session after you validated what happened in your Microservices.
