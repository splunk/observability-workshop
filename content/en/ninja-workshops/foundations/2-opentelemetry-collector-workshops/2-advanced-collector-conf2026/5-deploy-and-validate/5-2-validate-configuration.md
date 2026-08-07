---
title: 5.2 Validate the Configuration
linkTitle: 5.2 Validate Configuration
weight: 2
---

Keep the updated Collector running in the **Agent terminal**. Run every command
below in the **Command terminal**, which is already in `[WORKSHOP]/1-agent`.

## Local validation 1: Drop health-check spans

First, preview one application span and one health-check span exactly as the
load generator creates them:

```bash
../loadgen -preview -health -count 1
```

Preview mode prints the original OTLP payloads in the **Command terminal** and
does not send them. Find both span names in the output:

```json
"name": "/movie-validator"
"name": "/_healthz"
```

Now send five of each span through the Agent:

```bash
../loadgen -health -count 5
```

In the **Agent terminal**, the debug exporter prints five
`/movie-validator` spans. A processed span resembles this excerpt:

```text { title="Expected Agent debug output" }
InstrumentationScope cinema.library 1.0.0
Span #0
    Name           : /movie-validator
    Kind           : Server
    Status code    : Ok
```

The debug output does not contain a `/_healthz` span because `filter/health`
drops it before every trace exporter.

List the spans written by the file exporter:

```bash
jq -s -r '
  [.[].resourceSpans[].scopeSpans[].spans[]]
  | to_entries[]
  | "Span \(.key + 1) found with name \(.value.name)"
' ./agent-traces.out
```

Expected output:

```text
Span 1 found with name /movie-validator
Span 2 found with name /movie-validator
Span 3 found with name /movie-validator
Span 4 found with name /movie-validator
Span 5 found with name /movie-validator
```

Run an explicit check for the filter result:

```bash
jq -e -s '
  [.[].resourceSpans[].scopeSpans[].spans[]]
  | length == 5 and all(.name != "/_healthz")
' ./agent-traces.out
```

The result is `true`. The `-e` option also gives the command a nonzero exit
status if the assertion fails.

{{% notice title="Filter precisely" style="primary" icon="lightbulb" %}}
Use the most specific filter condition that fits your telemetry. Test it with
representative data before applying it broadly so that useful spans are not
dropped accidentally.
{{% /notice %}}

## Local validation 2: Protect sensitive span attributes

Preview one original `/movie-validator` span:

```bash
../loadgen -preview -count 1
```

In the **Command terminal**, the original OTLP payload includes these
synthetic values:

```text { title="Original span attributes" }
user.phone_number = +1555-867-5309
user.email        = george@deathstar.email
user.password     = LOTR>StarWars1-2-3
user.visa         = 4111 1111 1111 1111
user.mastercard   = 5555 5555 5555 4444
user.amex         = 3782 822463 10005
```

Send a new span through the Agent:

```bash
../loadgen -count 1
```

The **Agent terminal** shows the span after the `attributes` and `redaction`
processors. The payment amount can vary.

```text { title="Expected Agent debug output" }
Attributes:
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(UNKNOWN NUMBER)
     -> user.email: Str(62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287)
     -> payment.amount: Double(<random value>)
     -> user.visa: Str(****)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(****)
     -> redaction.masked.keys: Str(user.mastercard,user.visa)
     -> redaction.masked.count: Int(2)
```

`user.password` is absent. Inspect the latest application span in
`agent-traces.out`:

```bash
jq -s '
  [.[].resourceSpans[].scopeSpans[].spans[]
   | select(.name == "/movie-validator")][-1]
  | reduce .attributes[] as $attribute
      ({};
       .[$attribute.key] =
         ($attribute.value.stringValue
          // $attribute.value.intValue
          // $attribute.value.doubleValue))
  | {
      phone: .["user.phone_number"],
      email: .["user.email"],
      password_present: has("user.password"),
      visa: .["user.visa"],
      mastercard: .["user.mastercard"],
      amex: .["user.amex"]
    }
' ./agent-traces.out
```

Expected output:

```json
{
  "phone": "UNKNOWN NUMBER",
  "email": "62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287",
  "password_present": false,
  "visa": "****",
  "mastercard": "****",
  "amex": "3782 822463 10005"
}
```

The Amex value remains visible because the workshop policy deliberately omits
its pattern. This demonstrates the result of an incomplete redaction policy.

