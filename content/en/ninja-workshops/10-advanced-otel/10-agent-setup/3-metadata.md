---
title: Adding Resource Metadata
linkTitle: 1.3 Resource Metadata
weight: 3
---
### Setup

What we have done so far is basically exported a straight copy of trace we send though the OpenTelemetry collector. Now let's start adding some metadata to the base trace using `processors`, this is information we can use during trouble shooting and can be used for Related Content.

Let's run our next exercise:

{{% notice title="Exercise" style="green" icon="running" %}}
 We are going to modify data flowing though our pipelines with the following changes to the agent.yaml:

- **Add** `resourcedetection:` **processor** to detect info about the system the agent runs on.

  ```yaml
  resourcedetection:               # Processor Type
    detectors: [system]            # Array of Resource Detectors - (usually has cloud providers also)
    override: true                 # Existing attributes in data are overwritten by the processor.
  ```

- **Add** `resource:` **processor** and name it `add_mode:` to show what mode the agenn uses.

  ```yaml
<<<<<<< HEAD
  resource/add_mode:               # Processor Type/Name
    attributes:                    # Array of Attributes and modifications 
    - action: insert               # Action taken is to `insert' a key 
      key: otelcol.service.mode    # key Name
      value: "agent"               # Key Value
  ```
=======
    resource/add_mode:
      attributes:
      - action: insert
        key: otelcol.service.mode
        value: "agent"
    ```
>>>>>>> abf6c90d9 (Formatting fixes)

- Add the two processors to **ALL 3** `processors:` arrays in the pipelines (leaving `memory_limiter` as the first one)

  ```yaml
  traces:                         # Traces Pipeline
    receivers: [otlp]             # Array of Trace Receivers
    processors:                   # Array of Trace Processors
    - memory_limiter              # Handles memory limits for this Pipeline
    - resourcedetection           # Adds System Attributes to data flowing through this pipeline 
    - resource/add_mode           # Adds Collector mode to data flowing through this pipeline 
    exporters: [debug,file]       # Array of Trace exporters 
    # metric pipeline
    # logs pipeline
  ```

{{% /notice %}}

---

Validate your new `agent.yaml` with **[otelbin.io](https://www.otelbin.io/)** for spelling etc..

![otelbin-a-1-3-logs](../../images/agent-1-3-logs.png?width=50vw)

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
