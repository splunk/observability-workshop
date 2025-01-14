---
title: Add Meta Data.
linkTitle: Adding Meta data
weight: 16
---
What we have so far is basically a straight copy from the  trace we send though the otel collector,
Now lets start adding Meta data to the base trace. this is information we can use during trouble shooting etc. 

Let's run our next exercise:

{{% notice title="Exercise" style="green" icon="running" %}}

* Add a **resourcedetection:** processor, add a *detectors:* entry, with a value of *"[system]"* and add a second entry *override:* with the value *true*
* Add a **resource** processor and name it "*/add_mode:*
* Give it the following attributes by adding a *attributes:* section, add a *action:* entry  with a value of *insert* and a second entry *value:* with a value of *"agent"*. Add the *key:* entry with a value of  *otelcol.service.mode*
* Add the two processors to the list of processors in the pipelines (leaving memory_limiter as the first one )

{{% /notice %}}

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
 Make sure that the resource processor's attributes: section is an array, best to use the following construct:   

 <pre>
    section_name:  
      - entry: my_entry  
        value: "something"  
        key: my_key_attribute
 </pre>

{{% /notice %}}

Validate your new `agent.yaml` with [https://otelbin.io](https://otelbin.io), your pipelines should look like this:

![otelbin2](../../images/agent-1-3.png)

Restart your collector with your new config to test it:

```text
otelcol_darwin_arm64 --config=agent.yaml
```

Again, if you have done everything correctly, the last line of the output should be:

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

Send a trace again, check the agent.out, a new line shoudl have been written for you trace:

```text
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}},{"key":"host.name","value":{"stringValue":"[YOUR_HOST_NAME]"}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5b8efff798038103d269b633813fc60c","spanId":"eee19b7ec3c1b174","parentSpanId":"eee19b7ec3c1b173","name":"I'm a server span","kind":2,"startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","attributes":[{"value":{"stringValue":"some value"}}],"status":{}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

If you compare it to the original agent.out file you will note that the collector has added the following attributes to the resourceSpans section automatically:

```text
{"value":{"stringValue":"[YOUR_HOST_NAME]}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}
```

As a last exercise in this section, we are going to add a metric receiver:

 {{% notice title="Exercise" style="green" icon="running" %}}

* Add a **hostmetrics:** receiver, add a *collection_interval:* entry, with a value of *10s* and add a second entry *scrapers:*.  Add a value entry to this called *cpu:*
* Add the *hostmetrics* receiver to the metrics pipeline as a receiver (leaving otlp as the first one )

{{% /notice %}}

Validate again with [https://otelbin.io](https://otelbin.io), your result should look like this:
![otelbin-4](../../images/agent-1-4.png)

Restart the agent again using the agent.yaml and tail the agent.out, the collector  should  write metric lines to your agent.out every 10 seconds that looks like this:

Note that you get cpu entries for all the cpu's/cores present iny your system and that in the resourceMetrics section, you find the same attributes added as with the trace these will help with corelating between traces and metrics.

```text
{"resourceMetrics":[{"resource":{"attributes":[{"key":"host.name","value":{"stringValue":"YOUR_HOST_NAME"}},{"key":"os.type","value":{"stringValue":"YOUR_OS"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeMetrics":[{"scope":{"name":"github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver/internal/scraper/cpuscraper","version":"v0.116.0"},"metrics":[{"name":"system.cpu.time","description":"Total seconds each logical CPU spent on each mode.","unit":"s","sum":{"dataPoints":[{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1028590.93},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":447490.75},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":553542.9},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1029342.54},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":441906.19},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":558385.54},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu2"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":510378.43},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu2"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":247897.29},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu2"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1240666.69},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu2"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu3"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":406858.66},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu3"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":193601.05},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu3"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1403053.18},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu3"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu4"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":261857.23},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu4"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":123152.05},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu4"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1626135.19},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu4"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu5"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":142217.63},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu5"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":67345.17},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu5"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1805202.13},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu5"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu6"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":118140.45},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu6"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":33211.34},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu6"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1885711.2},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu6"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu7"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":68595.2},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu7"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":17934.11},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu7"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1951584.74},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu7"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu8"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":51432.76},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu8"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":12218.08},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu8"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1974897.05},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu8"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu9"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":42869.04},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu9"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":9223.64},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu9"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1986628.98},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu9"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0}],"aggregationTemporality":2,"isMonotonic":true}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.9.0"}]}
```

Stop the agent for now.