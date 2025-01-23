---
title: Using a Filter to Drop Spans in OpenTelemetry Collector
linkTitle: 5. Dropping Spans
time: 10 minutes
weight: 5
---

In this section, we will explore how to use the **Filter Processor** to selectively drop spans based on certain conditions.

Specifically, we will drop traces based on the span name, which is commonly used to filter out unwanted spans such as health checks or internal communication traces.

Filter Processor: The filter processor is the core of this workshop. It is configured to drop spans based on a specific condition. In this case, we are filtering out spans whose name is "/_healthz", typically associated with health check requests.

In the `[WORKSHOP]` directory create a new subdirectory called `5-dropping-spans`, then copy all the files from `4-resilience`.

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

{{% /notice %}}

{{% tab title="health.json" %}}

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

##### Simulate Trace Data

To test your configuration, you'll need to generate some trace data that includes a span named "/_healthz". This is typically seen in health check requests that many services send to verify their status.

Once the data is sent, the OpenTelemetry Collector should process it and drop any spans with the name "/_healthz". You can confirm this by checking the trace data in the destination where it is exported (e.g., Jaeger, Zipkin, or any other trace backend).

##### Error Mode Handling

If the filter processor encounters any issues, the `error_mode: ignore` setting will ensure that the processing continues even if there's an error. However, it’s useful to set up logging and monitoring to ensure that the filter configuration is working as expected.

For example, check the logs of the OpenTelemetry Collector for messages related to trace filtering.

##### Modify the Filter Condition

You can customize the filter condition to drop spans based on other criteria. For example, you might want to drop spans that have a specific tag or attribute.

Example of dropping spans based on an attribute:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'attributes["service.name"] == "frontend"'
```

This filter would drop spans where the `service.name` attribute is set to `frontend`.

##### Filter Multiple Spans

You can filter out multiple span names by extending the span list:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'name == "/_healthz"'
      - 'name == "/internal/metrics"'
```

This will drop spans with the names "/_healthz" and "/internal/metrics".

You can further extend this configuration to filter out spans based on different attributes, tags, or other criteria, making the OpenTelemetry Collector more customizable and efficient for your observability needs.
