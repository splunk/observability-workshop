---
title: 2.1 Build the filter in Config Builder
linkTitle: 2.1 Configure the filter
weight: 1
---

{{% exercise title="Add the filter processor in Config Builder" %}}

{{< step "Create the filter processor" "1" >}}

Open **Data Management > OTel Collector Config Builder**, select
**Component Inventory**, and select **Add component**.

For **Component type**, select `processor`.

![Selecting processor as the component type](/images/obs1184/config-builder-component-type.png)

For **Component**, select `filter`, then select **Next**.

![Selecting the filter processor](/images/obs1184/config-builder-filter-component.png)

Use `health` as the component name so its Collector component ID is
`filter/health`.

In **Options**, set the top-level `error_mode` to `ignore`. Beside
`trace_conditions`, select **+** to add a condition group. Inside that group,
beside `conditions`, select **+** and enter:

```ottl
span.name == "/_healthz"
```

This OpenTelemetry Transformation Language (OTTL) expression compares the
current span's `name` field with the exact, case-sensitive value `/_healthz`.
When the expression evaluates to `true`, the filter processor drops that span.
All spans with other names continue through the pipeline. In this workshop,
`/_healthz` represents a frequent health-probe request that confirms service
availability but adds little value to application performance analysis.

Leave the condition group's `context` and `error_mode` fields empty. The
Collector infers the `span` context from `span.name`, and the group inherits
the top-level `error_mode`.

{{% notice title="Why these settings?" style="info" %}}
`trace_conditions` limits this rule to trace data, while `span.name` tells the
Collector to evaluate one span at a time. Setting `error_mode` to `ignore`
means that an evaluation error is logged and the processor continues with the
remaining telemetry. It does not mean that matching spans are ignored;
matching spans are deliberately removed.
{{% /notice %}}

{{% notice title="Use trace_conditions" style="note" %}}
The legacy `traces.span` filter configuration is deprecated. This workshop
uses `trace_conditions`. Config Builder represents the condition as a group
containing a `conditions` list.
{{% /notice %}}

![Adding a span-name condition under trace_conditions](/images/obs1184/config-builder-filter-trace-conditions.png)

Select **Preview**, confirm the generated YAML defines
`processors.filter/health`, and select **Add**.

![Previewing and adding the filter health component](/images/obs1184/config-builder-filter-health-preview.png)

{{< /step >}}

{{< step "Add the processor to the traces pipeline" "2" >}}

Select **Pipelines**, find `traces`, and select its pencil-shaped **Edit** icon.

In the **Edit pipeline** dialog, select **+** beside **processors** and add
`filter/health`. Place it immediately after `memory_limiter`, then select
**Edit**.

Processor order matters. `memory_limiter` stays first so it can protect the
Collector during memory pressure. The filter runs next, which removes the
unwanted health-check spans before resource enrichment, batching, local file
output, or cloud export. This avoids spending additional work on telemetry
that you have already decided not to retain.

{{% notice title="Keep the existing pipeline components" style="warning" %}}
Keep every currently selected receiver, processor, and exporter. Add only the
`filter/health` processor.
{{% /notice %}}

{{< /step >}}

{{< step "Review the generated YAML" "3" >}}

Select **Collector YAML** and confirm the generated configuration includes:

```yaml
processors:
  filter/health:
    error_mode: ignore
    trace_conditions:
      - conditions:
          - 'span.name == "/_healthz"'

service:
  pipelines:
    traces:
      receivers:
        - jaeger
        - otlp
        - zipkin
      processors:
        - memory_limiter
        - filter/health
        - resourcedetection
        - resource/add_mode
        - batch
      exporters:
        - debug
        - file/traces
```

If cloud export is enabled, `otlp_http` also appears under `exporters`. Confirm
that `filter/health` appears once and that all existing components remain
connected.

Keep this Config Builder project open. You will download the completed
configuration in Chapter 5.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The filter processor is connected to the traces pipeline. Continue to the sensitive-data scenario." >}}
