---
title: Testing the initial agent configuration
linkTitle: 1.1 Test Configuration
weight: 1
---

Once you've updated the configuration, you’re ready to proceed to running the OpenTelemetry Collector with your new setup. This exercise sets the foundation for understanding how data flows through the OpenTelemetry Collector.

Start or reuse your initial terminal window, we will use this to run the `Agent`.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
To improve organization during the workshop, consider customizing your Terminal windows or Shells with unique names and colors. This will make it easier to identify and switch between them quickly.
{{% /notice %}}

Run the following command from the `1-agent` directory (ensure you’re using the correct OpenTelemetry Collector binary you downloaded):

```text
../otelcol --config=agent.yaml
```

If everything is set up correctly, the  first and last line of the output should read:

```text
2025/01/13T12:43:51 settings.go:478: Set config to [agent.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.117.0/service.go:261 Everything is ready. Begin running and processing data.
```

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
On `Windows` you may see a dialog box popup now, asking if you want to grant public and private networks access to the **otelcol.exe**, Please select **allow** to continue.

{{%/notice%}}

Rather than instrumenting an application, we will simulate sending trace data, in JSON format, to the OpenTelemetry Collector using `curl`.

Create a new file named `trace.json` and copy the content from one of the tabs below (both tabs contain the same trace data).

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

{{% tab title="Updated Directory Structure" %}}

```text
[WORKSHOP]
├── 1-agent         # Module directory
│   └── agent.yaml  # OpenTelemetry Collector configuration file
│   └── trace.json  # Sample trace data
└── otelcol         # OpenTelemetry Collector binary
```

{{%/tab%}}

Next, Open a second terminal window and navigate to the [WORKSHOP]/1-agent directory. In this new terminal (used for running 'Tests'), execute the following command to send a trace to test your setup:

```ps1
 curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
```

After you ran the **cURL** command in the 'Test' terminal, you should see an HTTP response like this in the terminal:

 ```text
 HTTP/1.1 200 OK
Content-Type: application/json
Date: Mon, 27 Jan 2025 09:51:02 GMT
Content-Length: 21

{"partialSuccess":{}}%
 ```

- HTTP/1.1 200 OK: Confirms the request was processed successfully.
- {“partialSuccess”:{}}: Indicates 100% success, as the field is empty. In case of a partial failure, this field will include details about any failed parts.

Next, check the agent’s debug console in the `Agent` terminal window. You should see a debug log for the trace you just sent, similar to this:

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

If everything worked as expected, you’re ready to continue building out the agent's YAML configuration file.
