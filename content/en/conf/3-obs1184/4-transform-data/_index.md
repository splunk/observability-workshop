---
title: 4. Transform logs
linkTitle: 4. Transform logs
time: 6 minutes
weight: 7
---

The [transform processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md)
uses OpenTelemetry Transformation Language (OTTL) to filter, enrich, and
transform telemetry without changing application code.

The File Log receiver reads each line into the log body. Even when the line is
JSON, severity and application fields are not automatically promoted into the
OpenTelemetry log record:

```text
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str({"level":"WARN","message":"Do or do not, there is no try."})
```

The unprocessed log resource also contains metadata that is not required after
collection. This example is from Linux. On Apple silicon, `os.type` is
`darwin`:

```text
Resource attributes:
     -> com.splunk.source: Str(./quotes.log)
     -> com.splunk.sourcetype: Str(quotes)
     -> service.name: Str(quote-generator)
     -> host.name: Str(workshop-instance)
     -> os.type: Str(linux)
     -> otelcol.service.mode: Str(agent)
```

You keep selected resource attributes, parse JSON fields into log
attributes, and map `level` to standard OpenTelemetry severity values. You will
Then you download the completed configuration and validate the filtering,
sensitive-data protection, and log transformation together in Chapter 5.
