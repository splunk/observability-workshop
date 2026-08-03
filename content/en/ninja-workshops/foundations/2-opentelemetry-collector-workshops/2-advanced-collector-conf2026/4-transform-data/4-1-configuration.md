---
title: 4.1 Transform Structured Logs
linkTitle: 4.1 Configure Transform
weight: 1
---

{{% exercise title="Add the transform processor in Config Builder" %}}

{{< step "Create the transform processor" "1" >}}

In **Component Inventory**, click **Add component**. Select component type
`processor`, select component `transform`, and click **Next**.

Set `error_mode` to `ignore` so one malformed workshop line does not stop the
logs pipeline.

Add a statement group with context `resource` and this statement:

```ottl
keep_keys(resource.attributes, ["com.splunk.sourcetype", "host.name", "otelcol.service.mode"])
```

This keeps the resource metadata used by the exercise and removes fields such
as `com.splunk.source`, `service.name`, and `os.type` from the exported log
resource.

{{< /step >}}

{{< step "Parse fields and map severity" "2" >}}

Add a second statement group with context `log` and these statements in order:

```ottl
set(log.cache, ParseJSON(log.body)) where IsMatch(log.body, "^\\{")
flatten(log.cache, "")
merge_maps(log.attributes, log.cache, "upsert")
set(log.severity_text, log.attributes["level"])
set(log.severity_number, 1) where log.severity_text == "TRACE"
set(log.severity_number, 5) where log.severity_text == "DEBUG"
set(log.severity_number, 9) where log.severity_text == "INFO"
set(log.severity_number, 13) where log.severity_text == "WARN"
set(log.severity_number, 17) where log.severity_text == "ERROR"
set(log.severity_number, 21) where log.severity_text == "FATAL"
```

`ParseJSON` creates a map in the temporary cache, `flatten` normalizes nested
fields, and `merge_maps(..., "upsert")` inserts new keys or replaces existing
keys in the log attributes. The remaining statements copy the embedded level
into `severity_text` and map it to an OpenTelemetry severity number.

The load generator produces `DEBUG`, `INFO`, `WARN`, and `ERROR`. The `TRACE`
and `FATAL` statements demonstrate how the mapping can cover additional input.

Review **Preview** and click **Add**. The generated configuration should define
one `transform` processor with both statement groups.

{{% notice title="Cardinality guidance" style="warning" %}}
Promoting every JSON field to a top-level attribute is useful for this
exercise, but it can create high-cardinality data in production. Use an
explicit field allowlist for real workloads.
{{% /notice %}}

{{< /step >}}

{{< step "Add the processor to the logs pipeline" "3" >}}

Select **Pipelines**, click the pencil-shaped **Edit** icon for `logs`, and
select `transform` in the **processors** selector. Keep all existing receivers,
processors, and exporters selected, then click **Edit**.

Open **Collector YAML** and confirm:

- `transform` contains one resource context and one log context.
- `transform` appears exactly once in `service.pipelines.logs.processors`.
- It appears after `resource_detection`, allowing `host.name` to be detected
  before the resource allowlist is applied.
- `filter`, `attributes`, and `redaction` remain connected to `traces`.

The relevant logs pipeline should be equivalent to:

```yaml
service:
  pipelines:
    logs:
      processors:
        - memory_limiter
        - resource/add_mode
        - batch
        - resource_detection
        - transform
```

Review **Collector YAML** and resolve any errors shown. If `transform` is not
after `resource_detection`, stop and ask the workshop facilitator before
continuing. The resource allowlist must run after host metadata is detected,
and the supplied Pipeline editor does not expose a separate reorder control.

Keep the project open for Chapter 5.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The completed configuration is ready to download, deploy, and validate." >}}
