---
title: Add a File exporter
linkTitle: 1.1 File exporter
weight: 1
---
### Setup

We want to see the output generated during the export phase of the pipeline, so we are going to write the OTLP data to files for comparison.

Let's run our second exercise:

{{% notice title="Exercise" style="green" icon="running" %}}

- Add `file:` under `exporters:` key
  - Add `path:` key with a value of `"./agent.out"`
  - Add `rotation:` key
    - Add `max_megabytes:` key and set a value of `2` # This set the max size for the file exporter output file
    - Add `max_backups:` key and set a value of `2` # This will set the max number rotational backup it creates

Add `file` as an exporter to  exporters array in the `metrics`, `traces` and `logs` pipelines. (leave debug as the first in the array)

{{% /notice %}}

Validate your updated `agent.yaml` with **[otelbin.io](https://www.otelbin.io/)**, your pipelines should look like this:

![otelbin-a-1-2-w](../../images/agent-1-2w.png)

---

### Test & Validate

Restart your collect this time with your new config to test it:

```bash
[WORKSHOP]/otelcol --config=agent.yaml
```

Again, if you have done everything correctly, the last line of the output should be:

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

If you send a trace again, you should get the same output as we saw previously, but you also should have a file in the same directory called `agent.out`.
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
cat ./agent.json | jq
```

Copy `agent.out` to `agent-1.out` so you can use it to compare against other results later on in this workshop.
