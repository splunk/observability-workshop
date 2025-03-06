---
title: 2.4 Send traces from the Agent to the Gateway
linkTitle: 2.4 Send Traces
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Send a Test Trace**:

1. Validate `agent` and `gateway` are still running.
2. Find your **Spans terminal** window
3. Navigate it to the `[WORKSHOP]/2-gateway` directory.
4. Run the following command to send 5 spans:

```bash { title="Start the Load Generator"}
../loadgen -count 5
```
  
Below, we show the first and last lines of the debug output. Use the **Complete Debug Output** button below to verify that both the `agent` and `gateway` produced similar debug output.

```text
2025-03-06T11:49:00.456Z        info    Traces  {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
<snip>
        {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces"}
```

{{% expand title="{{% badge style=primary icon=scroll %}}Complete Debug Output{{% /badge %}}" %}}

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

{{% /expand %}}

**Verify the Gateway has handled the spans**: Verify that the gateway has generated a new file named `./gateway-traces.out`.

```bash
jq -c '.resourceSpans[].scopeSpans[].spans[] | "Span \(input_line_number) found with spanId \(.spanId)"' ./gateway-traces.out
```

{{% /notice %}}

Stop the `agent` and the `gateway` processes by pressing `Ctrl-C` in their respective terminals.
