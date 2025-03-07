---
title: 2.4 Send traces from the Agent to the Gateway
linkTitle: 2.4 Send Traces
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Send a Test Trace**:

1. Validate `agent` and `gateway` are still running.
2. In the **Spans terminal** window, run the following command to send 5 spans and validate the `agent` and `gateway` debug logs:

{{% tabs %}}
{{% tab title="Start the Load Generator" %}}

```bash
../loadgen -count 5
```

{{% /tab %}}
{{% tab title="Agent/Gateway Debug Output" %}}

```text
2025-03-06T11:49:00.456Z        info    Traces  {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
2025-03-06T11:49:00.456Z        info    ResourceSpans #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> service.name: Str(cinema-service)
     -> deployment.environment: Str(production)
     -> host.name: Str(workshop-instance)
     -> os.type: Str(linux)
     -> otelcol.service.mode: Str(agent)
ScopeSpans #0
ScopeSpans SchemaURL:
InstrumentationScope cinema.library 1.0.0
InstrumentationScope attributes:
     -> fintest.scope.attribute: Str(Starwars, LOTR)
Span #0
    Trace ID       : 97fb4e5b13400b5689e3306da7cff077
    Parent ID      :
    ID             : 413358465e5b4f15
    Name           : /movie-validator
    Kind           : Server
    Start time     : 2025-03-06 11:49:00.431915 +0000 UTC
    End time       : 2025-03-06 11:49:01.431915 +0000 UTC
    Status code    : Ok
    Status message : Success
Attributes:
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
     -> payment.amount: Double(87.01)
        {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces"}
```

{{% /tab %}}
{{% /tabs %}}

**Verify the Gateway has handled the spans**: After the gateway processes the incoming spans, it writes the trace data to a file named `gateway-traces.out`. To confirm that the gateway has successfully handled the spans, you can inspect this file. Specifically, you can use the `jq` command to extract and display relevant information about each span, such as its `spanId` and its position in the file.

{{% tabs %}}
{{% tab title="Inspect the Gateway Trace File" %}}

```bash
jq -c '.resourceSpans[].scopeSpans[].spans[] | "Span \(input_line_number) found with spanId \(.spanId)"' ./gateway-traces.out
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
"Span 1 found with spanId 830b45581f53b3d8"
"Span 2 found with spanId a82662dbed83cdee"
"Span 3 found with spanId b662569e8e52c6ac"
"Span 4 found with spanId 28b78a41a76162fa"
"Span 5 found with spanId 23b06e57f8af7336"
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}

Stop the `agent` and the `gateway` processes by pressing `Ctrl-C` in their respective terminals.
