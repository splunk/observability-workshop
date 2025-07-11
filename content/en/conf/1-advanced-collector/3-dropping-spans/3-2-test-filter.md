---
title: 3.2 Test Filter Processor
linkTitle: 3.2 Test Filter Processor
weight: 2
---

To test your configuration, you'll need to generate some trace data that includes a span named `"/_healthz"`.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In your **Gateway terminal** window start the **Gateway**.

```bash
../otelcol --config ./gateway.yaml
```

**Start the Agent**: In your **Agent terminal** window start the **Agent**.

```bash
../otelcol --config ./agent.yaml
```

**Start the Loadgen**: In the **Loadgen terminal** window run the `loadgen` with the flag to also send `healthz` spans along with base spans:
  
```bash
../loadgen -health -count 5
```

 The debug output in the **Agent terminal** will show `_healthz` spans:

 ```text
 InstrumentationScope healthz 1.0.0
Span #0
    Trace ID       : 0cce8759b5921c8f40b346b2f6e2f4b6
    Parent ID      :
    ID             : bc32bd0e4ddcb174
    Name           : /_healthz
    Kind           : Server
    Start time     : 2025-07-11 08:47:50.938703979 +0000 UTC
    End time       : 2025-07-11 08:47:51.938704091 +0000 UTC
    Status code    : Ok
    Status message : Success
```

They will not be present in the **Gateway** debug as they are dropped by the filter processor that was configured earlier.

**Verify `agent.out`**: Using `jq`, in the **Test terminal**, confirm the name of the spans received by the **Agent**:

{{% tabs %}}
{{% tab title="Check spans in agent.out" %}}

```bash
jq -c '.resourceSpans[].scopeSpans[].spans[] | "Span \(input_line_number) found with name \(.name)"' ./agent.out
```

{{% /tab %}}
{{% tab title="Example output" %}}

```text
"Span 1 found with name /movie-validator"
"Span 2 found with name /_healthz"
"Span 3 found with name /movie-validator"
"Span 4 found with name /_healthz"
"Span 5 found with name /movie-validator"
"Span 6 found with name /_healthz"
"Span 7 found with name /movie-validator"
"Span 8 found with name /_healthz"
"Span 9 found with name /movie-validator"
"Span 10 found with name /_healthz"
```

{{% /tab %}}
{{% /tabs %}}

**Check the Gateway Debug output**: Using `jq` confirm the name of the spans received by the **Gateway**:

{{% tabs %}}
{{% tab title="Check spans in gateway-traces.out" %}}

```bash { title="Check spans in gateway-traces.out" }
jq -c '.resourceSpans[].scopeSpans[].spans[] | "Span \(input_line_number) found with name \(.name)"' ./gateway-traces.out
```

{{% /tab %}}
{{% tab title="Example output" %}}

The `gateway-metrics.out` file will not contain any spans named `/_healthz`.

```text
"Span 1 found with name /movie-validator"
"Span 2 found with name /movie-validator"
"Span 3 found with name /movie-validator"
"Span 4 found with name /movie-validator"
"Span 5 found with name /movie-validator"
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

To ensure optimal performance with the Filter processor, thoroughly understand your incoming data format and rigorously test your configuration. **Use the most specific filtering criteria possible** to minimize the risk of inadvertently dropping important data.

This configuration can be extended to filter spans based on various attributes, tags, or custom criteria, enhancing the OpenTelemetry Collector's flexibility and efficiency for your specific observability requirements.
{{% /notice %}}

> [!IMPORTANT]
> Stop the **Agent** and the **Gateway** processes by pressing `Ctrl-C` in their respective terminals.

<!--
---
The following excises can be done in your own time after the workshop.

**(Optional) Modify the Filter Condition**:

If you’d like, you can customize the filter condition to drop spans based on different criteria. This step is optional and can be explored later. For example, you might configure the filter to drop spans that include a specific tag or attribute.

Here’s an example of dropping spans based on an attribute:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'attributes["service.name"] == "frontend"'
```

This filter would drop spans where the `service.name` attribute is set to `frontend`.

**(Optional) Filter Multiple Spans**:

You can filter out multiple span names by extending the span list:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'name == "/_healthz"'
      - 'name == "/internal/metrics"'
```

This will drop spans with the names `"/_healthz"` and `"/internal/metrics"`.
-->
