---
title: 1.3.1 Test File Exporter
linkTitle: 1.3.1 Test File Exporter
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Restart your agent**: Find your **Agent terminal** window, and (re)start the `agent` using the modified configuration:

{{% tabs %}}
{{% tab title="Start the Agent" %}}

```bash
../otelcol --config=agent.yaml
```

{{% /tab %}}
{{% tab title="Agent Output" %}}

```text
2025-01-13T12:43:51.747+0100 info service@v0.120.0/service.go:261 Everything is ready. Begin running and processing data.
```

{{% /tab %}}
{{% /tabs %}}

**Send a Trace**: From the **Spans terminal** window, send another span and verify you get the same output on the console as we saw previously:

```bash { title="Start Load Generator" }
../loadgen -count 1
```

We can now stop the `agent` in the **Agent terminal** window using `Ctrl-C` so that we can verify the `agent.out` file was written. 

**Verify that the `agent.out` file is written**: Check that a file named `agent.out` is written in the current directory.

```text { title="Updated Directory Structure" }
.
├── agent.out    # OTLP/Json output created by the File Exporter
└── agent.yaml
```

**Verify the span format**:

1. Verify the format used by the File Exporter to write the span to `agent.out`.  
2. The output will be a single line in **OTLP/JSON** format.
3. To view the contents of `agent.out`, you can use the `cat ./agent.out` command. For a more readable formatted view, pipe the output to `jq` like this: `cat ./agent.out | jq`:

{{% tabs %}}
{{% tab title="cat ./agent.out" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"cinema-service"}},{"key":"deployment.environment","value":{"stringValue":"production"}},{"key":"host.name","value":{"stringValue":"workshop-instance"}},{"key":"os.type","value":{"stringValue":"linux"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeSpans":[{"scope":{"name":"cinema.library","version":"1.0.0","attributes":[{"key":"fintest.scope.attribute","value":{"stringValue":"Starwars, LOTR"}}]},"spans":[{"traceId":"d824a28db5aa5f5a3011f19c452e5af0","spanId":"ab4cde146f77eacf","parentSpanId":"","name":"/movie-validator","kind":2,"startTimeUnixNano":"1741256991405300000","endTimeUnixNano":"1741256992405300000","attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.password","value":{"stringValue":"LOTR\u003eStarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}},{"key":"payment.amount","value":{"doubleValue":56.24}}],"status":{"message":"Success","code":1}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
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
              "traceId": "d824a28db5aa5f5a3011f19c452e5af0",
              "spanId": "ab4cde146f77eacf",
              "parentSpanId": "",
              "name": "/movie-validator",
              "kind": 2,
              "startTimeUnixNano": "1741256991405300000",
              "endTimeUnixNano": "1741256992405300000",
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
                  "key": "user.password",
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
                },
                {
                  "key": "payment.amount",
                  "value": {
                    "doubleValue": 56.24
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