## Local validation 3: Transform JSON logs

Write five original JSON log lines to `quotes.log`:

```bash
../loadgen -logs -json -count 5
```

Read the five source records in the **Command terminal**:

```bash
jq . ./quotes.log
```

Each original line resembles this record. The generated level, message, movie,
and timestamp vary.

```json { title="Original quotes.log record" }
{
  "level": "WARN",
  "message": "Your focus determines your reality.",
  "movie": "SW",
  "timestamp": "2026-08-06 20:26:58"
}
```

The File Log receiver reads the records automatically. In the **Agent
terminal**, confirm that the transform processor sets OpenTelemetry severity,
promotes the JSON fields to attributes, and keeps only the selected resource
attributes:

```text { title="Expected Agent debug output" }
Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(<detected-host-name>)
     -> otelcol.service.mode: Str(agent)
LogRecord #0
SeverityText: WARN
SeverityNumber: Warn(13)
Body: Str({"level":"WARN","message":"Your focus determines your reality.","movie":"SW","timestamp":"<generated timestamp>"})
Attributes:
     -> log.file.name: Str(quotes.log)
     -> log.file.path: Str(quotes.log)
     -> level: Str(WARN)
     -> message: Str(Your focus determines your reality.)
     -> movie: Str(SW)
     -> timestamp: Str(<generated timestamp>)
```

Inspect the transformed records in `agent-logs.out`:

```bash
jq -s '[
  .[].resourceLogs[].scopeLogs[].logRecords[]
  | {
      severityText,
      severityNumber,
      body: .body.stringValue,
      attributes:
        ([.attributes[] | {key, value: .value.stringValue}]
         | from_entries)
    }
]' ./agent-logs.out
```

A transformed record resembles:

```json
{
  "severityText": "WARN",
  "severityNumber": 13,
  "body": "{\"level\":\"WARN\",\"message\":\"Your focus determines your reality.\",\"movie\":\"SW\",\"timestamp\":\"<generated timestamp>\"}",
  "attributes": {
    "log.file.name": "quotes.log",
    "log.file.path": "quotes.log",
    "level": "WARN",
    "message": "Your focus determines your reality.",
    "movie": "SW",
    "timestamp": "<generated timestamp>"
  }
}
```

Five random records might not include every level. When present, the configured
mappings are `DEBUG` → `5`, `INFO` → `9`, `WARN` → `13`, and `ERROR` → `17`.

## Optional: Validate in Splunk Observability Cloud

Confirm that cloud export was enabled during setup:

```bash
source ../workshop-env.sh
echo "${CONF2026_CLOUD_ENABLED}"
```

Continue when the result is `true`. Telemetry can take a short time to become
searchable.

### Confirm the filtered and protected traces

1. Open **APM > Trace Analyzer**, select **All traces**, and choose a time range
   beginning before the local tests.
2. Filter for service `cinema-service` and operation `/movie-validator`.
3. Open a recent trace and confirm the processed `user.*` attributes match the
   local result: the phone number is replaced, the email is hashed, the
   password is absent, and the configured card patterns are masked.
4. Search for operation `/_healthz` over the same test period and confirm that
   no workshop health-check spans were exported.

### Confirm host metrics

Print the exact host filter detected by the Agent:

```bash
jq -r '
  .resourceMetrics[].resource.attributes[]
  | select(.key == "host.name")
  | "host.name:\(.value.stringValue)"
' ./agent-metrics.out | sort -u
```

Open **Infrastructure > Hosts**, paste the resulting
`host.name:<detected-host-name>` value into the filter bar, and confirm recent
CPU, memory, load, or network data from the normal `metrics` pipeline.

The workshop `logs/workshop` pipeline intentionally exports to local debug and
`agent-logs.out`; it does not send these generated quote logs to Splunk
Observability Cloud.

See
[Search traces using Trace Analyzer](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/search-traces-using-trace-analyzer),
[View spans within a trace](https://help.splunk.com/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/view-and-filter-for-spans-within-a-trace),
and
[Monitor hosts](https://help.splunk.com/en/splunk-observability-cloud/monitor-infrastructure/monitor-services-and-hosts/monitor-hosts).

{{< checkpoint "Local output proves filtering, attribute changes, redaction, and log transformation. Cloud-connected attendees can also verify processed traces and host metrics in Splunk Observability Cloud." >}}
