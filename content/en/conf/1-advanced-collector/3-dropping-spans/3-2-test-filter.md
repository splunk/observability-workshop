---
title: 3.2 Test Filter Processor
linkTitle: 3.2 Test Filter Processor
weight: 2
---

To test your configuration, you'll need to generate some trace data that includes a span named `"/_healthz"`.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In your **Gateway terminal** window start the `gateway`.

```bash
../otelcol --config ./gateway.yaml
```

**Start the Agent**: In your **Agent terminal** window start the `agent`.

```bash
../otelcol --config ./agent.yaml
```

**Start the Loadgen**: In the **Spans terminal** window run the `loadgen` with the flag to also send `healthz` spans along with base spans:
  
```bash
../loadgen -health -count 5
```

**Verify `agent.out`**: Using `jq` confirm the name of the spans received by the `agent`:

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

**Check the Gateway Debug output**: Using `jq` confirm the name of the spans received by the `gateway`:

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

When using the `Filter` processor, make sure you understand the look of your incoming data and test the configuration thoroughly. In general, use **as specific a configuration as possible** to lower the risk of the wrong data being dropped.

You can further extend this configuration to filter out spans based on different attributes, tags, or other criteria, making the OpenTelemetry Collector more customizable and efficient for your observability needs.

> [!IMPORTANT]
> Stop the `agent` and the `gateway` processes by pressing `Ctrl-C` in their respective terminals.

{{% /notice %}}
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
