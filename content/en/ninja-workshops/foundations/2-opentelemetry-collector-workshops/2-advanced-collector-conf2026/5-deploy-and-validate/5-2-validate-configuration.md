---
title: 5.2 Validate the Configuration
linkTitle: 5.2 Validate Configuration
weight: 2
---

Keep the updated Agent running in the **Agent Console**. Run the commands in
this step from the **Loadgen** terminal.

{{% notice title="Cloud validation is conditional" style="info" %}}
Local console and file validation works in every supported environment.
Apple Silicon attendees use those local checks and skip every cloud-validation
subsection.

Run the following without printing any credentials to see which optional
exporters were configured:

```bash
cd [WORKSHOP]/1-agent
source ../workshop-env.sh
echo "Observability Cloud: ${CONF2026_CLOUD_ENABLED}"
echo "Splunk HEC: ${CONF2026_HEC_ENABLED}"
```

Skip APM and infrastructure checks when Observability Cloud is `false`. Log
Observer validation additionally requires Splunk HEC to be `true` and a Log
Observer Connect integration for that Splunk Platform instance. Your Log
Observer Connect role must also have access to the index used by the HEC
token.
{{% /notice %}}

{{% exercise title="Validate filtering, sensitive-data protection, and log transformation" %}}

{{< step "Verify noisy health spans are dropped" "1" >}}

Generate five application spans and five health-check spans:

```bash
cd [WORKSHOP]/1-agent
../loadgen -health -count 5
```

The load generator creates one `/movie-validator` span and one `/_healthz`
span for each iteration before processing. Copy one of the base trace IDs from
the command output for the APM check below.

The **Agent Console** should show `/movie-validator` spans similar to:

```text
InstrumentationScope cinema.library 1.0.0
Span #0
    Name           : /movie-validator
    Kind           : Server
    Status code    : Ok
    Status message : Success
```

It must not show a processed `/_healthz` span. Confirm the local trace file:

```bash
jq -r '.resourceSpans[].scopeSpans[].spans[].name' agent-traces.out \
  | sort \
  | uniq -c
```

Expected result at this point:

```text
5 /movie-validator
```

**Validate filtering in Splunk Observability Cloud**

When Observability Cloud export is enabled:

1. Open **APM**, then **Traces** (Trace Analyzer).
2. Select a time range beginning immediately before this test and set the
   sample ratio to **All traces**.
3. Search for a base trace ID copied from `loadgen`. Open the trace and confirm
   it contains `/movie-validator` and does not contain `/_healthz`.
4. As a second check, search for service `cinema-service` and operation
   `/movie-validator`; fresh traces should be present.
5. Change the service to `frontend-service` and the operation to `/_healthz`
   within the same time range. No new trace should be present.

The negative result is meaningful only after the positive
`/movie-validator` result proves that this Agent successfully exported fresh
data. See [Search traces using Trace Analyzer](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/search-traces-using-trace-analyzer).

{{% notice title="Filtering guidance" style="warning" %}}
Use narrow conditions and test them against representative telemetry. Data
dropped by a filter cannot reach any later processor or exporter.
{{% /notice %}}

{{% notice title="After the workshop: extend the filter" style="primary" icon="lightbulb" %}}
Try a specific resource condition such as:

```ottl
resource.attributes["service.name"] == "frontend-service"
```

Or add another known noisy operation:

```ottl
span.name == "/internal/metrics"
```

Preview and validate the generated YAML before deploying either variation.
{{% /notice %}}

{{< /step >}}

{{< step "Verify sensitive span attributes are protected" "2" >}}

Generate one additional application span and copy its trace ID:

```bash
../loadgen -count 1
```

Before processing, the span contains the original phone number, email,
password, and payment-card values shown in Chapter 3. The processed **Agent
Console** output should resemble:

```text
     -> user.phone_number: Str(UNKNOWN NUMBER)
     -> user.email: Str(62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287)
     -> user.visa: Str(****)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(****)
     -> redaction.masked.keys: Str(user.mastercard,user.visa)
     -> redaction.masked.count: Int(2)
```

`user.password` must be absent. The order of
`redaction.masked.keys` can vary.

Inspect the protected values on the most recently exported
`/movie-validator` span:

