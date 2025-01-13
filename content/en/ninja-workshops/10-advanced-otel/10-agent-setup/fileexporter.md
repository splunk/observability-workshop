---
title: Add a File exporter and Meta Data.
linkTitle: File exporter & Meta data
weight: 15
---
As we want to be able to see the output generated for the pipeline we are going to write the otlp data to files, so we can compare.

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

```

If you want it json expanded, you can cat the file and pipe it though jq ( if you have it installed)

```bash
cat ./agent.json | jq
```
