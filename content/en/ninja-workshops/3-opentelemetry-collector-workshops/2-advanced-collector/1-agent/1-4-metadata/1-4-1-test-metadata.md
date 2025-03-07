---
title: 1.4.1 Test Resource Metadata
linkTitle: 1.4.1 Test Resource Metadata
weight: 1
---
{{% notice title="Exercise" style="green" icon="running" %}}

**Restart your Agent**: In your **Agent terminal** window, and restart the `agent` using the updated configuration to test the changes:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

If everything is set up correctly, the last line of the output should confirm the collector is running:

```text
  2025-01-13T12:43:51.747+0100 info service@v0.120.0/service.go:261 Everything is ready. Begin running and processing data.
```

**Send a Trace**: From the **Spans terminal** window (making sure you are in the `1-agent` directory), send spans again with the `loadgen` binary to create a new `agent.out`:

```bash { title="Start Load Generator" }
../loadgen
```

**Check the Agent’s debug output**: You should see three new lines in the `resource attributes` section: (`host.name`, `os.type` & `otelcol.service.mode`):

```text
<snip>
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
    -> service.name: Str(cinema.service)
    -> deployment.environment: Str(production)
    -> host.name: Str([MY_HOST_NAME])
    -> os.type: Str([MY_OS])
    -> otelcol.service.mode: Str(agent)
</snip>
```

**Verify that metadata is added to spans**: Stop `loadgen` using `Ctrl-C`. In the new `agent.out` file:

1. Check for the existence of the`otelcol.service.mode` attribute in the `resourceSpans` section and that it has a value of `agent`.
2. Verify that the `resourcedetection` attributes (`host.name` and `os.type`) exist too.

These values are automatically added based on your device by the processors configured in the pipeline.

{{% tabs %}}
{{% tab title="cat ./agent.out" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"cinema-service"}},{"key":"deployment.environment","value":{"stringValue":"production"}},{"key":"host.name","value":{"stringValue":"RCASTLEY-M-YQRY.local"}},{"key":"os.type","value":{"stringValue":"darwin"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeSpans":[{"scope":{"name":"cinema.library","version":"1.0.0","attributes":[{"key":"fintest.scope.attribute","value":{"stringValue":"Starwars, LOTR"}}]},"spans":[{"traceId":"ae921957a4d93fa11cee640cd7908eb8","spanId":"f6b0f29825efe585","parentSpanId":"","name":"/movie-validator","kind":2,"startTimeUnixNano":"1740994347431796000","endTimeUnixNano":"1740994348431796000","attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.account_password","value":{"stringValue":"LOTR\u003eStarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}}],"status":{"message":"Success","code":1}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

{{% /tab %}}
{{% tab title="cat ./agent.out | jq" %}}

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
              "stringValue": "agent"
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
              "traceId": "ab984cd113463aa919ac200751fcfc1d",
              "spanId": "db651e116290a8f2",
              "parentSpanId": "",
              "name": "/movie-validator",
              "kind": 2,
              "startTimeUnixNano": "1740994462515044000",
              "endTimeUnixNano": "1740994463515044000",
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
{{% /notice %}}

Stop the `agent` and `loadgen` processes by using `Ctrl-C` in the respective terminal windows.
