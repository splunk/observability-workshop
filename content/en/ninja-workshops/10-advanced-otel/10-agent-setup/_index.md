---
title: Initial setup our agent config  
linkTitle: 1. Initial Agent Setup
time: 10 minutes
weight: 1
---

### Setup

In your `[WORKSHOP]` directory, create a subdirectory named 1-agent and navigate into it.

```text
mkdir -p [WORKSHOP]/1-agent
cd [WORKSHOP]/1-agent
```

Inside the `1-agent` directory, create a file called `agent.yaml` and paste the following starting configuration into it:

```text
[WORKSHOP]
├── 1-agent         # Module directory
│   └── agent.yaml  # OpenTelemetry Collector configuration file
└── otelcol         # OpenTelemetry Collector binary
```

```yaml
receivers:

exporters:
    
processors:
  memory_limiter:
    check_interval: 2s
    limit_mib: 512
  
service:
  pipelines:
    traces:
      receivers: []
      processors:
      -
      exporters: []
    metrics:
      receivers: []
      processors: 
      -
      exporters: []
    logs: 
      receivers: []
      processors: 
      - 
      exporters: []
```

This is the basic structure of an OpenTelemetry Collector configuration file, defining the components you'll need to work with.

{{% notice title="Exercise" style="green" icon="running" %}}
Let's walk through a few modifications to get started:

1. **Add `otlp` receiver**: Under the `receivers` section, add the `otlp` receiver to enable the collector to receive telemetry data in the OTLP (OpenTelemetry Protocol) format.
2. **Add `protocols` section**: Under the `otlp` receiver.
3. **Add `http` key**: Under the `protocols` section, specify an `http` receiver type.
4. **Add `endpoint` key**: Set the value to `0.0.0.0:4318`. This will tell the Collector to listen for incoming telemetry data on this endpoint.

<!--
  - Add `otlp:` under the `receivers:` key (taking care to format it correctly)
    - Add `otlp:` key
      - Add `http:` key
        - Add `endpoint:` key and set a value of `"0.0.0.0:4318"`
-->
{{% expand title="{{% badge style=primary icon=lightbulb %}}**Hint**{{% /badge %}}" %}}
For proper formatting, make sure to align the YAML structure, paying attention to indentation.

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:4318"
```

{{% /expand %}}

5. **Add `debug` exporter**: Under the `exporters` section, add a `debug` exporter. This will help you see the collected data in a human-readable format in the logs.
6. **Add `verbosity` level**: Set the `verbosity` of the exporter to `detailed` for more comprehensive logging output.
7. **Update Pipelines**: Ensure that the `otlp` receiver, `memory_limiter` processor, and `debug` exporter are added to the pipelines for traces, metrics, and logs.

<!--
- Add a `debug` exporter under the `exporters:` key
  - Add `verbosity:`key and set it to a value of `detailed`
- Add the `otlp` receiver to the `traces:`, `metrics:` and `logs:` pipelines
- Add the `memory_limiter` processor to the `traces:`, `metrics:` and `logs:` pipelines
- Add the `debug` exporter to the `traces:`, `metrics:` and `logs:` pipelines-->
{{% expand title="{{% badge style=primary icon=lightbulb %}}**Hint**{{% /badge %}}" %}}

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors:   # you also could use [memory_limiter]
      - memory_limiter
      exporter: [debug]

    # metrics: pipeline section...  
```

{{% /expand %}}

{{% /notice %}}

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
In the exercise above, we’ve provided all the key elements in YAML format, but it’s up to you to correct and complete them. Be mindful of the formatting, as the OpenTelemetry Collector configuration is YAML-based.

Going forward, we will provide only a limited set of hints, so you'll need to apply what you've learned.

If you’re ever unsure about the format, you can refer to otelbin.io, which will display the default agent configuration when first accessed.
{{% /notice %}}

By using [**otelbin.io**](https://otelbin.io) to validate your `agent.yaml` file, you can quickly identify spelling or configuration errors. If everything is set up correctly, your configuration for all pipelines should look like this (click the image to enlarge):

<!--![otelbin-a-1-1-all](../images/agent-1-1-all.png)-->
![agent-traces](../images/agent-traces.png?classes=inline&width=20vw)
![agent-metrics](../images/agent-metrics.png?classes=inline&width=20vw)
![agent-logs](../images/agent-logs.png?classes=inline&width=20vw)

---

### Test & Validate

To test your configuration, run the following command (ensure you’re using the correct OpenTelemetry Collector binary you downloaded):

```text
../otelcol --config=agent.yaml
```

If everything is set up correctly, the last line of the output should read:

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

Next, open a new terminal window, create a file named `trace.json`, and copy the content from one of the tabs below (both tabs contain the same trace data):

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

In the second terminal window, run the following command to test your setup and validate the output:

{{% tabs %}}
{{% tab title="cURL Command" %}}

```ps1
 curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
```

{{% /tab %}}

{{% tab title="Debug Output" %}}

 ```text
 2025-01-13T13:26:13.502+0100 info Traces {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
2025-01-13T13:26:13.502+0100 info ResourceSpans #0
Resource SchemaURL:
Resource attributes:
     -> service.name: Str(my.service)
     -> deployment.environment: Str(my.environment)
ScopeSpans #0
ScopeSpans SchemaURL:
InstrumentationScope my.library 1.0.0
InstrumentationScope attributes:
     -> my.scope.attribute: Str(some scope attribute)
Span #0
    Trace ID       : 5b8efff798038103d269b633813fc60c
    Parent ID      : eee19b7ec3c1b173
    ID             : eee19b7ec3c1b174
    Name           : I'm a server span
    Kind           : Server
    Start time     : 2018-12-13 14:51:00 +0000 UTC
    End time       : 2018-12-13 14:51:01 +0000 UTC
    Status code    : Unset
    Status message :
Attributes:
     -> : Str(some value)
  {"kind": "exporter", "data_type": "traces", "name": "debug"}
```

{{% /tab %}}
{{% /tabs %}}

Once you've updated the configuration, you’re ready to proceed to running the OpenTelemetry Collector with your new setup. This exercise sets the foundation for understanding how data flows through the OpenTelemetry Collector, including receivers, processors, and exporters.
