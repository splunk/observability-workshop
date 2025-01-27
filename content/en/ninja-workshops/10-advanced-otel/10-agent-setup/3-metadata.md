---
title: Adding Resource Metadata
linkTitle: 1.3 Resource Metadata
weight: 3
---
### Setup

So far, we’ve essentially exported a direct copy of the trace sent through the OpenTelemetry Collector. Now, let’s enhance the base trace by adding metadata using `processors`. This additional information can be valuable for troubleshooting and for enabling features like Related Content.

{{% notice title="Exercise" style="green" icon="running" %}}
We will enhance the data flowing through our pipelines by making the following changes to the `agent.yaml`:  

- **Add the `resourcedetection` Processor**: The [**Resource Detection Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourcedetectionprocessor/README.md) can be used to detect resource information from the host and append or override the resource value in telemetry data with this information.

  ```yaml
    # Processor Type
    resourcedetection:
      # Array of resource detectors (e.g., system, cloud providers)
      detectors: [system]
      # Overwrites existing attributes in the data
      override: true
  ```

- **Add `resource` Processor (`add_mode`)**: The Resource Processor can be used to apply changes on resource attributes.

  ```yaml
    resource/add_mode:             # Processor Type/Name
      attributes:                  # Array of attributes and modifications
      - action: insert             # Action is to insert a key
        key: otelcol.service.mode  # Key name
        value: "agent"             # Key value
  ```

- **Update All Pipelines**: Add both processors (`resourcedetection` and `resource/add_mode`) to the `processors` array in **all pipelines** (traces, metrics, and logs). Ensure `memory_limiter` remains the first processor.

  ```yaml
    traces:                     # Traces Pipeline
      receivers: [otlp]         # Array of trace receivers
      processors:               # Array of trace processors
        - memory_limiter        # Handles memory limits for this pipeline
        - resourcedetection     # Adds system attributes to the data
        - resource/add_mode     # Adds collector mode metadata
      exporters: [debug, file]  # Array of trace exporters
    #metrics:
    #logs:
  ```

{{% /notice %}}

By adding these processors, we enrich the data with system metadata and the agent’s operational mode, which aids in troubleshooting and provides useful context for related content.

Validate your updated `agent.yaml` with **[otelbin.io](https://www.otelbin.io/)**:

![otelbin-a-1-3-logs](../../images/agent-1-3-logs.png?width=50vw)

### Test the Metadata Configuration

Rename `./agent.out` to `.agent.old`, this so you can compare it later.

{{% tab title="Updated Directory Structure" %}}

```text
[WORKSHOP]
├── 1-agent         # Module directory
│   └── agent.yaml  # OpenTelemetry Collector configuration file
│   └── trace.json  # Sample trace data
│   └── agent.old   # Copy of previous agent.out
└── otelcol         # OpenTelemetry Collector binary
```

{{%/tab%}}

Then restart your collector in the ` Agent` terminal window using the updated configuration to test the changes:

```bash
../otelcol --config=agent.yaml
```

If everything is set up correctly, the last line of the output should confirm the collector is running:

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

Next, from the `Test` terminal window, send a trace again with the `cURL` command to create a new `agent.out`:

{{% tab title="cURL Command" %}}

```ps1
 curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
```

{{% /tab %}}

In the agent’s debug output, you should see three new lines in the `Resource attributes section`: (host.name, os.type & otelcol.service.mode.)

```text
<snip>
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> service.name: Str(my.service)
     -> deployment.environment: Str(my.environment)
     -> host.name: Str([MY_HOST_NAME])
     -> os.type: Str([MY_OS])
     -> otelcol.service.mode: Str(agent)
</snip>
```

also a new `agent.out` file should be created:

{{% tab title="Updated Directory Structure" %}}

```text
[WORKSHOP]
├── 1-agent         # Module directory
│   └── agent.yaml  # OpenTelemetry Collector configuration file
│   └── trace.json  # Sample trace data
│   └── agent.old   # Copy of previous agent.out
│   └── agent.out   # OTLP/Json output created by the File Exporter
└── otelcol         # OpenTelemetry Collector binary
```

{{%/tab%}}

Check the newly created agent.out file. You should see a line written for the trace.

{{% tabs %}}
{{% tab title="Compacted JSON" %}}

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

When you compare the new `agent.out` file to the original `agent.old`, you’ll notice that the collector has added the `otelcol.service.mode` attribute, along with several `resourcedetection` attributes (`host.name` & `os.type`) to the `resourceSpans` section of the trace. These values are based on your device and were automatically added by the processors we configured in the pipeline:

{{% tabs %}}
{{% tab title="Compacted JSON" %}}

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
