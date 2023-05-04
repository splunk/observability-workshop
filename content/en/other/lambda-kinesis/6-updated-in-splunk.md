---
title: Updated Lambdas in Splunk APM
linkTitle: 6. Updated Lambdas in Splunk
weight: 6
---

Navigate back to APM in [Splunk Observabilty Cloud](https://app.us1.signalfx.com/#/apm)

Go back to your Service Dependency map.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Notice the difference?
{{% /notice %}}

![6-updated-1-map](../images/6-updated-1-map.png)

You should be able to see the `consumer-lambda` now clearly connected to the `producer-lambda`.

Remember the value you copied from your producer logs? You can run `sls logs -f consumer` command again on your EC2 lab host to fetch one.

Take that value, and paste it into trace search:

![6-updated-2-trace-search](../images/6-updated-2-trace-search.png)

Click on Go and you should be able to find the logged Trace:

![6-updated-3-trace](../images/6-updated-3-trace.png)

Notice that the `Trace ID` is something that makes up the trace context that we propagated.

You can read up on the two common propagation standards:

1. W3C: [https://www.w3.org/TR/trace-context/#traceparent-header](https://www.w3.org/TR/trace-context/#traceparent-header)
2. B3: [https://github.com/openzipkin/b3-propagation#overall-process](https://github.com/openzipkin/b3-propagation#overall-process)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Which one are we using?
{{% /notice %}}

It should be self-explanatory from the Propagator we are creating in the Functions

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Bonus Question: What happens if we mix and match the W3C and B3 headers?
{{% /notice %}}

Expand the `consumer-lambda` span.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Can you find the attributes from your message?
{{% /notice %}}

![6-updated-4-attributes](../images/6-updated-4-attributes.png)
