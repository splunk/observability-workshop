---
title: Adding Resource Metadata
linkTitle: 1.2 Resource Metadata
weight: 2
---
### Setup

What we have so far is basically a straight copy from the trace we send though the OTel collector. Now lets start adding some metadata to the base trace, this is information we can use during trouble shooting etc.

Let's run our next exercise:

{{% notice title="Exercise" style="green" icon="running" %}}

- Add `resourcedetection:` under the `processors:` key
  - Add `detectors:` key and set a value of `[system]`
  - Add `override:` key and set a value of `true`
- Add `resource:` under the `processors:` key and name it `/add_mode:`
  - Add `attributes:` key
    - Add `- action:` key and set a value of `insert` * The - is on the same ident as of attributes
      - Add `key:` key and set a value of `otelcol.service.mode`
      - Add `value:` key wand set a value of `"agent"`

{{% expand title="{{% badge style=primary icon=lightbulb %}}**Hint**{{% /badge %}}" %}}

```yaml
  resource/add_mode:
    attributes:
    - action:
      key: #.......
```

{{% /expand %}}


- Add the two processors to `processors:` array in the pipelines (leaving `memory_limiter` as the first one)

{{% /notice %}}

---

Validate your new `agent.yaml` with **[otelbin.io](https://www.otelbin.io/)**.

![otelbin-a-1-3-w](../../images/agent-1-3w.png)

### Test & Validate

Delete the existing `./agent.out` file, then restart your collector with your new config to test it:

```bash
[WORKSHOP]/otelcol --config=agent.yaml
```

Again, if you have done everything correctly, the last line of the output should be:

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

Send a trace again, check the agent.out, a new line should have been written for your trace:

{{% tabs %}}
{{% tab title="Compact JSON" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}},{"key":"host.name","value":{"stringValue":"[YOUR_HOST_NAME]"}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5b8efff798038103d269b633813fc60c","spanId":"eee19b7ec3c1b174","parentSpanId":"eee19b7ec3c1b173","name":"I'm a server span","kind":2,"startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","attributes":[{"value":{"stringValue":"some value"}}],"status":{}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
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
          },
          {
            "key": "host.name",
            "value": {
              "stringValue": "[YOUR_HOST_NAME]"
            }
          },
          {
            "key": "os.type",
            "value": {
              "stringValue": "[YOUR_OS]"
            }
          },
          {
            "key": "otelcol.service.mode",
            "value": {
              "stringValue": "agent"
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
              "traceId": "5b8efff798038103d269b633813fc60c",
              "spanId": "eee19b7ec3c1b174",
              "parentSpanId": "eee19b7ec3c1b173",
              "name": "I'm a server span",
              "kind": 2,
              "startTimeUnixNano": "1544712660000000000",
              "endTimeUnixNano": "1544712661000000000",
              "attributes": [
                {
                  "value": {
                    "stringValue": "some value"
                  }
                }
              ],
              "status": {}
            }
          ]
        }
      ],
      "schemaUrl": "https://opentelemetry.io/schemas/1.6.1"
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

If you compare it to the original agent.out file you will note, the collector has added  the `otelcol.service.mode` attribute and a number of `resourcedetection` & `resource` attributes to the `resourceSpans` section of the trace.  These values are based on your device and added automatically as part of the processors we added to the pipeline:

{{% tabs %}}
{{% tab title="Compact JSON" %}}

```json
{"key":"host.name","value":{"stringValue":"[YOUR_HOST_NAME]"}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}
```

{{% /tab %}}
{{% tab title="Formatted JSON" %}}

```json
{
  "key": "host.name",
  "value": {
    "stringValue": "[YOUR_HOST_NAME]"
  }
},
{
  "key": "os.type",
  "value": {
    "stringValue": "[YOUR_OS]"
  }
},
{
  "key": "otelcol.service.mode",
  "value": {
    "stringValue": "agent"
  }
}
```

{{% /tab %}}
{{% /tabs %}}
