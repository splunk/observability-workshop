---
title: 5.2 Validate the Configuration
linkTitle: 5.2 Validate Configuration
weight: 2
---

Everyone validates locally first. Cloud verification is optional.

## Local validation — required

| Change | Original telemetry | Expected processed telemetry |
|---|---|---|
| Filter spans | Five `/movie-validator` and five `/_healthz` spans | Five `/movie-validator` spans; no `/_healthz` spans |
| Change attributes | Phone, email, and password are visible | Phone replaced, email hashed, password removed |
| Redact values | Visa, Mastercard, and Amex are visible | Visa and Mastercard masked; Amex remains visible |
| Transform logs | Fields remain in the JSON body | Fields become attributes and severity is populated |

{{% notice title="One metrics pipeline" style="info" %}}
The `metrics` pipeline follows the original workshop pattern: it collects CPU
metrics at startup and then once per hour. It always writes to debug and
`agent-metrics.out`; cloud-enabled setups also send to SignalFx.
{{% /notice %}}

{{% expand title="1. Generate the trace test cases" %}}

In the **Loadgen** terminal, send five application spans and five health spans:

```bash
cd [WORKSHOP]/1-agent
../loadgen -health -count 5
```

`loadgen` prints a Base trace and a Health trace for each iteration. Copy one
Base trace ID if you plan to complete the cloud check.

The original application spans contain:

```text
user.phone_number = +1555-867-5309
user.email        = george@deathstar.email
user.password     = LOTR>StarWars1-2-3
user.visa         = 4111 1111 1111 1111
user.mastercard   = 5555 5555 5555 4444
user.amex         = 3782 822463 10005
```

{{% /expand %}}

{{% expand title="2. Compare spans before and after filtering" %}}

Count the post-processed spans in `agent-traces.out`:

```bash
jq -s -r '
  [.[].resourceSpans[].scopeSpans[].spans[]]
  | group_by(.name)[]
  | "\(length) \(.[0].name)"
' agent-traces.out
```

Expected output:

```text
5 /movie-validator
```

The missing `/_healthz` row proves that `filter/health` removed those spans
before local or cloud export.

{{% /expand %}}

{{% expand title="3. Compare sensitive attributes before and after processing" %}}

Inspect the latest application span:

```bash
jq -s '
  [.[].resourceSpans[].scopeSpans[].spans[]
   | select(.name == "/movie-validator")][-1]
  | [.attributes[]
     | select(.key | startswith("user."))
     | {key: .key, value: (.value.stringValue // .value.intValue)}]
' agent-traces.out
```

Confirm these results:

```text
user.phone_number = UNKNOWN NUMBER
user.email        = 62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287
user.password     = absent
user.visa         = ****
user.mastercard   = ****
user.amex         = 3782 822463 10005
```

Amex remains visible because the workshop policy intentionally omits its
pattern. This demonstrates how an incomplete policy behaves.

{{% /expand %}}

{{% expand title="4. Compare logs before and after transformation" %}}

Generate five JSON logs:

```bash
../loadgen -logs -json -count 5
```

View the original record:

```bash
head -n 1 quotes.log | jq .
```

Its `level`, `message`, `movie`, and `timestamp` fields are inside the JSON
body, and OpenTelemetry severity is not yet set.

Inspect the processed records:

```bash
jq -s '[
  .[].resourceLogs[].scopeLogs[].logRecords[]
  | {
      severityText,
      severityNumber,
      attributes: [.attributes[].key]
    }
]' agent-logs.out
```

Expected behavior:

- `DEBUG`, `INFO`, `WARN`, and `ERROR` map to severity numbers `5`, `9`, `13`,
  and `17`.
- `level`, `message`, `movie`, and `timestamp` appear as log attributes.
- Only `com.splunk.sourcetype`, `host.name`, and `otelcol.service.mode` remain
  as resource attributes.

{{% /expand %}}

{{% expand title="5. Confirm host metrics" %}}

```bash
jq -r '
  .resourceMetrics[].scopeMetrics[].metrics[]
  | select(.name == "system.cpu.time")
  | .name
' agent-metrics.out | sort -u
```

Expected output:

```text
system.cpu.time
```

{{% /expand %}}

{{% expand title="Optional: verify traces and metrics in Splunk Observability Cloud" %}}

Confirm that cloud export was enabled:

```bash
source ../workshop-env.sh
echo "${CONF2026_CLOUD_ENABLED}"
```

Continue only when the result is `true`. Telemetry can take a short time to
become searchable.

### Traces in APM

1. Open **APM > Trace Analyzer**, select **All traces**, and choose a time range
   beginning before the local test.
2. Search for the copied Base trace ID, or filter for service
   `cinema-service` and operation `/movie-validator`.
3. Confirm `/movie-validator` is present and `/_healthz` is absent.
4. Inspect the span properties and confirm the same attribute changes shown in
   the local output.

### Metrics in Infrastructure Monitoring

Read the detected host name:

```bash
jq -r '
  .resourceMetrics[].resource.attributes[]
  | select(.key == "host.name")
  | .value.stringValue
' agent-metrics.out | sort -u
```

Open **Infrastructure > Hosts**, locate that host, and confirm recent CPU data.

See
[Search traces using Trace Analyzer](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/search-traces-using-trace-analyzer),
[View spans within a trace](https://help.splunk.com/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/view-and-filter-for-spans-within-a-trace),
and
[Monitor hosts](https://help.splunk.com/en/splunk-observability-cloud/monitor-infrastructure/monitor-services-and-hosts/monitor-hosts).

{{% /expand %}}

{{< checkpoint "Local output proves filtering, attribute changes, redaction, and log transformation. Cloud-connected attendees can also verify traces in APM and metrics in Infrastructure Monitoring." >}}
