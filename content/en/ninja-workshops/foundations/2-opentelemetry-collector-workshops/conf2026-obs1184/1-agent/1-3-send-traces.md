---
title: 1.3 Send traces to the agent
linkTitle: 1.3 Send traces
weight: 3
---

{{% exercise title="Send a test trace" %}}

1. Verify that the agent is still running in the **Agent terminal**.
2. In the **Command terminal**, send five spans:

{{% tabs %}}
{{% tab title="Start the Load Generator" %}}

```bash
../loadgen -count 5
```

{{% /tab %}}
{{% tab title="Agent debug output" %}}

```text
Traces  {"otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
ResourceSpans #0
Resource attributes:
     -> service.name: Str(cinema-service)
     -> deployment.environment: Str(production)
     -> host.name: Str(workshop-instance)
     -> os.type: Str(linux)
     -> otelcol.service.mode: Str(agent)
ScopeSpans #0
InstrumentationScope cinema.library 1.0.0
InstrumentationScope attributes:
     -> fintest.scope.attribute: Str(Starwars, LOTR)
Span #0
    Trace ID       : 97fb4e5b13400b5689e3306da7cff077
    Parent ID      :
    ID             : 413358465e5b4f15
    Name           : /movie-validator
    Kind           : Server
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
```

{{% /tab %}}
{{% /tabs %}}

In the **Agent terminal**, confirm that five `/movie-validator` spans appear.
Resource detection adds host information, and `resource/add_mode` adds
`otelcol.service.mode=agent`.

The sample sensitive values are workshop test data that later
exercises will modify. The spans are written to the console and
`agent-traces.out`; when cloud export is enabled, `otlp_http` also sends them
to Splunk APM.

{{% /exercise %}}