```bash
jq -s '
  [
    .[].resourceSpans[].scopeSpans[].spans[]
    | select(.name == "/movie-validator")
  ][-1]
  | [
      .attributes[]
      | select(
          .key == "user.phone_number"
          or .key == "user.email"
          or .key == "user.visa"
          or .key == "user.amex"
          or .key == "user.mastercard"
          or (.key | startswith("redaction."))
        )
      | {
          key: .key,
          value: (.value.stringValue // .value.intValue)
        }
    ]
' agent-traces.out
```

A representative subset is shown below. The generated email hash is
deterministic for this input, while summary-field ordering can vary:

```json
[
  {
    "key": "user.phone_number",
    "value": "UNKNOWN NUMBER"
  },
  {
    "key": "user.email",
    "value": "62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287"
  },
  {
    "key": "user.visa",
    "value": "****"
  },
  {
    "key": "user.amex",
    "value": "3782 822463 10005"
  },
  {
    "key": "user.mastercard",
    "value": "****"
  },
  {
    "key": "redaction.masked.keys",
    "value": "user.mastercard,user.visa"
  },
  {
    "key": "redaction.masked.count",
    "value": "2"
  }
]
```

The dedicated query below verifies that no exported span contains
`user.password`:

```bash
jq -s '
  [
    .[].resourceSpans[].scopeSpans[].spans[].attributes[]
    | select(.key == "user.password")
  ]
  | length
' agent-traces.out
```

Expected result:

```text
0
```

Setting `summary: debug` adds the masked-key names and count without exposing
the original values.

**Validate protected attributes in Splunk Observability Cloud**

When Observability Cloud export is enabled:

1. In **APM > Traces** (Trace Analyzer), keep **All traces** selected and use
   the narrow test time range.
2. Search for the trace ID from `../loadgen -count 1`.
3. Open the trace, select the `/movie-validator` span in the waterfall, and
   inspect its span properties.
4. Confirm the phone is `UNKNOWN NUMBER`, the email is hashed, `user.password`
   is absent, Visa and Mastercard are `****`, and Amex remains visible.

Organization visibility rules can hide some tags from filter controls. The
local `agent-traces.out` checks remain authoritative when a tag is not
available as a Trace Analyzer filter. See
[View and filter spans within a trace](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/view-and-filter-for-spans-within-a-trace).

{{% notice title="After the workshop: cover Amex" style="primary" icon="lightbulb" %}}
Add this Amex pattern to the Redaction Processor, deploy the new YAML, and
confirm all three payment-card values are masked:

```text
\b3[47][0-9]{2}[\s-]?[0-9]{6}[\s-]?[0-9]{5}\b
```
{{% /notice %}}

{{< /step >}}

{{< step "Verify JSON log transformation" "3" >}}

Generate five JSON log lines:

```bash
../loadgen -logs -json -count 5
```

Confirm the source file contains five lines:

```bash
wc -l quotes.log
```

Expected result:

```text
5 quotes.log
```

The File Log Receiver reads these lines automatically. In the **Agent
Console**, confirm that a processed record resembles:

```text
Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(workshop-instance)
     -> otelcol.service.mode: Str(agent)
SeverityText: WARN
SeverityNumber: Warn(13)
Body: Str({"level":"WARN","message":"Your focus determines your reality.","movie":"SW","timestamp":"..."})
Attributes:
     -> log.file.path: Str(quotes.log)
     -> level: Str(WARN)
     -> message: Str(Your focus determines your reality.)
     -> movie: Str(SW)
     -> timestamp: Str(...)
```

The quote, timestamp, level, and detected host name vary. Verify that:

- Only `com.splunk.sourcetype`, `host.name`, and `otelcol.service.mode` remain
  as resource attributes.
- `com.splunk.source`, `service.name`, and `os.type` were removed.
- `SeverityText` matches the JSON `level`.
- `SeverityNumber` is `5`, `9`, `13`, or `17` for the generated `DEBUG`,
  `INFO`, `WARN`, or `ERROR` record.
- `level`, `message`, `movie`, and `timestamp` are promoted to log attributes.

Inspect severity and body in the local log file:

```bash
jq -s '
  [
    .[].resourceLogs[].scopeLogs[].logRecords[]
    | {
        severityText,
        severityNumber,
        body: .body.stringValue
      }
  ]
' agent-logs.out
```

