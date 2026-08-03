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

In **Options**, set `error_mode` to `ignore`. Under `trace_conditions`, add:

```ottl
span.name == "/_healthz"
```

{{% notice title="Why these settings?" style="info" %}}
The condition matches spans by name. Setting `error_mode` to `ignore` keeps the
pipeline running if a telemetry item cannot be evaluated.
{{% /notice %}}

![Configuring processor options](../images/config-builder-component-options.png)

Select **Preview**, confirm the generated YAML defines `processors.filter`,
and click **Add**.

![Previewing and adding the component](../images/config-builder-component-preview.png)

{{< /step >}}

{{< step "Add the processor to the traces pipeline" "2" >}}

Select **Pipelines**, find `traces`, and click its pencil-shaped **Edit** icon.

![Editing the traces pipeline from the Pipelines tab](../images/config-builder-pipelines-edit.png)

{{% notice title="About the screenshot" style="note" %}}
The screenshot includes an unused `otlp_grpc/gateway` component. This workshop
uses one Agent and does not add that component to a pipeline.
{{% /notice %}}

In the **Edit pipeline** modal, open the **processors** selector, select
`filter`, and click **Edit**.

![Selecting processors in the Edit pipeline modal](../images/config-builder-edit-pipeline-modal.png)

{{% notice title="Keep the existing pipeline components" style="warning" %}}
Keep every currently selected receiver, processor, and exporter. Add only the
`filter` processor. Clearing a checkbox removes that component from the
pipeline.
{{% /notice %}}

{{< /step >}}

{{< step "Review the generated YAML" "3" >}}

Select **Collector YAML** and confirm the generated configuration includes:

```yaml
processors:
  filter:
    error_mode: ignore
    trace_conditions:
      - 'span.name == "/_healthz"'

service:
  pipelines:
    traces:
      processors:
        - memory_limiter
        - resource/add_mode
        - batch
        - resource_detection
        - filter
```

The important checks are that `filter` appears exactly once in
`traces.processors` and that the existing receivers, processors, and exporters
remain connected.

Keep this Config Builder project open. You will download the completed
configuration in Chapter 5.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The filter processor is connected to the traces pipeline. Continue to the sensitive-data scenario." >}}
