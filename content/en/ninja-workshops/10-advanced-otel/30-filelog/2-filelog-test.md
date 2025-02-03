---
title: Test Filelog Receiver
linkTitle: 3.2 Test Configuration
weight: 2
---

In your gateway terminal window, navigate to the `[WORKSHOP]/3-filelog` directory, then start the gateway collector and wait for it to be ready to receive data.

Next, to test the Filelog Receiver, switch to your agent terminal window, navigate to the same `[WORKSHOP]/3-filelog` directory, and start the agent.

Once running, the agent should begin sending CPU metrics as before. Both the agent and the gateway should display debug output similar to the following:

{{% expand title="{{% badge style=primary icon=scroll %}}Check Full Debug Log{{% /badge %}}" %}}

```text
2025-01-18T21:25:01.806+0100    info    ResourceLog #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> com.splunk/source: Str(./quotes.log)
     -> host.name: (YOUR_HOST_NAME)
     -> os.type: Str(YOUR_OS)
     -> otelcol.service.mode: Str(gateway)
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
```

{{% /expand %}}

When the agent begins reading the `quotes.log` file, it will display this activity in the debug console output and forward the log lines to the gateway. The gateway pipeline will then generate the `gateway-log.out` file. At this point, your directory structure will appear as follows:

{{% tab title="Updated Directory Structure" %}}

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

{{% /tab %}}

The generated `gateway-log.out` file should look like this (below is a preview showing the beginning and a single log line; your actual output will contain many more):

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

The `resourceLogs` section includes the same attributes we observed in the `traces` and `metrics` sections. This shared attribute mechanism powers the **Related Content** feature in Splunk Observability, which seamlessly links and correlates logs, metrics, traces, and dashboards.

This feature is designed to help users quickly identify and investigate issues by providing a unified view of related telemetry data. Instead of isolating each data type, Splunk Observability connects them, enabling faster troubleshooting and more efficient root cause analysis.

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

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
You may have noticed that every log line contains empty placeholders for `"traceId":""` and `"spanId":""`. The Filelog receiver will populate these fields only if they are not already present in the log line. For example, if the log line is generated by an application instrumented with an OpenTelemetry instrumentation library, these fields will already be included and will not be overwritten.
{{% /notice %}}

Stop the Agent, Gateway and the Quotes generating script as well using `Command-c/Ctrl-c`.
