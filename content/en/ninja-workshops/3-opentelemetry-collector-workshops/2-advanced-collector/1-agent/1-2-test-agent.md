---
title: 1.2 Test Agent Configuration
linkTitle: 1.2 Test Agent Configuration
weight: 2
---

You’re ready to start the OpenTelemetry Collector with the newly created `agent.yaml`. This exercise sets the foundation for understanding how data flows through the OpenTelemetry Collector.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Agent**: In the **Agent terminal** window run the following command:

```bash { title="Start Collector" }
../otelcol --config=agent.yaml
```

**Verify debug output**: If everything is configured correctly, the first and last lines of the output will look like:

```text
2025/01/13T12:43:51 settings.go:478: Set config to [agent.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.120.0/service.go:261 Everything is ready. Begin running and processing data.
```

**Send Test Span**: Instead of instrumenting an application, we’ll simulate sending trace data to the OpenTelemetry Collector using the `loadgen` tool.

In the **Spans terminal** window, change into the `1-agent` directory and run the following command to send a single span:

{{% tabs %}}
{{% tab title="Start Load Generator" %}}

```bash
../loadgen -count 1
```

{{% /tab %}}
{{% tab title="Load Generator Output" %}}

```text
Sending traces. Use Ctrl-C to stop.
Response: {"partialSuccess":{}}

Base trace sent with traceId: 1aacb1db8a6d510f10e52f154a7fdb90 and spanId: 7837a3a2d3635d9f
 ```

`{"partialSuccess":{}}`: Indicates 100% success, as the `partialSuccess` field is empty. In case of a partial failure, this field will include details about any failed parts.

{{% /tab %}}
{{% /tabs %}}

**Verify Debug Output**:

In the **Agent terminal** window check the collector's debug output:

```text
2025-03-06T10:11:35.174Z        info    Traces  {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
2025-03-06T10:11:35.174Z        info    ResourceSpans #0
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
    Trace ID       : 0ef4daa44a259a7199a948231bc383c0
    Parent ID      :
    ID             : e8fdd442c36cbfb1
    Name           : /movie-validator
    Kind           : Server
    Start time     : 2025-03-06 10:11:35.163557 +0000 UTC
    End time       : 2025-03-06 10:11:36.163557 +0000 UTC
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
     -> payment.amount: Double(86.48)
        {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces"}
```

{{% /notice %}}

Stop the `agent` in the **Agent terminal** window using `Ctrl-C`.
