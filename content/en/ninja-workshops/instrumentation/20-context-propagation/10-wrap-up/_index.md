---
title: Wrap-Up
weight: 10
time: 5 minutes
description: Key takeaways & cleanup instructions.

---

## Summary

## Workshop summary

In this workshop you traced a single checkout from Splunk RUM through an order → payment → fulfillment pipeline and restored correlation at three places where traces commonly go dark. 

First, at the edge NGINX gateway, explicit proxy_set_header rules forwarded the request but not W3C Trace Context - so you added proxy_set_header traceparent $http_traceparent (plus tracestate and baggage) to pass headers through the reverse proxy. 

Second, at the payment gateway, an instrumented Node.js proxy still broke the chain because its outbound HTTP call did not propagate context - a typical BFF/proxy bug you fixed in application code with propagation.inject() and by removing suppressTracing() on the upstream fetch. 

Third, across RabbitMQ, the broker does not carry trace context on its own; the async handoff failed because the producer did not inject W3C headers into AMQP message properties and the consumer did not extract them - so you wired inject-on-publish and extract-on-consume (the same contract OTel messaging instrumentation automates in other stacks). 

Together, these fixes reconnect browser/RUM spans, synchronous HTTP hops through proxies and app-layer gateways, and asynchronous fulfillment work into one trace you can follow end to end in Splunk APM.

{{% notice title="Note" style="info" %}}
Congratulations - you've restored full-stack observability across proxies and message buses!
{{% /notice %}}

---

## Clean up

Remove all local workshop resources (k3d cluster, Splunk collector, app workloads, local images):

```bash
make cleanup
```

---

