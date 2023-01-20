---
title: Custom Attribution
linkTitle: Custom Attribution
weight: 5
---

To take a deeper look at this issue, we will implement Custom Attributes via Opentelemetry Manual Instrumentation

To speed up manual instrumentation in Java you can leverage [OpenTelemetry Annotations](https://opentelemetry.io/docs/instrumentation/java/automatic/annotations/), which automatically create a span around a method without modifying the actual code inside the method.

This can be very valueable if you are working with an SRE that may have limited accesss to source code changes.

To add even more information to help our developers find the root cause faster, [OpenTelemetry Annotations](https://opentelemetry.io/docs/instrumentation/java/automatic/annotations/) can be used to generate span tags with parameter values for the method in question.

It is important to remember that any developer should be able to debug a method with knowledge of parameter values at the time of an issue ( exception or latency).

To expedite manual instrumentation implementation for this exercise, we have provided a tool which will annotate the entirety of the "shop" and "products" services with OpenTelemetry standard annotations for every method call without having to write any code. This "annotator" tool will also tag every parameter in every function, which adds a span tag with Parameter=Value.

{{% alert title="Note:" color="info" %}}

This Full-fidelity Every-method approach is the Monolith Use Case with Splunk APM for Java.

{{% /alert %}}

## 1. Run Manual Instrumentation Tool

``` bash
cd javashop-otel directory
./AutomateManualInstrumentation.sh
```

## 2. Rebuild and Deploy Application

``` bash
./BuildAndDeploy.sh
```

Now that we have rebuilt and deployed our application, traffic is being sent once again.

Go back to the Splunk Observability UI and let's see if these annotations help us narrow down the root cause more quickly.

Click back on the trace window

![Screen Shot 2022-11-28 at 7 29 43 AM](https://user-images.githubusercontent.com/32849847/204348366-38b8c82a-02ca-472b-b1aa-feeb746ec1d7.png)

Give the traces a couple minutes to generate ...

## 3. Houston, we have a new problem

Once traces populate, Select "Errors Only"

![Screen Shot 2022-11-28 at 7 36 50 AM](https://user-images.githubusercontent.com/32849847/204348492-84a4ad45-e11c-4e75-a6a9-d6e52e0eb13e.png)

Note: we haven't changed the code at all by adding annotations. Click on a trace with an error present.

![Screen Shot 2022-11-28 at 7 38 33 AM](https://user-images.githubusercontent.com/32849847/204348687-12241153-b297-4bd7-9ea8-4b410369e82c.png)

We can see our Exception is `InvalidLocaleException`!

The real problem must be related to the new data associated with SRI LANKA as the Exception says "Non English Characters found in Instrument Data.

This exception had not surfaced in previous traces because the method where it was thrown was NOT covered with Auto Instrumentation.

Once we completed the Manual Instrumentation via the Annotations we added, this method was instrumented  and we can now see we had a buried Exception being thrown.
