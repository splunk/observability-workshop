---
title: 4.1 Transform structured logs
linkTitle: 4.1 Configure the transform
weight: 1
---

{{% exercise title="Add the transform processor in Config Builder" %}}

{{< step "Create the transform processor" "1" >}}

In **Component Inventory**, select **Add component**. Select component type
`processor`, select component `transform`, and select **Next**.

Set `error_mode` to `ignore` so one malformed workshop line does not stop the
`logs/workshop` pipeline.

Under `log_statements`, select **+** to add a statement group and set its
context to `resource`. Under that group's `statements`, select **+** and enter:

```ottl
keep_keys(resource.attributes, ["com.splunk.sourcetype", "host.name", "otelcol.service.mode"])
```

This keeps the resource metadata used by the exercise and removes fields such
as `com.splunk.source`, `service.name`, and `os.type` from the exported log
resource.

Resource attributes describe the source that produced a group of log records;
they are different from attributes on an individual log record. Using the
`resource` context ensures that `keep_keys` changes only that shared source
metadata. An explicit allowlist also makes the intended output easier to
review than removing unwanted keys one at a time.

Under `log_statements`, select **+** again to add a second statement group and
set its context to `log`. Leave its `statements` list empty for now. The
expressions are too long for the Options fields, so you add the complete OTTL
statements in the Collector YAML editor.

The `log` context gives the statements access to the body, attributes, and
severity of each individual record. Keeping the resource and log operations
in separate context groups prevents a statement from accidentally targeting
the wrong part of the OpenTelemetry data model.

![The Transform Processor Options form with resource and log context groups](../../images/config-builder-transform-options-contexts.png)

If an empty statement row was added under the `log` context, use its trash-can
icon to remove it. Keep the `log` context with no statements beneath
it.

![The Transform Processor Options form with an empty log statements list](../../images/config-builder-transform-empty-log-statements.png)

Select **Preview**. Confirm that the preview contains one `transform`
processor, a `resource` context with the `keep_keys` statement, and an empty
`log` context. Select **Add**.

![Previewing the Transform Processor shell before adding it](../../images/config-builder-transform-preview.png)

{{< /step >}}

{{< step "Complete the log statements in Collector YAML" "2" >}}

Open **Collector YAML**, then select **Edit YAML**.

Find `processors`, then `transform`, then the empty `- context: log` entry.
Place the cursor on the next line below `- context: log`. Copy and paste the
entire indented block below exactly as shown:

```yaml
        statements:
          - set(log.cache, ParseJSON(log.body)) where IsMatch(log.body,
            "^\\{")
          - flatten(log.cache, "")
          - merge_maps(log.attributes, log.cache, "upsert")
          - set(log.severity_text, log.attributes["level"])
          - set(log.severity_number, 1) where log.severity_text ==
            "TRACE"
          - set(log.severity_number, 5) where log.severity_text ==
            "DEBUG"
          - set(log.severity_number, 9) where log.severity_text == "INFO"
          - set(log.severity_number, 13) where log.severity_text ==
            "WARN"
          - set(log.severity_number, 17) where log.severity_text ==
            "ERROR"
          - set(log.severity_number, 21) where log.severity_text ==
            "FATAL"
```

The indentation is part of the YAML. `statements:` must be nested beneath the
existing `- context: log` entry, and each `- set(...)` or function call must be
nested beneath `statements:`. Do not add a second `- context: log` entry.

Wait for the editor header to show **VALID**, then select **Save changes**.

`ParseJSON` creates a map in the temporary cache, `flatten` normalizes nested
fields, and `merge_maps(..., "upsert")` inserts new keys or replaces existing
keys in the log attributes. The remaining statements copy the embedded level
into `severity_text` and map it to an OpenTelemetry severity number.

The `where IsMatch(log.body, "^\\{")` clause attempts JSON parsing only when
the body begins with an opening brace. This avoids trying to parse ordinary
plain-text records as JSON. `error_mode: ignore` provides a second safeguard:
if one record is malformed, the Collector reports the error and continues
processing the rest of the batch.

The load generator produces `DEBUG`, `INFO`, `WARN`, and `ERROR`. The `TRACE`
and `FATAL` statements demonstrate how the mapping can cover additional input.

The saved configuration now defines one `transform` processor with both
statement groups.

{{% notice title="Cardinality guidance" style="warning" %}}
Promoting every JSON field to a top-level attribute is useful for this
exercise, but it can create high-cardinality data in production. Use an
explicit field allowlist for real workloads.
{{% /notice %}}

{{< /step >}}

{{< step "Add the processor to the workshop logs pipeline" "3" >}}

Select **Pipelines** and select the pencil-shaped **Edit** icon for
`logs/workshop`.
Select **+** beside **processors** and add `transform`. Keep every existing
receiver, processor, and exporter. Use the drag handle to place `transform`
after `resourcedetection`, then select **Edit**.

Open **Collector YAML** and confirm:

- `transform` contains one resource context and one log context.
- `transform` appears exactly once in the processors list under
  `service.pipelines.logs/workshop`.
- It appears after `resourcedetection`, allowing `host.name` to be detected
  before the resource allowlist is applied.
- `filter/health`, `attributes`, and `redaction` remain connected to `traces`.

The position after `resourcedetection` is intentional. If `transform` ran
first, `host.name` might not exist yet and therefore could not survive the
resource allowlist. `resource/add_mode` runs afterward and adds
`otelcol.service.mode=agent`, so the final log resource contains both the
detected host identity and the Collector mode used in later validation.

The complete workshop logs pipeline is equivalent to:

```yaml
service:
  pipelines:
    logs/workshop:
      receivers:
        - otlp
        - file_log/quotes
      processors:
        - memory_limiter
        - resourcedetection
        - transform
        - resource/add_mode
      exporters:
        - debug
        - file/logs
```

Review **Collector YAML** and resolve any errors shown. If `transform` is not
after `resourcedetection`, return to the Pipeline editor and use the drag
handle to move it. The resource allowlist must run after host metadata is
detected.

Keep the project open for Chapter 5.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The completed configuration is ready to download, deploy, and validate." >}}
