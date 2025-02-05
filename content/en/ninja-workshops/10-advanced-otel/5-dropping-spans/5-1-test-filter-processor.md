---
title: 5.1 Test Filter Processor
linkTitle: 5.1 Test Filter Processor
weight: 1
---

To test your configuration, you'll need to generate some trace data that includes a span named `"/_healthz"`.

Copy the following JSON and save to a file called `health.json` in the `5-dropping-spans` directory:

{{% tabs %}}
{{% tab title="Compacted JSON" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"frontend"}}]},"scopeSpans":[{"scope":{"name":"healthz","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5B8EFFF798038103D269B633813FC60C","spanId":"EEE19B7EC3C1B174","parentSpanId":"EEE19B7EC3C1B173","name":"/_healthz","startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","kind":2,"attributes":[]}]}]}]}
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
                "stringValue": "frontend"
              }
            }
          ]
        },
        "scopeSpans": [
          {
            "scope": {
              "name": "healthz",
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
                "name": "/_healthz",
                "startTimeUnixNano": "1544712660000000000",
                "endTimeUnixNano": "1544712661000000000",
                "kind": 2,
                "attributes": []
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

Ensure that both the **Agent** and **Gateway** are started from the `[WORKSHOP]/5-dropping-spans` directory using their respective configuration.yaml files. Next, update and use the **cURL** command we used earlier to send the `health.json` payload.

Once the `span` payload is sent, the agent will process it, which you can confirm by checking the agent’s debug output to see the span data. The **Agent** will then forward the span to the **Gateway**. However, because the **Gateway** is configured with a filter to drop spans named `"/_healthz"`, the span will be discarded and not processed further.

The gateway console will remain unchanged, showing no indication that the data was received or handled.

To confirm functionality, you can use the cURL command with the `trace.json` file again. This time, you should see both the agent and gateway process the spans successfully.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

When using the `Filter` processor make sure you understand the look of your incoming data and test the configuration thoroughly. In general, use as specific a configuration as possible to lower the risk of the wrong data being dropped.
{{% /notice %}}

### (Optional) Modify the Filter Condition

If you’d like, you can customize the filter condition to drop spans based on different criteria. This step is optional and can be explored later. For example, you might configure the filter to drop spans that include a specific tag or attribute.

Here’s an example of dropping spans based on an attribute:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'attributes["service.name"] == "frontend"'
```

This filter would drop spans where the `service.name` attribute is set to `frontend`.

### (Optional) Filter Multiple Spans

You can filter out multiple span names by extending the span list:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'name == "/_healthz"'
      - 'name == "/internal/metrics"'
```

This will drop spans with the names `"/_healthz"` and `"/internal/metrics"`.

You can further extend this configuration to filter out spans based on different attributes, tags, or other criteria, making the OpenTelemetry Collector more customizable and efficient for your observability needs.

Stop the **Agent** and **Gateway** using Ctrl-C.
