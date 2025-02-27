---
title: 2.4 Send traces from the Agent to the Gateway
linkTitle: 2.4 Send Traces
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Validate both collectors are running**:

1. Find the **Agent** terminal window. If the **Agent** is stopped, restart it.
2. Find the **Gateway** terminal window. Check if the **Gateway** is running, otherwise restart it.

**Send a Test Trace**:

1. Find your **Tests** terminal window
2. Navigate it to the `[WORKSHOP]/2-gateway` directory.
3. Ensure that you have copied `trace.json` to the `2-gateway` directory.
4. Run the `cURL` command to send the span.
  
Below, we show the first and last lines of the debug output. Use the **Complete Debug Output** button below to verify that both the **Agent** and **Gateway** produced similar debug output.

```text
2025-02-05T15:55:18.966+0100    info    Traces  {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
<snip>
      {"kind": "exporter", "data_type": "traces", "name": "debug"}
```

{{% expand title="{{% badge style=primary icon=scroll %}}Complete Debug Output{{% /badge %}}" %}}

```text
        {"kind": "exporter", "data_type": "metrics", "name": "debug"}
2025-02-05T15:55:18.966+0100    info    Traces  {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
2025-02-05T15:55:18.966+0100    info    ResourceSpans #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> service.name: Str(my.service)
     -> deployment.environment: Str(my.environment)
     -> host.name: Str(PH-Windows-Box.hagen-ict.nl)
     -> os.type: Str(windows)
     -> otelcol.service.mode: Str(agent)
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
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.account_password: Str(LOTR>StarWars1-2-3)
```

{{% /expand %}}

**Gateway has handled the span**: Verify that the gateway has generated a new file named `./gateway-traces.out`.

{{% tabs %}}
{{% tab title="cat /gateway-traces.out" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}},{"key":"host.name","value":{"stringValue":"[YOUR_HOST_NAME]"}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5b8efff798038103d269b633813fc60c","spanId":"eee19b7ec3c1b174","parentSpanId":"eee19b7ec3c1b173","name":"I'm a server span","kind":2,"startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.account_password","value":{"stringValue":"LOTR\u003eStarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}}],"status":{}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

{{% /tab %}}
{{% tab title="cat /gateway-traces.out|jq" %}}

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
                  "key": "user.name",
                  "value": {
                    "stringValue": "George Lucas"
                  }
                },
                {
                  "key": "user.phone_number",
                  "value": {
                    "stringValue": "+1555-867-5309"
                  }
                },
                {
                  "key": "user.email",
                  "value": {
                    "stringValue": "george@deathstar.email"
                  }
                },
                {
                  "key": "user.account_password",
                  "value": {
                    "stringValue": "LOTR>StarWars1-2-3"
                  }
                },
                {
                  "key": "user.visa",
                  "value": {
                    "stringValue": "4111 1111 1111 1111"
                  }
                },
                {
                  "key": "user.amex",
                  "value": {
                    "stringValue": "3782 822463 10005"
                  }
                },
                {
                  "key": "user.mastercard",
                  "value": {
                    "stringValue": "5555 5555 5555 4444"
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

Ensure that both `gateway-metrics.out` and `gateway-traces.out` include a resource attribute key-value pair for `otelcol.service.mode` with the value `gateway`.

{{% /notice %}}
{{% notice note %}}
In the provided `gateway.yaml` configuration, we modified the `resource/add_mode` processor to use the `upsert` action instead of `insert`.
The `upsert` action updates the value of the resource attribute key if it already exists, setting it to `gateway`. If the key is not present, the `upsert` action will add it.
{{% /notice %}}

Stop the **Agent** and **Gateway** processes by pressing `Ctrl-C` in their respective terminals.
