---
title: Using a Filter to Drop Spans in OpenTelemetry Collector
linkTitle: 7. Dropping Spans
time: 10 minutes
weight: 7
---

In this section, we will explore how to use the **Filter Processor** to selectively drop spans based on certain conditions.

Specifically, we will drop traces based on the span name, which is commonly used to filter out unwanted spans such as health checks or internal communication traces. In this case, we will be filtering out spans whose name is `"/_healthz"`, typically associated with health check requests.

In the `[WORKSHOP]` directory create a new subdirectory called `5-dropping-spans`, then copy `agent.yaml`, `gateway.yaml`, `trace.json` and your `log-gen` script from `4-resilience`.

{{% tab title="Initial Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
├── 5-dropping-spans
│   ├── agent.yaml
│   ├── gateway.yaml
│   ├── log-gen.sh (or .ps1)
│   └── trace.json
└── otelcol
```

{{% /tab %}}

Open the `gateway.yaml` and add the following configuration to the `processors` section:

{{% notice title="Exercise" style="green" icon="running" %}}

- **Add a `filter` processor**: Configure the OpenTelemetry Collector to drop spans with the name `"/_healthz"`:

  ```yaml
    # Defines a filter processor
    filter:
      # Specifies that errors in the filter processor should be ignored
      error_mode: ignore
      # Configures filtering rules specifically for traces
      traces:
        # Applies the filter to spans within traces 
        span:
          # Excludes spans where the span name is "/_healthz"
          - 'name == "/_healthz"'
  ```

- **Add the `filter` processor**: Make sure you add the filter to the `traces` pipeline. Filtering should be applied as early as possible, ideally *right after the* memory_limiter and *before* the batch processor.

{{% /notice %}}

Validate the gateway configuration using **[otelbin.io](https://www.otelbin.io/)**, the results for the `traces` pipeline should look like this:

![otelbin-f-5-1-traces](../images/spans-5-1-trace.png)

### Simulate Trace Data

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

Ensure that both the `agent` and `gateway` are started from the `[WORKSHOP]/5-dropping-spans` folder using their respective configuration.yaml files. Next, update and use the **cURL** command we used earlier to send the `health.json` payload.

Once the `span` payload is sent, the agent will process it, which you can confirm by checking the agent’s debug output to see the span data. The `agent` will then forward the span to the `gateway`. However, because the `gateway` is configured with a filter to drop spans named `"/_healthz"`, the span will be discarded and not processed further.

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

Stop the `agent` and `gateway` using Command-c/Ctrl-c.
