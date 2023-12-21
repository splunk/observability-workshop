---
title: 2.1 Service Map
linkTitle: 2.1 Service Map
weight: 2
---

## Service Map

Click on **paymentservice** in the service map and select **version** from the `breakdown` drop down filter underneath **paymentservice**. This will filter our service map by the custom span tag **version**.

You will now see the service map has been updated like the below screenshot to show the different versions of the **paymentservice**. 

Splunk Observability shows that not only is paymentservice experiencing errors (you can see request rate vs error rate) but that this service is the root cause.

This happens automatically with our AI-directed triage capabilities once distributed tracing is enabled in your services. You don’t have to set a threshold or anything for it to populate just like this.

This is one example of how customers can detect issues faster and know where to look for errors and hence helps reduce the MTTD and MTTR.


![Payment Service](../../images/paymentservice.png)
