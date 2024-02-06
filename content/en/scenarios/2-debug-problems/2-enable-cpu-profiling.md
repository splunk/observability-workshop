---
title: Enable CPU Profiling
linkTitle: 5.2 Enable CPU Profiling
weight: 2
---

Let's learn how to enable the CPU profiler, verify its operation,
and use the results in Splunk Observability Cloud to find out why our application sometimes runs slowly. 

### Update the application configuration

We will need to pass an additional configuration argument to the Splunk OpenTelemetry Java agent in order to
enable the profiler. The configuration is [documented here](https://docs.splunk.com/observability/en/gdi/get-data-in/application/java/instrumentation/instrument-java-application.html#activate-alwayson-profiling)
in detail, but for now we just need one single setting:

`SPLUNK_PROFILER_ENABLED="true"`

Since our application is deployed in Kubernetes, we can update the Kubernetes manifest file to set this environment variable.  Open the `doorgame/doorgame.yaml` file for editing, and ensure the value of the `SPLUNK_PROFILER_ENABLED` environment variable is set to "true":

````
- name: SPLUNK_PROFILER_ENABLED
  value: "true"
````

Next, let's redeploy the Door Game application by running the following command: 

```
cd workshop/profiling
./4-redeploy-doorgame.sh
```

After a few minutes, a new pod will be deployed with the updated application settings. 

###  Confirm operation

To ensure the profiler is enabled, let's review the application logs with the following commands: 

````
kubectl logs -l app=doorgame --tail=100 | grep JfrActivator
````

You should see a line in the application log output that shows the profiler is active:

````
[otel.javaagent 2024-02-05 19:01:12:416 +0000] [main] INFO com.splunk.opentelemetry.profiler.JfrActivator - Profiler is active.```
````

This confirms that the profiler is enabled and sending data to the OpenTelemetry collector deployed in our Kubernetes cluster, which in turn sends profiling data to Splunk Observability Cloud. 

### Profiling in APM

Visit `http://<your IP address>:81` and play a few more rounds of The Door Game.

Then head on over to Splunk Observability Cloud, click on APM, 
and click on the `doorgame` service at the bottom of the screen. 

In the rightmost column you should see the "AlwaysOn Profiling"
card that looks similar to this:

![AlwaysOn Profiling](../images/always-on-profiling.png)

Click the card title to go to the AlwaysOn Profiling view. It will look something
like this:

![Flamegraph and table](../images/flamegraph_and_table.png)

By default, we show both the table and [flamegraph](https://www.brendangregg.com/flamegraphs.html).
Take some time to explore this view by doing some of the following:

* toggle between flamegraph and table views
* click a table item and notice the change in flamegraph
* navigate the flamegraph by clicking on a stack frame to zoom in, and a parent frame to zoom out
* add a search term like `splunk` or `jetty` to highlight some matching stack frames

We should note that the sample app is greatly underutilized and most of the time
is spent waiting for user input and service requests. As a result, the flame graph
should be somewhat less interesting than a high-volume, real-world production service.

### Traces with Call Stacks

Now that we've seen the profiling view, let's go back to the trace list view. We want to find a
trace that was long enough so that we increase the chance of having sampled call stacks.
If you haven't already, you should play The Door Game enough to stick with door 3
(either by choosing it initially and staying, or choosing another door and switching when given the chance).
You'll notice that it's slow, and it should show up at around 5s in the trace list view:

![Slow Trace](../images/slow_trace.png)

Identify the slow trace in the trace list view and click it to view the
individual trace. In the single trace view, you should see that the innermost span
`DoorGame.getOutcome` is responsible for the entire slow duration of the span.
There should be 2 call stacks sampled during the execution of that span.

![Span with Stacks](../images/span_with_stacks.png)

If you're up for the challenge, expand the span and explore the Java stack frames on your own
before we tackle it in the next section.


## What did we accomplish?

We've come a long way already!

* We learned how to enable the profiler in the Splunk OpenTelemetry Java instrumentation agent.
* We learned how to verify in the agent output that the profiler is enabled.
* We have explored several profiling related workflows in APM:
    * How to navigate to AlwaysOn Profiling from the troubleshooting view
    * How to explore the flamegraph and method call duration table through navigation and filtering
    * How to identify when a span has sampled call stacks associated with it

In the next section, we'll explore the profiling data further to determine what's causing the slowness, and then apply a fix to our application to resolve the issue. 