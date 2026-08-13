---
title: 3.1 Protect sensitive span attributes
linkTitle: 3.1 Configure protection
weight: 1
---

{{% exercise title="Add attributes and redaction processors" %}}

{{< step "Create the attributes processor" "1" >}}

In **Component Inventory**, select **Add component**. Select component type
`processor`, select component `attributes`, and select **Next**.

In **Options**, add these actions in order:

1. Update `user.phone_number` to `UNKNOWN NUMBER`.
2. Hash `user.email`.
3. Delete `user.password`.

Review **Preview**, then select **Add**. The generated component is equivalent
to:

```yaml
processors:
  attributes:
    actions:
      - key: user.phone_number
        action: update
        value: UNKNOWN NUMBER
      - key: user.email
        action: hash
      - key: user.password
        action: delete
```

These actions demonstrate three ways to handle known sensitive fields:

- `update` keeps the phone-number key but replaces its value with a safe
  placeholder. This is useful when downstream searches expect the key to
  exist.
- `hash` replaces the email address with a repeatable, non-plain-text value.
  You can correlate repeated values without exporting the original address.
- `delete` removes both the password key and its value because the field has
  no valid observability use in this scenario.

The attributes processor is a good fit when you know the exact attribute keys
and want a specific action for each one.

{{% notice title="Use the exact password key" style="info" %}}
The load generator emits `user.password`. The processor key must match it
exactly or the password attribute will remain in the exported span.
{{% /notice %}}

{{< /step >}}

{{< step "Create the redaction processor" "2" >}}

Select **Add component** again. Select component type `processor`, select
component `redaction`, and select **Next**.

In **Options**, set `allow_all_keys` to **True**. Beside `blocked_values`,
select **+** twice to create two entries, then paste one regular expression into
each entry:

```text
\b4[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b
\b5[1-5][0-9]{2}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b
```

The first pattern matches the sample Visa value and the second matches the
Mastercard value. The Amex value is intentionally left unmatched so the test
can demonstrate an incomplete policy.

![Configuring allow_all_keys and two blocked value patterns for the Redaction Processor](../../images/config-builder-redaction-options.png)

Scroll through the remaining options and set `summary` to `debug`. Leave the
database sanitizer options and all other optional fields unset.

{{% notice title="Why allow all keys?" style="info" %}}
Setting `allow_all_keys` to `true` retains attributes whose values do not match
a blocked pattern. The two matching payment-card values are masked; the
unmatched Amex value remains visible so you can recognize an incomplete
redaction policy during validation.
{{% /notice %}}

The redaction processor complements the attributes processor. Instead of
targeting a known key, it scans attribute values for the configured patterns.
This helps when the same kind of sensitive value can appear under different
keys. In production, review the patterns regularly and test them against every
format your applications can emit.

Review **Preview**, then select **Add**. The generated component is equivalent
to:

```yaml
processors:
  redaction:
    allow_all_keys: true
    blocked_values:
      - '\b4[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'
      - '\b5[1-5][0-9]{2}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'
    summary: debug
```

{{< /step >}}

{{< step "Add both processors to the traces pipeline" "3" >}}

Select **Pipelines** and select the pencil-shaped **Edit** icon for `traces`.
Select **+** beside **processors** to add `attributes`, then repeat to add
`redaction`. Keep every existing receiver, processor, and exporter. Use the
drag handles to place both new processors after `filter/health` and before
`resourcedetection`, then select **Edit**.

This order first removes spans you do not plan to keep, then protects the
sensitive values in the remaining spans. Resource detection and batching run
afterward, so every local or cloud exporter receives the protected version.

![Adding the attributes and redaction processors to the traces pipeline](../../images/config-builder-traces-attributes-redaction.png)

Use the screenshot as a UI reference for the add controls and drag handles.
Follow the processor order below for this workshop configuration.

Open **Collector YAML** and confirm:

- Both processor definitions are present.
- `attributes` and `redaction` each appear exactly once in
  `service.pipelines.traces.processors`.
- All existing trace receivers and exporters remain connected.

The complete traces pipeline is equivalent to:

```yaml
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
        - attributes
        - redaction
        - resourcedetection
        - resource/add_mode
        - batch
      exporters:
        - debug
        - file/traces
```

For this exercise, the order of `attributes` and `redaction` does not change
the result. Confirm that both appear exactly once and that all existing
receivers and exporters remain connected. Cloud-enabled configurations also
include `otlp_http`.

Keep the project open and continue to Chapter 4.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The traces pipeline now filters health checks and protects the selected sensitive attributes." >}}
