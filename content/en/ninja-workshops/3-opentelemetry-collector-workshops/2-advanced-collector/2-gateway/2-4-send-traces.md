---
title: 2.4 Send traces from the Agent to the Gateway
linkTitle: 2.4 Send Traces
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Validate both collectors are running**:

1. Find the **Agent terminal** window. If the `agent` is stopped, restart it.
2. Find the **Gateway terminal** window. Check if the `gateway` is running, otherwise restart it.

**Send a Test Trace**:

1. Find your **Spans terminal** window
2. Navigate it to the `[WORKSHOP]/2-gateway` directory.
3. Run the following command to send spans:

```bash { title="Start the Load Generator"}
../loadgen
```
  
Below, we show the first and last lines of the debug output. Use the **Complete Debug Output** button below to verify that both the `agent` and `gateway` produced similar debug output.

```text
2025-03-03T10:25:22.852Z        info    Traces  {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
<snip>
        {"kind": "exporter", "data_type": "traces", "name": "debug"}
```

{{% expand title="{{% badge style=primary icon=scroll %}}Complete Debug Output{{% /badge %}}" %}}

```text
2025-03-03T10:25:22.852Z        info    Traces  {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
2025-03-03T10:25:22.852Z        info    ResourceSpans #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> service.name: Str(cinema-service)
     -> deployment.environment: Str(production)
     -> host.name: Str(RCASTLEY-M-YQRY.local)
     -> os.type: Str(darwin)
     -> otelcol.service.mode: Str(agent)
ScopeSpans #0
ScopeSpans SchemaURL:
InstrumentationScope cinema.library 1.0.0
InstrumentationScope attributes:
     -> fintest.scope.attribute: Str(Starwars, LOTR)
Span #0
    Trace ID       : d11c2f2a0d22cf459bbdd0ca86e6118f
    Parent ID      :
    ID             : d068611c407471c1
    Name           : /movie-validator
    Kind           : Server
    Start time     : 2025-03-03 10:25:22.685314 +0000 UTC
    End time       : 2025-03-03 10:25:23.685314 +0000 UTC
    Status code    : Ok
    Status message : Success
Attributes:
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.account_password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
        {"kind": "exporter", "data_type": "traces", "name": "debug"}
```

{{% /expand %}}

**Gateway has handled the span**: Verify that the gateway has generated a new file named `./gateway-traces.out`.

{{% tabs %}}
{{% tab title="cat ./gateway-traces.out" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"cinema-service"}},{"key":"deployment.environment","value":{"stringValue":"production"}},{"key":"host.name","value":{"stringValue":"RCASTLEY-M-YQRY.local"}},{"key":"os.type","value":{"stringValue":"darwin"}},{"key":"otelcol.service.mode","value":{"stringValue":"gateway"}}]},"scopeSpans":[{"scope":{"name":"cinema.library","version":"1.0.0","attributes":[{"key":"fintest.scope.attribute","value":{"stringValue":"Starwars, LOTR"}}]},"spans":[{"traceId":"0f80c9081d199c3d607d1265f26ef60c","spanId":"27b71a8e90ee4f4e","parentSpanId":"","name":"/movie-validator","kind":2,"startTimeUnixNano":"1740997517682094000","endTimeUnixNano":"1740997518682094000","attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.account_password","value":{"stringValue":"LOTR\u003eStarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}}],"status":{"message":"Success","code":1}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

{{% /tab %}}
{{% tab title="cat ./gateway-traces.out | jq" %}}

```json
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": {
              "stringValue": "cinema-service"
            }
          },
          {
            "key": "deployment.environment",
            "value": {
              "stringValue": "production"
            }
          },
          {
            "key": "host.name",
            "value": {
              "stringValue": "RCASTLEY-M-YQRY.local"
            }
          },
          {
            "key": "os.type",
            "value": {
              "stringValue": "darwin"
            }
          },
          {
            "key": "otelcol.service.mode",
            "value": {
              "stringValue": "gateway"
            }
          }
        ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "cinema.library",
            "version": "1.0.0",
            "attributes": [
              {
                "key": "fintest.scope.attribute",
                "value": {
                  "stringValue": "Starwars, LOTR"
                }
              }
            ]
          },
          "spans": [
            {
              "traceId": "d11c2f2a0d22cf459bbdd0ca86e6118f",
              "spanId": "d068611c407471c1",
              "parentSpanId": "",
              "name": "/movie-validator",
              "kind": 2,
              "startTimeUnixNano": "1740997522685314000",
              "endTimeUnixNano": "1740997523685314000",
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
              "status": {
                "message": "Success",
                "code": 1
              }
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

Stop the `agent` and `gateway` processes by pressing `Ctrl-C` in their respective terminals.
