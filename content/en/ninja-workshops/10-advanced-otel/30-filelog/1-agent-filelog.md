---
title: Configure the filelog receiver in the agent
linkTitle: 3.1 Agent Filelog Config
weight: 1
---

### Update the agent configuration

Check that you are in the `[WORKSHOP]/3-filelog` directory.  Open the `agent.yaml` copied across earlier and in your editor and add the `filelog` receiver to the `agent.yaml`.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Add the `filelog` receiver**: The Filelog receiver reads log data from a file and includes custom resource attributes in the log data:

  ```yaml
    # Define a filelog receiver named "quotes"
    filelog/quotes:
      # Specifies the file to read log data from (quotes.log)
      include: ./quotes.log
      # Includes the full file path in the log data
      include_file_path: true
      # Excludes the file name from the log data
      include_file_name: false
      # Add custom resource attributes to the log data
      resource:
        # Sets the source of the log data to "quotes.log"
        com.splunk.source: ./quotes.log
        # Sets the sourcetype for the log data to "quotes"
        com.splunk.sourcetype: quotes
  ```

- Add `filelog/quotes` receiver to the `receivers` array in the `logs` section of the pipelines.  (make sure it also contains `otlp`)

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**, the results for the `Logs` pipeline should look like this:

![otelbin-f-3-1-logs](../../images/filelog-3-1-logs.png)

---

### Test the Filelog receiver

Find your `gateway` terminal window, navigate to the `[WORKSHOP]/3-filelog` directory, start the `gateway` collector and wait until it is ready to receive data.

Next, to test the Filelog Receiver, find your `agent` terminal window, navigate to the `[WORKSHOP]/3-filelog` directory and start the agent.

The agent should start to send **CPU** metrics again as before and both the agent and the gateway should reflect that in their debug output like this:

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

When the agent begins reading the `quotes.log` file, it will display this activity in the debug console output and forward the log lines to the gateway.

The gateway pipeline will then generate the `gateway-log.out` file. At this point, your directory structure will appear as follows:

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

The resulting `gateway-log.out` should look like this: (We only show the top and a single log line, you will have many more)

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
