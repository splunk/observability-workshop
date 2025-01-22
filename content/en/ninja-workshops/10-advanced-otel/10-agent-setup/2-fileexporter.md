---
title: Add a File exporter
linkTitle: 1.2 Add File exporter
weight: 2
---
### Setup

We not only want to see some debug flying across the screen, we also  want to see the output generated during the export phase of the pipeline. For this we are going to add a `FileExporter`

Let's run our next exercise:

{{% notice title="Exercise" style="green" icon="running" %}}

- **Add** `file:` **exporter** that writes the OTLP data to files for comparison.

  ```yaml
  exporters:
    file:                            # Exporter Type
      path: "./agent.out"            # Path where data will be saved in OTLP json format
      rotation:                      # Rotation settings for trace file
        max_megabytes: 2             # Maximum file size in MB before rotation
        max_backups: 2               # Maximum number of backups to keep
  ```

- **Update the Pipelines Section**: Add `file` exporter to the `metrics`, `traces` and `logs` pipelines. (leave debug as the first in the array)

```yaml
    # traces Pipeline
      metrics:                       # Metrics Pipeline
        receivers: [otlp].           # Array of Metric Receivers
        processors:                  # Array of Metric Processors
        - memory_limiter             # Handles memory limits for this Pipeline
        exporters: [debug,file]      # Array of Metric Exporters
     # logs Pipeline  
```

{{% /notice %}}

Validate your updated `agent.yaml` with **[otelbin.io](https://www.otelbin.io/)**. As an example, here is how the `Traces:` section of your pipelines should loo in OTelBin:

![otelbin-a-1-2-w](../../images/agent-1-2-traces.png?width=30vw)

---

### Test & Validate

Restart your collect this time with your new config to test it:

```bash
../otelcol --config=agent.yaml
```

Again, if you have done everything correctly, the last line of the output should be:

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

If you send a trace again, you should get the same output as we saw previously:

{{% tab title="cURL Command" %}}

```ps1
 curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
```

{{% /tab %}}

You now should have a file in the same directory called `agent.out`:

```text
[WORKSHOP]/1-agent/
├── agent.yaml    # Configuration file
├── agent.out     # Trace export file
├── trace.json    # Trace JSON file

```

In the file the trace is written as a single line in JSON format, when you look at the file it looks like this:

{{% tabs %}}
{{% tab title="Compacted JSON" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5B8EFFF798038103D269B633813FC60C","spanId":"EEE19B7EC3C1B174","parentSpanId":"EEE19B7EC3C1B173","name":"I'm a server span","startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","kind":2,"attributes":[{"keytest":"my.span.attr","value":{"stringValue":"some value"}}]}]}]}]}
```

{{% /tab %}}
{{% tab title="Formatted JSON" %}}

```json
{
    "resourceSpans": [
      {
        "resource": {
          "attributes": [
            {
              "key": "service.name",
              "value": {
                "stringValue": "my.service"
              }
            },
            {
              "key": "deployment.environment",
              "value": {
                "stringValue": "my.environment"
              }
            }
          ]
        },
        "scopeSpans": [
          {
            "scope": {
              "name": "my.library",
              "version": "1.0.0",
              "attributes": [
                {
                  "key": "my.scope.attribute",
                  "value": {
                    "stringValue": "some scope attribute"
                  }
                }
              ]
            },
            "spans": [
              {
                "traceId": "5B8EFFF798038103D269B633813FC60C",
                "spanId": "EEE19B7EC3C1B174",
                "parentSpanId": "EEE19B7EC3C1B173",
                "name": "I'm a server span",
                "startTimeUnixNano": "1544712660000000000",
                "endTimeUnixNano": "1544712661000000000",
                "kind": 2,
                "attributes": [
                  {
                    "keytest": "my.span.attr",
                    "value": {
                      "stringValue": "some value"
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
```

{{% /tab %}}
{{% /tabs %}}

If you want to see the JSON expanded on your device, you can cat the file and pipe it though `jq` (if you have it installed).

```bash
cat ./agent.out | jq
```

Copy `agent.out` to `agent-1.out` so you can use it to compare against other results later on in this workshop.
