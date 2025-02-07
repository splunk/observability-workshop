---
title: 3.4 Test Filelog Receiver
linkTitle: 3.4 Test Filelog Receiver
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Check the log-gen script is running**: Find the **Tests** Terminal window, and check the script is still running, and the last line is still stating the below, if it not, restart it in the `[WORKSHOP]/3-filelog` folder.

```text
Writing logs to quotes.log. Press Ctrl+C to stop.
```

**Start the Gateway**:

1. Find your `Gateway` terminal window.
2. Navigate to the `[WORKSHOP]/3-filelog` directory.
3. Start the **Gateway** collector.

**Start the Agent**:

1. Switch to your `Agent` terminal window
2. Navigate to the `[WORKSHOP]/3-filelog` directory
3. Start the **Agent**.
4. Ignore the initial **CPU** metrics in the debug output and wait until the continuous stream of log data from the `quotes.log` appears. The debug output should look similar to the following (use the *Check Full Debug Log* to see all data):

```text
<snip>
Body: Str(2025-02-05 18:05:16 [INFO] - All we have to decide is what to do with the time that is given)us.
Attributes:
    -> log.file.path: Str(quotes.log)
</snip>
```

{{% expand title="{{% badge style=primary icon=scroll %}}Check Full Debug Log{{% /badge %}}" %}}

```text
2025-02-05T18:05:17.050+0100    info    Logs    {"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 1}
2025-02-05T18:05:17.050+0100    info    ResourceLog #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> com.splunk.source: Str(./quotes.log)
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(PH-Windows-Box.hagen-ict.nl)
     -> os.type: Str(windows)
     -> otelcol.service.mode: Str(gateway)
ScopeLogs #0
ScopeLogs SchemaURL:
InstrumentationScope
LogRecord #0
ObservedTimestamp: 2025-02-05 17:05:16.6926816 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str(2025-02-05 18:05:16 [INFO] - All we have to decide is what to do with the time that is given)us.
Attributes:
     -> log.file.path: Str(quotes.log)
Trace ID:
Span ID:
Flags: 0
        {"kind": "exporter", "data_type": "logs", "name": "debug"}
```

{{% /expand %}}

**Verify the gateway has handled the logs**:

1. **Windows only**: Stop the **Agent** and **Gateway** to flush the files.
2. Check if the **Gateway** has written a `./gateway-log.out` file.

At this point, your directory structure will appear as follows:

{{% tabs %}}
{{% tab title="Updated Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
│   ├── agent.yaml          # Agent Collector configuration file
│   ├── gateway-logs.out    # Output from the gateway logs pipeline
│   ├── gateway-metrics.out # Output from the gateway metrics pipeline
│   ├── gateway.yaml        # Gateway Collector configuration file
│   ├── log-gen.(sh or ps1) # Script to write a file with logs lines 
│   ├── quotes.log          # File containing Random log lines
│   └── trace.json          # Example trace file 
└── otelcol                 # OpenTelemetry Collector binary
```

{{% /tab %}}
{{% /tabs %}}

**Examine a log line in `gateway-log.out`**: Compare a log line with the snippet below. It is a preview showing the beginning and a single log line; your actual output will contain many, many more:

{{% tabs %}}
{{% tab title="cat /gateway-log.out" %}}

```json
{"resourceLogs":[{"resource":{"attributes":[{"key":"com.splunk.sourcetype","value":{"stringValue":"quotes"}},{"key":"com.splunk/source","value":{"stringValue":"./quotes.log"}},{"key":"host.name","value":{"stringValue":"[YOUR_HOST_NAME]"}},{"key":"os.type","value":{"stringValue":"[YOUR_OS]"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeLogs":[{"scope":{},"logRecords":[{"observedTimeUnixNano":"1737231901720160600","body":{"stringValue":"2025-01-18 21:25:01 [WARN] - Do or do not, there is no try."},"attributes":[{"key":"log.file.path","value":{"stringValue":"quotes.log"}}],"traceId":"","spanId":""}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
{"resourceLogs":[{"resource":{"attributes":[{"key":"com.splunk/source","value":{"stringValue":"./quotes.log"}},{"key":"com.splunk.sourcetype","value":{"stringValue":"quotes"}},{"key":"host.name","value":{"stringValue":"PH-Windows-Box.hagen-ict.nl"}},{"key":"os.type","value":{"stringValue":"windows"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeLogs":[{"scope":{},"logRecords":[{"observedTimeUnixNano":"1737231902719133000","body":{"stringValue":"2025-01-18 21:25:02 [DEBUG] - One does not simply walk into Mordor."},"attributes":[{"key":"log.file.path","value":{"stringValue":"quotes.log"}}],"traceId":"","spanId":""}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

{{% /tab %}}
{{% tab title="cat ./gateway-log.out | jq" %}}

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

**Examine the `resourceLogs` section**: Verify that the files include the same attributes we observed in the `traces` and `metrics` sections.

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
{{% /notice %}}
> [!NOTE]
> You may also have noticed that every log line contains empty placeholders for `"traceId":""` and `"spanId":""`.  
> The FileLog receiver will populate these fields only if they are not already present in the log line.
> For example, if the log line is generated by an application instrumented with an OpenTelemetry instrumentation library, these fields will already be included and will not be overwritten.


Stop the Agent, Gateway and the Quotes generating script as well using `Ctrl-C`.
