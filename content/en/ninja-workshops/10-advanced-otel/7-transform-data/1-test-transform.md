---
title: Test Transform Processor
linkTitle: 7.1 Test Transform Processor
weight: 1
---

### Test the Transform

**Run the Log Generator**:
In the `test` terminal window, navigate to the `[WORKSHOP]/7-transform-data` directory and start the appropriate `log-gen` script for your system. We want to work with structured JSON logs, so add the `-json` flag to the script command. 

```sh
./log-gen.sh -json
```

The script will begin writing lines to a file named `./quotes.log`, while displaying a single line of output in the console. 

 ```txt
 Writing logs to quotes.log. Press Ctrl+C to stop.
 ```

**Run the Gateway**:
Find your `Gateway` terminal window, and navigate to the `[WORKSHOP]/7-transform-data` directory and restart the gateway.

It should start up normally and state : `Everything is ready. Begin running and processing data.`

**Run the Agent**:
Find your `Agent` terminal window and navigate to the `[WORKSHOP]/7-transform-data` directory and restart the agent with the resilience configurations specified in the YAML file.

It should also start up normally and state : `Everything is ready. Begin running and processing data.`

{{% notice title="Exercise" style="green" icon="running" %}}
In this exercise, we will **remove the** `com.splunk/source` and `os.type` **metadata** from the log resource attributes before it is exported by the `agent`. We will also parse the log body to set the `SeverityText` and `SeverityNumber` on the `LogRecord` and promote the log `body` json fields to log `attributes`.

- **Check the debug output** of both the `Agent` and `Gateway` to confirm that `com.splunk/source` and `os.type` have been removed.

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

- **Check the debug output** of both the `Agent` and `Gateway` to confirm that `SeverityText` and `SeverityNumber` in the `LogRecord` is now defined with the severity `level` from the log body. Confirm that the JSON fields from the body can be accessed as top-level log `Attributes`.

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

Stop the `agent` and `gateway` using Command-c/Ctrl-c.