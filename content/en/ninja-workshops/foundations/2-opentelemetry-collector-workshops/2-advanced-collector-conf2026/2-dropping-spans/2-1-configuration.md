---
title: 2.1 Build the Filter in Config Builder
linkTitle: 2.1 Configure Filter
weight: 1
---

{{% exercise title="Add the filter processor in Config Builder" %}}

{{< step "Create the filter processor" "1" >}}

Open **Data Management > OTel Collector Config Builder**, select
**Component Inventory**, and click **Add component**.

![The Add component button in Component Inventory](../images/config-builder-component-inventory.png)

For **Component type**, select `processor`.

![Selecting processor as the component type](../images/config-builder-component-type.png)

For **Component**, select `filter`, then click **Next**.

![Selecting the filter processor](../images/config-builder-filter-component.png)

Use `health` as the component name so its Collector component ID is
`filter/health`.

In **Options**, set the top-level `error_mode` to `ignore`. Beside
`trace_conditions`, click **+** to add a condition group. Inside that group,
beside `conditions`, click **+** and enter:

```ottl
span.name == "/_healthz"
```

Leave the condition group's `context` and `error_mode` fields empty. The
Collector infers the `span` context from `span.name`, and the group inherits
the top-level `error_mode`.

{{% notice title="Why these settings?" style="info" %}}
The condition matches spans by name. Setting `error_mode` to `ignore` keeps the
pipeline running if a telemetry item cannot be evaluated.
{{% /notice %}}

{{% notice title="Use trace_conditions" style="note" %}}
The legacy `traces.span` filter configuration is deprecated. This workshop
uses `trace_conditions`. Config Builder represents the condition as a group
containing a `conditions` list.
{{% /notice %}}

![Adding a span-name condition under trace_conditions](../images/config-builder-filter-trace-conditions.png)

Select **Preview**, confirm the generated YAML defines
`processors.filter/health`, and click **Add**.

![Previewing and adding the filter health component](../images/config-builder-filter-health-preview.png)

{{< /step >}}

{{< step "Add the processor to the traces pipeline" "2" >}}

Select **Pipelines**, find `traces`, and click its pencil-shaped **Edit** icon.

![Editing the traces pipeline from the Pipelines tab](../images/config-builder-pipelines-edit.png)

In the **Edit pipeline** modal, click **+** beside **processors** and add
`filter/health`. Place it immediately after `memory_limiter`, then click
**Edit**.

![Adding filter health to the traces pipeline and placing it after memory limiter](../images/config-builder-traces-pipeline-filter-health.png)

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
        - otlp
      processors:
        - memory_limiter
        - filter/health
        - resource_detection
        - resource/add_mode
      exporters:
        - debug
        - file/traces
```

If cloud export is enabled, `otlp_http` also appears under `exporters`. The
important check is that `filter/health` appears once and all existing
components remain connected.

Keep this Config Builder project open. You will download the completed
configuration in Chapter 5.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The filter processor is connected to the traces pipeline. Continue to the sensitive-data scenario." >}}
