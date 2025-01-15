---
title: Add Meta Data.
linkTitle: Adding Meta data
weight: 16
---
### Setup

What we have so far is basically a straight copy from the trace we send though the otel collector,
Now lets start adding Meta data to the base trace. this is information we can use during trouble shooting etc.

Let's run our next exercise:

{{% notice title="Exercise" style="green" icon="running" %}}

* Add the following processors:

```text
  resourcedetection: processor
    detectors: entry, with a value of [system] 
    override: with the value true
  resource: processor with a name  /add_mode:
    attributes: section
      - action: entry with a value of insert 
        value: entry with a value of "agent" 
        key: entry with a value of  otelcol.service.mode
```

* Add the two processors to the list of processors in the pipelines (leaving memory_limiter as the first one )

{{% /notice %}}

---

Validate your new `agent.yaml` with [https://otelbin.io](https://otelbin.io), your pipelines should look like this:

![otelbin2](../../images/agent-1-3.png)

### Test & Validate

Restart your collector with your new config to test it:

```bash
[LOCATION_OF_OTELCOLLECTOR]/otelcol --config=agent.yaml
```

Again, if you have done everything correctly, the last line of the output should be:

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

Send a trace again, check the agent.out, a new line should have been written for your trace:

```text
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}},{"key":"host.name","value":{"stringValue":"[YOUR_HOST_NAME]"}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5b8efff798038103d269b633813fc60c","spanId":"eee19b7ec3c1b174","parentSpanId":"eee19b7ec3c1b173","name":"I'm a server span","kind":2,"startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","attributes":[{"value":{"stringValue":"some value"}}],"status":{}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

If you compare it to the original agent.out file you will note that the collector has added the following attributes to the resourceSpans section automatically:

```text
{"value":{"stringValue":"[YOUR_HOST_NAME]}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}
```

### Adding Metrics

As a last exercise in this section, we are going to add a metric receiver:

 {{% notice title="Exercise" style="green" icon="running" %}}

* Add a the following receiver:

```text
    hostmetrics: receiver
      collection_interval: entry, with a value of 10s
      scrapers: entry  
        cpu: the single entry in the array of possible scrapers
```

* Add the *hostmetrics* receiver to the **metrics** pipeline as a receiver (leaving otlp as the first one )

{{% /notice %}}

Validate again with [https://otelbin.io](https://otelbin.io), your result should look like this:
![otelbin-4](../../images/agent-1-4.png)

### Metric Test & Validate

Restart the agent again using the agent.yaml and tail the agent.out, the collector  should  write metric lines to your agent.out every 10 seconds that looks like this:

Note that we show the entries for *cpu1* only, you will get cpu entries for all the cpu's/cores present in your system.  
Also note that in the resourceMetrics section, you find the same attributes added as with the trace, these will help with corelating between traces and metrics.

```text
{"resourceMetrics":[{"resource":{"attributes":[{"key":"host.name","value":{"stringValue":"YOUR_HOST_NAME"}},{"key":"os.type","value":{"stringValue":"YOUR_OS"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeMetrics":[{"scope":{"name":"github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver/internal/scraper/cpuscraper","version":"v0.116.0"},"metrics":[{"name":"system.cpu.time","description":"Total seconds each logical CPU spent on each mode.","unit":"s","sum":{"dataPoints":[{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1028590.93},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":447490.75},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":553542.9},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1029342.54},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":441906.19},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":558385.54},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":
}]}]}}]}]}]}
```

Stop the agent for now.
