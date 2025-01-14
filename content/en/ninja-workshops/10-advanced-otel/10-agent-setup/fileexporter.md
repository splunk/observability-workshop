---
title: Add a File exporter.
linkTitle: File exporter
weight: 14
---
We want to see the output generated during the export phase of the pipeline, so we are going to write the otlp data to files for comparison.

Let's run our second exercise:

{{% notice title="Exercise" style="green" icon="running" %}}

* Add an **file:** exporter, add a *path:* entry, with a value of *"./agent.out"*
* Configure file size constrains by adding a *rotation:* section, add a *max_megabytes:* entry  with a value of *"2"* as well as and *max_backups:* also with a value of 2
* Add the exporter as the first exporter entry to all the pipelines (leaving debug as the second one )

{{% /notice %}}

Validate your new `agent.yaml` with [https://otelbin.io](https://otelbin.io), your pipelines should look like this:

![otelbin2](../../images/agent-1-2.png)

start your collector again with your new config to test it:

```text
otelcol_darwin_arm64 --config=agent.yaml
```

Again, if you have done everything correctly, the last line of the output should be:

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

If you send a trace again, you should get the same output as we saw previously, but you also should have a file in the same directory called **agent.out**
In the file the trace is written as a single line in oltp.json format, when you look at the file it looks like this:

```text
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5b8efff798038103d269b633813fc60c","spanId":"eee19b7ec3c1b174","parentSpanId":"eee19b7ec3c1b173","name":"I'm a server span","kind":2,"startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","attributes":[{"value":{"stringValue":"some value"}}],"status":{}}]}]}]}
```

If you want it json expanded, you can cat the file and pipe it though jq (if you have it installed)

```bash
cat ./agent.json | jq
```

Copy agent.out to agent-1.out or something, so you can use it to compare other results with.
