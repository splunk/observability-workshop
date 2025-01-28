---
title: Configuring a File exporter
linkTitle: 1.2 Adding a File exporter
weight: 2
---
### Different between Debug and FileExporter

To capture more than just debug output on the screen, we also want to generate output during the export phase of the pipeline. For this, we'll add a **File Exporter** to write OTLP data to files for comparison.

The difference between the OpenTelemetry **debug exporter** and the **file exporter** lies in their purpose and output destination:

| Feature               | Debug Exporter                   | File Exporter                  |
|-----------------------|----------------------------------|--------------------------------|
| **Output Location**   | Console/Log                     | File on disk                  |
| **Purpose**           | Real-time debugging             | Persistent offline analysis   |
| **Best for**          | Quick inspection during testing | Temporary storage and sharing |
| **Production Use**    | No                              | Rare, but possible            |
| **Persistence**       | No                              | Yes                           |

In summary, the **debug exporter** is great for real-time, in-development troubleshooting, while the **file exporter** is better suited for storing telemetry data locally for later use.

Let's configure and add the `FileExporter`:

{{% notice title="Exercise" style="green" icon="running" %}}

- **Configuring a `file` exporter**: Add the following under the `exporters` section of your `agent.yaml`:

  ```yaml
    file:                  # Exporter Type
      path: "./agent.out"  # Path where data will be saved in OTLP json format
      append: false        # Overwrite the file each time
  ```

- **Update the Pipelines Section**: Add the `file` exporter to the `metrics`, `traces` and `logs` pipelines (leave debug as the first in the array)

  ```yaml
     #traces:
      metrics:                    # Metrics Pipeline
        receivers: [otlp]         # Array of Metric Receivers
        processors:               # Array of Metric Processors
        - memory_limiter          # Handles memory limits for this Pipeline
        exporters: [debug, file]  # Array of Metric Exporters
     #logs:
  ```

{{% /notice %}}

### Validating your agent.yaml Configuration

To ensure your updated `agent.yaml` is correct, validate it using [**otelbin.io**](https://www.otelbin.io/).
As an example, the `Traces:` section of your pipelines should look similar to this in **otelbin.io**:

![otelbin-a-1-2-w](../../images/agent-1-2-traces.png?width=30vw)

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If **otelbin.io** flags a warning regarding the append entry in the exporter you added, check the validation target at the top of the screen. Ensure you’ve selected the Splunk OpenTelemetry Collector as the target.

{{% /notice %}}

### Test your agent.yaml Configuration

Restart your agent in the `Agent` terminal window, this time with your new config to test it:

```bash
../otelcol --config=agent.yaml
```

Again, if you have done everything correctly, the last line of the output should be:

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

If you send a trace again, from the `Test` terminal window you should get the same output on the console as we saw previously:

{{% tab title="cURL Command" %}}

```ps1
 curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
```

{{% /tab %}}

You now should have a file in the same directory called `agent.out`:

{{% tab title="Updated Directory Structure" %}}

```text
[WORKSHOP]
├── 1-agent         # Module directory
│   └── agent.yaml  # OpenTelemetry Collector configuration file
│   └── trace.json  # Sample trace data
│   └── agent.out   # OTLP/Json output created by the File Exporter
└── otelcol         # OpenTelemetry Collector binary
```

{{% /tab %}}

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

---

If you want to see the JSON expanded on your device, you can cat the file and pipe it though `jq` (if you have it installed).

```bash
cat ./agent.out | jq
```
