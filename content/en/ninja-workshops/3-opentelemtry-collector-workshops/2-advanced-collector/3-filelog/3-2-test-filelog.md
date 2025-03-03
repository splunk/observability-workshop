---
title: 3.2 Test FileLog Receiver
linkTitle: 3.2 Test FileLog Receiver
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**:

1. Find your **Gateway terminal** window.
2. Navigate to the `[WORKSHOP]/3-filelog` directory.
3. Start the `gateway`.

**Start the Agent**:

1. Switch to your **Agent terminal** window.
2. Navigate to the `[WORKSHOP]/3-filelog` directory.
3. Start the `agent`.
4. Ignore the initial **CPU** metrics in the debug output and wait until the continuous stream of log data from the `quotes.log` appears. The debug output should look similar to the following (use the {{% badge style=primary icon=scroll %}}Check Full Debug Log{{% /badge %}} to see all data):

```text
<snip>
Body: Str(2025-03-03 15:11:17 [INFO] - All we have to decide is what to do with the time that is given us.)
Attributes:
     -> log.file.path: Str(quotes.log)
</snip>
```

{{% expand title="{{% badge style=primary icon=scroll %}}Check Full Debug Log{{% /badge %}}" %}}

```text
2025-03-03T15:11:17.523Z        info    ResourceLog #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> com.splunk.source: Str(./quotes.log)
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(RCASTLEY-M-YQRY.local)
     -> os.type: Str(darwin)
     -> otelcol.service.mode: Str(gateway)
ScopeLogs #0
ScopeLogs SchemaURL:
InstrumentationScope
LogRecord #0
ObservedTimestamp: 2025-03-03 15:11:17.128113 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str(2025-03-03 15:11:17 [INFO] - All we have to decide is what to do with the time that is given us.)
Attributes:
     -> log.file.path: Str(quotes.log)
Trace ID:
Span ID:
Flags: 0
        {"kind": "exporter", "data_type": "logs", "name": "debug"}
2025-03-03T15:11:18.325Z        info    Logs    {"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 1}
```

{{% /expand %}}

**Verify the gateway has handled the logs**:

1. **Windows only**: Stop the `agent` and `gateway` to flush the files.
2. Check if the `gateway` has written a `./gateway-logs.out` file.

At this point, your directory structure will appear as follows:

```text { title="Updated Directory Structure" }
[WORKSHOP]
└── 3-filelog
    ├── agent.yaml
    ├── gateway-logs.out    # Output from the gateway logs pipeline
    ├── gateway-metrics.out # Output from the gateway metrics pipeline
    ├── gateway.yaml
    └── quotes.log          # File containing Random log lines
```

**Examine a log line**: In `gateway-logs.out` compare a log line with the snippet below. Verify that the log entry includes the same attributes as we have seen in metrics and traces data previously:

{{% tabs %}}
{{% tab title="cat /gateway-logs.out" %}}

```json
{"resourceLogs":[{"resource":{"attributes":[{"key":"com.splunk.source","value":{"stringValue":"./quotes.log"}},{"key":"com.splunk.sourcetype","value":{"stringValue":"quotes"}},{"key":"host.name","value":{"stringValue":"RCASTLEY-M-YQRY.local"}},{"key":"os.type","value":{"stringValue":"darwin"}},{"key":"otelcol.service.mode","value":{"stringValue":"gateway"}}]},"scopeLogs":[{"scope":{},"logRecords":[{"observedTimeUnixNano":"1741014677128113000","body":{"stringValue":"2025-03-03 15:11:17 [INFO] - All we have to decide is what to do with the time that is given us."},"attributes":[{"key":"log.file.path","value":{"stringValue":"quotes.log"}}],"traceId":"","spanId":""}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

{{% /tab %}}
{{% tab title="cat ./gateway-logs.out | jq" %}}

```json
{
  "resourceLogs": [
    {
      "resource": {
        "attributes": [
          {
            "key": "com.splunk.source",
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
      "scopeLogs": [
        {
          "scope": {},
          "logRecords": [
            {
              "observedTimeUnixNano": "1741014677128113000",
              "body": {
                "stringValue": "2025-03-03 15:11:17 [INFO] - All we have to decide is what to do with the time that is given us."
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

> [!NOTE]
> You may also have noticed that every log line contains empty placeholders for `"traceId":""` and `"spanId":""`.  
> The FileLog receiver will populate these fields only if they are not already present in the log line.
> For example, if the log line is generated by an application instrumented with an OpenTelemetry instrumentation library, these fields will already be included and will not be overwritten.

{{% /notice %}}

Stop the `agent`, `gateway` and `loagen` using `Ctrl-C`.
