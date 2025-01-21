---
title: Configure the filelog receiver in the agent
linkTitle: 3.1 Agent Filelog Config
weight: 1
---

### Upate the agent configuration

Check that you are in the `[WORKSHOP]/3-filelog` folder.  Open the `agent.yaml` copied across earlier and in your editor and add the `filelog` receiver to the `agent.yaml`.

{{% notice title="Exercise" style="green" icon="running" %}}

- Add `filelog` under the `receivers:` key and name it `./quotes:`
  - Add `include:` key and set it to a value of  `[./quotes.log]`
  - Add `include_file_path:` key and set it to a value of `true`
  - Add `include_file_name:` key and set it to a value of `false`
  - Add `resource:` key
    - Add `com.splunk.source:` key and set it to a value of `./quotes.log`
    - Add `com.splunk.sourcetype:` key and set it to a value of `quotes`

- Add `filelog/quotes` receiver to the `receivers:` array in the  `logs:` section of the pipelines.  (make sure it also contains `otlp`)

{{% /notice %}}

Again validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**, the results for the `Logs:` pipeline should look like this:

![otelbin-f-3-1-logs](../../images/filelog-3-1-logs.png)

---

## Test the Filelog receiver

From the `[WORKSHOP]/3-filelog` folder, start the collector in `gateway` mode in its own shell and wait until it is ready to receive data. Next, make sure the quotes generating script is running its own shell

Once we start the agent, the resulting file structure should looks lik this.

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
│   ├── agent.yaml          # Agent Collector configuration file
│   ├── gateway-logs.out.   # Output from the gateway logs pipeline
│   ├── gateway-metrics.out # Output from the gateway metrics pipeline
│   ├── gateway.yaml        # Gateway Collector configuration file
│   ├── log-gen.(sh or ps1) # Script to write a file with logs lines 
│   ├── quotes.log          # File containing Random log lines
│   └── trace.json          # Example trace file 
└── otelcol                 # OpenTelemetry Collector binary
```

Now, start the agent in a 3rd shell with:

```bash
../otelcol --config=agent.yaml
```

The agent should start to send *cpu* metrics again. However, the agent should also start reading the `quotes.log` file,and both the agent and the gateway should reflect that in their debug output lke this:

```text
2025-01-18T21:25:01.806+0100    info    ResourceLog #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> com.splunk/source: Str(./quotes.log)
     -> host.name: (YOUR_HOST_NAME)
     -> os.type: Str(YOUR_OS)
     -> otelcol.service.mode: Str(agent)
ScopeLogs #0
ScopeLogs SchemaURL:
InstrumentationScope
LogRecord #0
ObservedTimestamp: 2025-01-18 20:25:01.7201606 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str(2025-01-18 21:25:01 [WARN] - Do or do not, there is no try.)
Attributes:
     -> log.file.path: Str(quotes.log)
Trace ID:
Span ID:
Flags: 0
        {"kind": "exporter", "data_type": "logs", "name": "debug"}
```

As the agent is reading the `quotes.log` file and forwarding those log line to the gateway. The gateway pipeline should cause the `gateway-log.out` file to be generated with the following output:

{{% tabs %}}
{{% tab title="Compacted JSON" %}}

```json
{"resourceLogs":[{"resource":{"attributes":[{"key":"com.splunk.sourcetype","value":{"stringValue":"quotes"}},{"key":"com.splunk/source","value":{"stringValue":"./quotes.log"}},{"key":"host.name","value":{"stringValue":"[YOUR_HOST_NAME]"}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeLogs":[{"scope":{},"logRecords":[{"observedTimeUnixNano":"1737231901720160600","body":{"stringValue":"2025-01-18 21:25:01 [WARN] - Do or do not, there is no try."},"attributes":[{"key":"log.file.path","value":{"stringValue":"quotes.log"}}],"traceId":"","spanId":""}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
{"resourceLogs":[{"resource":{"attributes":[{"key":"com.splunk/source","value":{"stringValue":"./quotes.log"}},{"key":"com.splunk.sourcetype","value":{"stringValue":"quotes"}},{"key":"host.name","value":{"stringValue":"PH-Windows-Box.hagen-ict.nl"}},{"key":"os.type","value":{"stringValue":"windows"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeLogs":[{"scope":{},"logRecords":[{"observedTimeUnixNano":"1737231902719133000","body":{"stringValue":"2025-01-18 21:25:02 [DEBUG] - One does not simply walk into Mordor."},"attributes":[{"key":"log.file.path","value":{"stringValue":"quotes.log"}}],"traceId":"","spanId":""}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

{{% /tab %}}
{{% tab title="Formatted JSON" %}}

```json
{
  "resourceLogs": [
    {
      "resource": {
        "attributes": [
          {
            "key": "com.splunk/source",
            "value": {
              "stringValue": "./quotes.log"
            }
          },
          {
            "key": "com.splunk.sourcetype",
            "value": {
              "stringValue": "quotes"
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
      "scopeLogs": [
        {
          "scope": {},
          "logRecords": [
            {
              "observedTimeUnixNano": "1737231902719133000",
              "body": {
                "stringValue": "2025-01-18 21:25:02 [DEBUG] - One does not simply walk into Mordor."
              },
              "attributes": [
                {
                  "key": "log.file.path",
                  "value": {
                    "stringValue": "quotes.log"
                  }
                }
              ],
              "traceId": "",
              "spanId": ""
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

Note that the `resoureLogs` section contains the same attributes as we saw in `traces` and `metrics`. This mechanism is what will drive `related content` in Splunk Observability and  refers to the seamless linking and contextual correlation between logs, metrics, traces, and dashboards. This feature is designed to help users quickly identify and investigate issues by providing a unified view of related telemetry data. Instead of treating each data type in isolation, Splunk Observability connects them, enabling faster troubleshooting and root cause analysis.

{{% tabs %}}
{{% tab title="Compacted JSON" %}}

```json
{"resourceLogs":[{"resource":{"attributes":[{"key":"com.splunk.sourcetype","value":{"stringValue":"quotes"}},{"key":"com.splunk/source","value":{"stringValue":"./quotes.log"}},{"key":"host.name","value":{"stringValue":"[YOUR_HOST_NAME]"}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]}}]}
```

{{% /tab %}}
{{% tab title="Formatted JSON" %}}

```json
{
  "resourceLogs": [
    {
      "resource": {
        "attributes": [
          {
            "key": "com.splunk.sourcetype",
            "value": {
              "stringValue": "quotes"
            }
          },
          {
            "key": "com.splunk/source",
            "value": {
              "stringValue": "./quotes.log"
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
      }
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}
