---
title: 2.3 Sending data from the Agent to the Gateway
linkTitle: 2.3 Send Data
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Verify the `gateway` is still running**: Check your **Gateway** terminal window and make sure the **Gateway** collector is running.

**Start the Agent**: In the **Agent** terminal window start the agent with the updated configuration:

```bash
../otelcol --config=agent.yaml
```

**Verify CPU Metrics**:

1. Check that when the **Agent** starts, it immediately starts sending **CPU** metrics.
2. Both the **Agent** and the **Gateway** will display this activity in their debug output. The output should resemble the following snippet:

```text
<snip>
NumberDataPoints #37
Data point attributes:
    -> cpu: Str(cpu9)
    -> state: Str(system)
StartTimestamp: 2024-12-09 14:18:28 +0000 UTC
Timestamp: 2025-01-15 15:27:51.319526 +0000 UTC
Value: 9637.660000
```

At this stage, the **Agent** continues to collect **CPU** metrics once per hour or upon each restart and sends them to the gateway. The **OpenTelemetry Collector**, running in **Gateway** mode, processes these metrics and exports them to a file named `./gateway-metrics.out`. This file stores the exported metrics as part of the pipeline service.  

**Verify Data arrived at Gateway**:

1. Open the newly created `gateway-metrics.out` file.
2. Check that it contains **CPU** metrics.
3. The Metrics should include details similar to those shown below (We're only displaying the `resourceMetrics` section and the first set of **CPU** metrics — You will likely see more):

{{% tabs %}}
{{% tab title="cat `./gateway-metrics.out`" %}}

```json
{"resourceMetrics":[{"resource":{"attributes":[{"key":"host.name","value":{"stringValue":"YOUR_HOST_NAME"}},{"key":"os.type","value":{"stringValue":"YOUR_OS"}},{"key":"otelcol.service.mode","value":{"stringValue":"gateway"}}]},"scopeMetrics":[{"scope":{"name":"github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver/internal/scraper/cpuscraper","version":"v0.116.0"},"metrics":[{"name":"system.cpu.time","description":"Total seconds each logical CPU spent on each mode.","unit":"s","sum":{"dataPoints":[{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1737133726158376000","asDouble":1168005.59}]}}]}]}]}
```

{{% /tab %}}
{{% tab title="cat `./gateway-metrics.out` | jq" %}}

```json
{
  "resourceMetrics": [
    {
      "resource": {
        "attributes": [
          {
            "key": "host.name",
            "value": {
              "stringValue": "YOUR_HOST_NAME"
            }
          },
          {
            "key": "os.type",
            "value": {
              "stringValue": "YOUR_OS"
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
      "scopeMetrics": [
        {
          "scope": {
            "name": "github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver/internal/scraper/cpuscraper",
            "version": "v0.116.0"
          },
          "metrics": [
            {
              "name": "system.cpu.time",
              "description": "Total seconds each logical CPU spent on each mode.",
              "unit": "s",
              "sum": {
                "dataPoints": [
                  {
                    "attributes": [
                      {
                        "key": "cpu",
                        "value": {
                          "stringValue": "cpu0"
                        }
                      },
                      {
                        "key": "state",
                        "value": {
                          "stringValue": "user"
                        }
                      }
                    ],
                    "startTimeUnixNano": "1733753908000000000",
                    "timeUnixNano": "1737133726158376000",
                    "asDouble": 1168005.59
                  },
                ]
              }
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
