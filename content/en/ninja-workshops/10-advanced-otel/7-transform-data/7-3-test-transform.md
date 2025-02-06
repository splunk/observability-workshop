---
title: 7.3 Test Transform Processor
linkTitle: 7.3 Test Transform Processor
weight: 3
---

This test verifies that the `com.splunk/source` and `os.type` metadata have been **removed** from the log resource attributes before being exported by the **Agent**. Additionally, the test ensures that:  

1. The log body is parsed to extract severity information.  
   - `SeverityText` and `SeverityNumber` are set on the `LogRecord`.  
2. JSON fields from the log body are promoted to log `attributes`.  

This ensures proper metadata filtering, severity mapping, and structured log enrichment before export.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Check the debug output** of both the **Agent** and **Gateway** to confirm that `com.splunk/source` and `os.type` have been removed.

{{% tabs %}}
{{% tab title="New Debug Output" %}}

  ```text
    Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(YOUR_HOST_NAME)
     -> otelcol.service.mode: Str(agent)
  ```

{{% /tab %}}
{{% tab title="Original Debug Output" %}}

  ```text
    Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> com.splunk/source: Str(./quotes.log)
     -> host.name: Str(YOUR_HOST_NAME)
     -> os.type: Str(YOUR_OS)
     -> otelcol.service.mode: Str(agent)
  ```

{{% /tab %}}
{{% /tabs %}}

- **Check the debug output** of both the **Agent** and **Gateway** to confirm that `SeverityText` and `SeverityNumber` in the `LogRecord` is now defined with the severity `level` from the log body. Confirm that the JSON fields from the body can be accessed as top-level log `Attributes`.

{{% tabs %}}
{{% tab title="New Debug Output" %}}

  ```text
  LogRecord #0
  ObservedTimestamp: 2025-01-31 21:49:29.924017 +0000 UTC
  Timestamp: 1970-01-01 00:00:00 +0000 UTC
  SeverityText: WARN
  SeverityNumber: Warn(13)
  Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
  Attributes:
      -> log.file.path: Str(quotes.log)
      -> timestamp: Str(2025-01-31 15:49:29)
      -> level: Str(WARN)
      -> message: Str(Do or do not, there is no try.)
  Trace ID:
  Span ID:
  Flags: 0
    {"kind": "exporter", "data_type": "logs", "name": "debug"}
  ```

{{% /tab %}}
{{% tab title="Original Debug Output" %}}

  ```text
  LogRecord #0
  ObservedTimestamp: 2025-01-31 21:49:29.924017 +0000 UTC
  Timestamp: 1970-01-01 00:00:00 +0000 UTC
  SeverityText: 
  SeverityNumber: Unspecified(0)
  Body: Str(2025-01-31 15:49:29 [WARN] - Do or do not, there is no try.)
  Attributes:
      -> log.file.path: Str(quotes.log)
  Trace ID:
  Span ID:
  Flags: 0
    {"kind": "exporter", "data_type": "logs", "name": "debug"}
  ```

{{% /tab %}}
{{% /tabs %}}

- **Check** the new `gateway-logs.out` file to verify the data has been transformed:

{{% tabs %}}
{{% tab title="New File Output" %}}

  ```json
        "resource": {
          "attributes": [
            {
              "key": "com.splunk.sourcetype",
              "value": {
                "stringValue": "quotes"
              }
            },
            {
              "key": "host.name",
              "value": {
                "stringValue": "YOUR_HOST_NAME"
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
                "observedTimeUnixNano": "1738360169924017000",
                "severityText": "WARN",
                "body": {
                  "stringValue": "2025-01-31 15:49:29 [WARN] - Do or do not, there is no try."
                },
                "attributes": [
                  {
                    "key": "log.file.path",
                    "value": {
                      "stringValue": "quotes.log"
                    }
                  },
                  {
                    "key": "timestamp",
                    "value": {
                      "stringValue": "2025-01-31 15:49:29"
                    }
                  },
                  {
                    "key": "level",
                    "value": {
                      "stringValue": "WARN"
                    }
                  },
                  {
                    "key": "message",
                    "value": {
                      "stringValue": "Do or do not, there is no try."
                    }
                  }
                ],
                "traceId": "",
                "spanId": ""
              }
            ]
          }
        ]
  ```

{{% /tabs %}}
{{% tab title="Original File Output" %}}

  ```json
        "resource": {
          "attributes": [
            {
              "key": "com.splunk.sourcetype",
              "value": {
                "stringValue": "quotes"
              }
            },
            {
              "key": "com.splunk.source",
              "value": {
                "stringValue": "./quotes.log"
              }
            },
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
                "observedTimeUnixNano": "1738349801265812000",
                "body": {
                  "stringValue": "2025-01-31 12:56:41 [INFO] - There is some good in this world, and it's worth fighting for."
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
        ]
  ```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}

Stop the **Agent** and **Gateway** using `Ctrl-C`.
