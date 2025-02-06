---
title: 1.4.1 Test Resource Metadata
linkTitle: 1.4.1 Test Resource Metadata
weight: 1
---
{{% notice title="Exercise" style="green" icon="running" %}}

- **Restart your Agent**
  1. Find your **Agent** terminal window, and restart your collector using the updated configuration to test the changes:

  ```bash
    ../otelcol --config=agent.yaml
  ```

    If everything is set up correctly, the last line of the output should confirm the collector is running:

    ```text
    2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
    ```

- **Send a Trace**:
  1. From the **Tests** terminal window, send a trace again with the `cURL` command to create a new `agent.out`:

  ```ps1
  curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
  ```

  2. Check the agent’s debug output, you should see three new lines in the `resource attributes` section: (`host.name`, `os.type` & `otelcol.service.mode`):

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

- **Verify** that a new `agent.out` file is created:
{{% tabs %}}

{{% tab title="Updated Directory Structure" %}}

```text
  [WORKSHOP]
  ├── 1-agent         # Module directory
  │   └── agent.out   # OTLP/Json output created by the File Exporter
  │   └── agent.yaml  # OpenTelemetry Collector configuration file
  │   └── trace.json  # Sample trace data
  └── otelcol         # OpenTelemetry Collector binary
```

{{% /tab %}}
{{% /tabs %}}

- **Verify that MetaData is added** to spans in the new `agent.out` file.
  1. Check for the existence of the`otelcol.service.mode` attribute in the `resourceSpans` section.
  2. Verify that the `resourcedetection` attributes (`host.name` and `os.type`) exist too.

  These values are automatically added based on your device by the processors configured in the pipeline.

{{% tabs %}}
{{% tab title="cat ./agent.out" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}},{"key":"host.name","value":{"stringValue":"[YOUR_HOST_NAME]"}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5b8efff798038103d269b633813fc60c","spanId":"eee19b7ec3c1b174","parentSpanId":"eee19b7ec3c1b173","name":"I'm a server span","kind":2,"startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.account_password","value":{"stringValue":"LOTR\u003eStarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}}],"status":{}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
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

{{% /notice%}}

Stop the **Agent** process by pressing `Ctrl-C` in the terminal window.
