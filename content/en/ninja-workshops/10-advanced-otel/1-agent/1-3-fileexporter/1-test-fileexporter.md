---
title: 1.3.1 Test File Exporter
linkTitle: 1.3.1 Test File Exporter
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

- **Restart your agent**
  1. Find your **Agent** terminal window, and (re)start the agent, this time with your new config to test it.

    ```bash
    ../otelcol --config=agent.yaml
    ```

  Again, if you have done everything correctly, the last line of the output should be:

  ```text
  2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
  ```

- **Send a Trace**:
  1. From the **Test** terminal window send another span.
  2. Verify you get the same output on the console as we saw previously:

  ```ps1
  curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
  ```

- **Verify that the `agent.out` file is written**:
  1. Check that a file named `agent.out` is written in the current directory.

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
{{% /tab %}}

{{% notice note %}}
On **Windows**, an open file may appear empty or cause issues when attempting to read it. To prevent this, make sure to stop the **Agent** or the **Gateway** before inspecting the file, as instructed.
{{% /notice %}}

- **Verify the span format**:
  1. Check the Format that The File Exporter has used to write the span to the `agent.out`.
  2. It should be a single line in OTLP/JSON format.
  3. Since no modifications have been made to the pipeline yet, this file should be identical to `trace.json`.

{{% tabs %}}
{{% tab title="cat ./agent.out" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5B8EFFF798038103D269B633813FC60C","spanId":"EEE19B7EC3C1B174","parentSpanId":"EEE19B7EC3C1B173","name":"I'm a server span","startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","kind":2,"attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.account_password","value":{"stringValue":"LOTR>StarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}}]}]}]}]}
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

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If you want to view the file’s content, simply run:

```sh
cat agent.out
```

For a formatted JSON output, you can use the same command but pipe it through **jq** (if installed):

```bash
cat ./agent.out | jq
```

{{% /notice %}}