The generated values are randomized, so your quotes, levels, movies, and
timestamps differ. A representative subset looks like:

```json
[
  {
    "severityText": "WARN",
    "severityNumber": 13,
    "body": "{\"level\":\"WARN\",\"message\":\"Your focus determines your reality.\",\"movie\":\"SW\",\"timestamp\":\"...\"}"
  },
  {
    "severityText": "ERROR",
    "severityNumber": 17,
    "body": "{\"level\":\"ERROR\",\"message\":\"One does not simply walk into Mordor.\",\"movie\":\"LOTR\",\"timestamp\":\"...\"}"
  }
]
```

Inspect the promoted fields:

```bash
jq -s '
  [
    .[].resourceLogs[].scopeLogs[].logRecords[]
    | {
        severityText,
        severityNumber,
        level: ([.attributes[] | select(.key == "level") | .value.stringValue][0]),
        message: ([.attributes[] | select(.key == "message") | .value.stringValue][0]),
        movie: ([.attributes[] | select(.key == "movie") | .value.stringValue][0]),
        timestamp: ([.attributes[] | select(.key == "timestamp") | .value.stringValue][0])
      }
  ]
' agent-logs.out
```

Confirm the retained resource keys:

```bash
jq -s '
  [.[].resourceLogs[].resource.attributes[].key]
  | unique
' agent-logs.out
```

Expected result:

```json
[
  "com.splunk.sourcetype",
  "host.name",
  "otelcol.service.mode"
]
```

**Validate transformed logs through Splunk Observability Cloud**

Run this subsection only when `CONF2026_HEC_ENABLED=true`, your Splunk
Platform instance is connected to Observability Cloud through Log Observer
Connect, and your role can access the index used by the HEC token.

1. Open **Logs > Log Observer** and choose the connection and index used by
   the HEC token.
2. Select a time range beginning immediately before this test.
3. Add a field filter for `source=otel` and, when exposed by the connection,
   `sourcetype=quotes`. If those fields are not extracted, search for a quote
   keyword from `quotes.log` and open the matching event.
4. In the log details, confirm `level`, `message`, `movie`, and `timestamp` are
   present. Inspect `otel.log.severity.text` and
   `otel.log.severity.number` rather than relying only on the severity column.

The regular quote logs do not use the Observability Cloud ingest token. They
are sent to the optional Splunk Platform HEC, and Log Observer Connect queries
that Splunk Platform data without storing it in Observability Cloud. If either
integration is unavailable, the local `agent-logs.out` validation completes
this exercise. See [Introduction to Log Observer Connect](https://help.splunk.com/en/splunk-observability-cloud/manage-data/view-splunk-platform-logs/introduction-to-splunk-log-observer-connect)
and [Search logs by keywords or fields](https://help.splunk.com/en/splunk-observability-cloud/manage-data/view-splunk-platform-logs/search-logs-by-keywords-or-fields).

{{< /step >}}

{{< step "Confirm the metrics connection" "4" >}}

When Observability Cloud export is enabled, determine the detected host name
from the local metrics file:

```bash
jq -r '
  .resourceMetrics[].resource.attributes[]
  | select(.key == "host.name")
  | .value.stringValue
' agent-metrics.out | sort -u
```

Open **Infrastructure > Hosts** and find that host. Confirm recent CPU, memory,
load, or network metrics are present.

Cloud-provider and Kubernetes hosts can appear in their corresponding
infrastructure navigator rather than the Hosts view. If needed, open
**Settings > Metric Metadata**, search for `host.name:<detected-host-name>`,
and confirm that recent host metrics exist. See
[Monitor hosts in Splunk Observability Cloud](https://help.splunk.com/en/splunk-observability-cloud/monitor-infrastructure/monitor-services-and-hosts/monitor-hosts).

A fresh APM trace and current host metrics confirm that both the `otlp_http`
trace exporter and `signalfx` metrics exporter are connected successfully.

{{< /step >}}

{{% /exercise %}}

{{% notice title="Stop the Agent" style="warning" %}}
Stop the Agent with `Ctrl-C` when all validation is complete.
{{% /notice %}}

{{< checkpoint "The updated Agent configuration has been validated locally and, where available, in the connected Splunk backends." >}}
