---
title: 7.3 Test Transform Processor
linkTitle: 7.3 Test Transform Processor
weight: 3
---

This test verifies that the `com.splunk/source` and `os.type` metadata have been **removed** from the log resource attributes before being exported by the `agent`. Additionally, the test ensures that:  

1. The log body is parsed to extract severity information.  
   - `SeverityText` and `SeverityNumber` are set on the `LogRecord`.  
2. JSON fields from the log body are promoted to log `attributes`.  

This ensures proper metadata filtering, severity mapping, and structured log enrichment before export.

{{% notice title="Exercise" style="green" icon="running" %}}

**Check the debug output**: For both the `agent` and `gateway` confirm that `com.splunk/source` and `os.type` have been removed:

{{% tabs %}}
{{% tab title="New Debug Output" %}}

  ```text
Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(workshop-instance)
     -> otelcol.service.mode: Str(agent)
  ```

{{% /tab %}}
{{% tab title="Original Debug Output" %}}

  ```text
Resource attributes:
     -> com.splunk.source: Str(./quotes.log)
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(workshop-instance)
     -> os.type: Str(linux)
     -> otelcol.service.mode: Str(agent)
  ```

{{% /tab %}}
{{% /tabs %}}

For both the `agent` and `gateway` confirm that `SeverityText` and `SeverityNumber` in the `LogRecord` is now defined with the severity `level` from the log body. Confirm that the JSON fields from the body can be accessed as top-level log `Attributes`:

{{% tabs %}}
{{% tab title="New Debug Output" %}}

```text
<snip>
SeverityText: WARN
SeverityNumber: Warn(13)
Body: Str({"level":"WARN","message":"Your focus determines your reality.","movie":"SW","timestamp":"2025-03-07 11:17:26"})
Attributes:
     -> log.file.path: Str(quotes.log)
     -> level: Str(WARN)
     -> message: Str(Your focus determines your reality.)
     -> movie: Str(SW)
     -> timestamp: Str(2025-03-07 11:17:26)
</snip>
```

{{% /tab %}}
{{% tab title="Original Debug Output" %}}

```text
<snip>
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str({"level":"WARN","message":"Your focus determines your reality.","movie":"SW","timestamp":"2025-03-07 11:17:26"})
Attributes:
     -> log.file.path: Str(quotes.log)
</snip>
```

{{% /tab %}}
{{% /tabs %}}

**Check file output**: In the new `gateway-logs.out` file verify the data has been transformed:

{{% tabs %}}
{{% tab title="jq Query" %}}

```bash
jq '[.resourceLogs[].scopeLogs[].logRecords[] | {severityText, severityNumber, body: .body.stringValue}]' gateway-logs.out
```

{{% /tabs %}}
{{% tab title="Example Output" %}}

```json
[
  {
    "severityText": "DEBUG",
    "severityNumber": 5,
    "body": "{\"level\":\"DEBUG\",\"message\":\"All we have to decide is what to do with the time that is given us.\",\"movie\":\"LOTR\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  },
  {
    "severityText": "WARN",
    "severityNumber": 13,
    "body": "{\"level\":\"WARN\",\"message\":\"The Force will be with you. Always.\",\"movie\":\"SW\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  },
  {
    "severityText": "ERROR",
    "severityNumber": 17,
    "body": "{\"level\":\"ERROR\",\"message\":\"One does not simply walk into Mordor.\",\"movie\":\"LOTR\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  },
  {
    "severityText": "DEBUG",
    "severityNumber": 5,
    "body": "{\"level\":\"DEBUG\",\"message\":\"Do or do not, there is no try.\",\"movie\":\"SW\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  }
]
[
  {
    "severityText": "ERROR",
    "severityNumber": 17,
    "body": "{\"level\":\"ERROR\",\"message\":\"There is some good in this world, and it's worth fighting for.\",\"movie\":\"LOTR\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  }
]
```

{{% /tab %}}
{{% /tabs %}}

> [!IMPORTANT]
> Stop the `agent` and the `gateway` processes by pressing `Ctrl-C` in their respective terminals.

{{% /notice %}}
